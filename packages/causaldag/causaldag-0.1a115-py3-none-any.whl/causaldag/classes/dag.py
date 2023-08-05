# Author: Chandler Squires
"""Base class for causal DAGs
"""

from collections import defaultdict
import numpy as np
import itertools as itr
from causaldag.utils import core_utils
import operator as op
from typing import Set
import networkx as nx
import random


class CycleError(Exception):
    def __init__(self, cycle):
        self.cycle = cycle
        message = 'Adding arc(s) causes the cycle ' + path2str(cycle)
        super().__init__(message)

def path2str(path):
    return '->'.join(map(str, path))


class DAG:
    """
    Base class for causal DAGs.
    """
    def __init__(self, nodes: Set=set(), arcs: Set=set(), dag=None):
        if dag is not None:
            self._nodes = set(dag._nodes)
            self._arcs = set(dag._arcs)
            self._neighbors = defaultdict(set)
            for node, nbrs in dag._neighbors.items():
                self._neighbors[node] = set(nbrs)
            self._parents = defaultdict(set)
            for node, par in dag._parents.items():
                self._parents[node] = set(par)
            self._children = defaultdict(set)
            for node, ch in dag._children.items():
                self._children[node] = set(ch)
        else:
            self._nodes = set(nodes)
            self._arcs = set()
            self._neighbors = defaultdict(set)
            self._parents = defaultdict(set)
            self._children = defaultdict(set)
            self.add_arcs_from(arcs, unsafe=True)

    def __eq__(self, other):
        if not isinstance(other, DAG):
            return False
        return self._nodes == other._nodes and self._arcs == other._arcs

    def __str__(self):
        t = self.topological_sort()
        substrings = []
        for node in t:
            if self._parents[node]:
                parents_str = ','.join(map(str, self._parents[node]))
                substrings.append('[%s|%s]' % (node, parents_str))
            else:
                substrings.append('[%s]' % node)
        return ''.join(substrings)

    def __repr__(self):
        return str(self)

    @classmethod
    def from_amat(cls, amat):
        """Return a DAG with arcs given by amat
        """
        nodes = set(range(amat.shape[0]))
        arcs = set()
        d = DAG(nodes=nodes)
        for (i, j), val in np.ndenumerate(amat):
            if val != 0:
                d.add_arc(i, j)
        return d

    def copy(self):
        """Return a copy of the current DAG


        """
        # return DAG(nodes=self._nodes, arcs=self._arcs)
        return DAG(dag=self)

    # === PROPERTIES
    @property
    def nodes(self):
        return set(self._nodes)

    @property
    def nnodes(self):
        return len(self._nodes)

    @property
    def arcs(self):
        return set(self._arcs)

    @property
    def num_arcs(self):
        return len(self._arcs)

    @property
    def neighbors(self):
        return core_utils.defdict2dict(self._neighbors, self._nodes)

    @property
    def parents(self):
        return core_utils.defdict2dict(self._parents, self._nodes)

    @property
    def children(self):
        return core_utils.defdict2dict(self._children, self._nodes)

    @property
    def skeleton(self):
        return {frozenset({i, j}) for i, j in self._arcs}

    @property
    def in_degrees(self):
        return {node: len(self._parents[node]) for node in self._nodes}

    @property
    def out_degrees(self):
        return {node: len(self._children[node]) for node in self._nodes}

    @property
    def max_in_degree(self):
        return max(len(self._parents[node]) for node in self._nodes)

    @property
    def max_out_degree(self):
        return max(len(self._parents[node]) for node in self._nodes)

    @property
    def sparsity(self):
        p = len(self._nodes)
        return len(self._arcs) / p / (p-1) * 2

    def parents_of(self, node):
        return self._parents[node].copy()

    def children_of(self, node):
        return self._children[node].copy()

    def neighbors_of(self, node):
        return self._neighbors[node].copy()

    def has_arc(self, source, target):
        return (source, target) in self._arcs

    def is_upstream_of(self, anc, desc):
        """Check if `anc` is upstream from `desc`

        Return
        ------
        bool
            True if `anc` is upstream of `desc`

        Example
        -------
        >>> g = cd.DAG(arcs={(1, 2), (1, 3), (2, 3)})
        >>> g.is_upstream_of(1, 3)
        True
        >>> g.is_upstream_of(3, 1)
        False
        """
        return desc in self._children[anc] or desc in self.downstream(anc)

    # === MUTATORS
    def add_node(self, node):
        """Add a node to the DAG

        Parameters
        ----------
        node:
            a hashable Python object

        See Also
        --------
        add_nodes_from

        Examples
        --------
        >>> g = cd.DAG()
        >>> g.add_node(1)
        >>> g.add_node(2)
        >>> len(g.nodes)
        2
        """
        self._nodes.add(node)

    def add_arc(self, i, j, unsafe=False):
        """Add an arc to the DAG

        Parameters
        ----------
        i:
            source node of the arc
        j:
            target node of the arc

        See Also
        --------
        add_arcs_from

        Examples
        --------
        >>> g = cd.DAG({1, 2})
        >>> g.add_arc(1, 2)
        >>> g.arcs
        {(1, 2)}
        """
        self._nodes.add(i)
        self._nodes.add(j)
        self._arcs.add((i, j))

        self._neighbors[i].add(j)
        self._neighbors[j].add(i)

        self._children[i].add(j)
        self._parents[j].add(i)

        if not unsafe:
            try:
                self._check_acyclic()
            except CycleError as e:
                self.remove_arc(i, j)
                raise e

    def _check_acyclic(self):
        self.topological_sort()

    def _mark_children_visited(self, node, any_visited, curr_path_visited, curr_path, stack):
        any_visited[node] = True
        curr_path_visited[node] = True
        curr_path.append(node)
        for child in self._children[node]:
            if not any_visited[child]:
                self._mark_children_visited(child, any_visited, curr_path_visited, curr_path, stack)
            elif curr_path_visited[child]:
                cycle = curr_path + [child]
                raise CycleError(cycle)
        curr_path.pop()
        curr_path_visited[node] = False
        stack.append(node)

    def topological_sort(self):
        """Return a topological sort of the nodes in the graph

        Returns
        -------
        List[Node]
            Return a topological sort of the nodes in a graph.

        Examples
        --------
        >>> g = cd.DAG(arcs={(1, 2), (2, 3)})
        >>> g.topological_sort
        [1, 2, 3]
        """
        any_visited = {node: False for node in self._nodes}
        curr_path_visited = {node: False for node in self._nodes}
        curr_path = []
        stack = []
        for node in self._nodes:
            if not any_visited[node]:
                self._mark_children_visited(node, any_visited, curr_path_visited, curr_path, stack)
        return list(reversed(stack))

    def add_nodes_from(self, nodes):
        """Add nodes to the graph from a collection

        Parameters
        ----------
        nodes:
            collection of nodes to be added

        See Also
        --------
        add_node

        Examples
        --------
        >>> g = cd.DAG({1, 2})
        >>> g.add_nodes_from({'a', 'b'})
        >>> g.add_nodes_from(range(3, 6))
        >>> g.nodes
        {1, 2, 'a', 'b', 3, 4, 5}
        """
        for node in nodes:
            self.add_node(node)

    def add_arcs_from(self, arcs, unsafe=False):
        """Add arcs to the graph from a collection

        Parameters
        ----------
        arcs:
            collection of arcs to be added

        See Also
        --------
        add_arcs

        Examples
        --------
        >>> g = cd.DAG(arcs={(1, 2)})
        >>> g.add_arcs_from({(1, 3), (2, 3)})
        >>> g.arcs
        {(1, 2), (1, 3), (2, 3)}
        """
        if not arcs:
            return

        sources, sinks = zip(*arcs)
        self._nodes.update(sources)
        self._nodes.update(sinks)
        self._arcs.update(arcs)
        for i, j in arcs:
            self._neighbors[i].add(j)
            self._neighbors[j].add(i)
            self._children[i].add(j)
            self._parents[j].add(i)

        if not unsafe:
            try:
                self._check_acyclic()
            except CycleError as e:
                for i, j in arcs:
                    self.remove_arc(i, j)
                raise e

    def reverse_arc(self, i, j, ignore_error=False, unsafe=False):
        """Reverse the arc i->j to i<-j

        Parameters
        ----------
        i:
            source of arc to be reversed
        j:
            target of arc to be reversed
        ignore_error:
            if True, ignore the KeyError raised when arc is not in the DAG

        Examples
        --------
        >>> g = cd.DAG(arcs={(1, 2)})
        >>> g.reverse_arc(1, 2)
        >>> g.arcs
        {(2, 1)}
        """
        self.remove_arc(i, j, ignore_error=ignore_error)
        self.add_arc(j, i, unsafe=unsafe)

    def remove_arc(self, i, j, ignore_error=False):
        """Remove the arc i->j

        Parameters
        ----------
        i:
            source of arc to be removed
        j:
            target of arc to be removed
        ignore_error:
            if True, ignore the KeyError raised when arc is not in the DAG

        Examples
        --------
        >>> g = cd.DAG(arcs={(1, 2)})
        >>> g.remove_arc(1, 2)
        >>> g.arcs
        set()
        """
        try:
            self._arcs.remove((i, j))
            self._parents[j].remove(i)
            self._children[i].remove(j)
            self._neighbors[j].remove(i)
            self._neighbors[i].remove(j)
        except KeyError as e:
            if ignore_error:
                pass
            else:
                raise e

    def remove_arcs(self, arcs, ignore_error=False):
        for i, j in arcs:
            self.remove_arc(i, j, ignore_error=ignore_error)

    def remove_node(self, node, ignore_error=False):
        """Remove a node from the graph

        Parameters
        ----------
        node:
            node to be removed
        ignore_error:
            if True, ignore the KeyError raised when node is not in the DAG

        Examples
        --------
        >>> g = cd.DAG(arcs={(1, 2)})
        >>> g.remove_node(2)
        >>> g.nodes
        {1}
        """
        try:
            self._nodes.remove(node)
            for parent in self._parents[node]:
                self._children[parent].remove(node)
                self._neighbors[parent].remove(node)
            for child in self._children[node]:
                self._parents[child].remove(node)
                self._neighbors[child].remove(node)
            del self._neighbors[node]
            del self._parents[node]
            del self._children[node]
            self._arcs = {(i, j) for i, j in self._arcs if i != node and j != node}

        except KeyError as e:
            if ignore_error:
                pass
            else:
                raise e

    # === GRAPH PROPERTIES
    def sources(self):
        """Get all nodes in the graph that have no parents

        Return
        ------
        List[node]
            Nodes in the graph that have no parents

        Example
        -------
        >>> g = cd.DAG(arcs={(1, 2), (1, 3), (2, 3)})
        >>> g.sources()
        {1)
        """
        return {node for node in self._nodes if len(self._parents[node]) == 0}

    def sinks(self):
        """Get all nodes in the graph that have no children

        Return
        ------
        List[node]
            Nodes in the graph that have no children

        Example
        -------
        >>> g = cd.DAG(arcs={(1, 2), (1, 3), (2, 3)})
        >>> g.sinks()
        {3)
        """
        return {node for node in self._nodes if len(self._children[node]) == 0}

    def reversible_arcs(self):
        """Get all reversible (aka covered) arcs in the DAG.

        Return
        ------
        List[arc]
            Return all reversible (aka covered) arcs in the DAG. An arc i -> j is *covered* if the :math:`Pa(j) = Pa(i) \cup {i}`.
            Reversing a reversible arc results in a DAG in the same Markov equivalence class.

        Example
        -------
        >>> g = cd.DAG(arcs={(1, 2), (1, 3), (2, 3)})
        >>> g.reversible_arcs()
        {(1, 2), (2, 3))
        """
        reversible_arcs = set()
        for i, j in self._arcs:
            if self._parents[i] == (self._parents[j] - {i}):
                reversible_arcs.add((i, j))
        return reversible_arcs

    def is_reversible(self, i, j):
        return self._parents[i] == self._parents[j] - {i}

    def arcs_in_vstructures(self):
        """Get all arcs in the graph that participate in a v-structure.

        Return
        ------
        List[arc]
            Return all arcs in the graph in a v-structure (aka an immorality). A v-structure is formed when i->j<-k but
            there is no arc between i and k. Arcs that participate in a v-structure are identifiable from observational
            data.

        Example
        -------
        >>> g = cd.DAG(arcs={(1, 3), (2, 3)})
        >>> g.arcs_in_vstructures()
        {(1, 3), (2, 3))
        """
        vstruct_arcs = set()
        for node in self._nodes:
            for p1, p2 in itr.combinations(self._parents[node], 2):
                if p1 not in self._parents[p2] and p2 not in self._parents[p1]:
                    vstruct_arcs.add((p1, node))
                    vstruct_arcs.add((p2, node))
        return vstruct_arcs

    def vstructures(self):
        vstructs = set()
        for node in self._nodes:
            for p1, p2 in itr.combinations(self._parents[node], 2):
                if p1 not in self._parents[p2] and p2 not in self._parents[p1]:
                    vstructs.add((p1, node, p2))
        return vstructs

    def induced_graph(self, nodes):
        return DAG(nodes=nodes, arcs={(i, j) for i, j in self._arcs if (i in nodes) and (j in nodes)})

    def markov_blanket(self, node):
        parents_of_children = set.union(*(self._parents[c] for c in self._children[node])) if self._children[node] else set()
        return self._parents[node] | self._children[node] | parents_of_children - {node}

    # === COMPARISON
    def chickering_distance(self, other):
        reversals = self._arcs & {tuple(reversed(arc)) for arc in other._arcs}
        return len(reversals) + 2*self.shd_skeleton(other)

    def shd(self, other) -> int:
        """Compute the structural Hamming distance between this DAG and another graph

        Parameters
        ----------
        other:
            the DAG to which the SHD will be computed.

        Return
        ------
        int
            The structural Hamming distance between :math:`G_1` and :math:`G_2` is the minimum number of arc additions,
            deletions, and reversals required to transform :math:`G_1` into :math:`G_2` (and vice versa).

        Example
        -------
        >>> g1 = cd.DAG(arcs={(1, 2), (2, 3)})
        >>> g2 = cd.DAG(arcs={(2, 1), (2, 3)})
        >>> g1.shd(g2)
        1
        """
        if isinstance(other, DAG):
            self_arcs_reversed = {(j, i) for i, j in self._arcs}
            other_arcs_reversed = {(j, i) for i, j in other._arcs}

            additions = other._arcs - self._arcs - self_arcs_reversed
            deletions = self._arcs - other._arcs - other_arcs_reversed
            reversals = self.arcs & other_arcs_reversed
            return len(additions) + len(deletions) + len(reversals)

    def shd_skeleton(self, other) -> int:
        """Compute the structure Hamming distance between the skeleton of this DAG and the skeleton of another graph

        Parameters
        ----------
        other:
            the DAG to which the SHD of the skeleton will be computed.

        Return
        ------
        int
            The structural Hamming distance between :math:`G_1` and :math:`G_2` is the minimum number of arc additions,
            deletions, and reversals required to transform :math:`G_1` into :math:`G_2` (and vice versa).

        Example
        -------
        >>> g1 = cd.DAG(arcs={(1, 2), (2, 3)})
        >>> g2 = cd.DAG(arcs={(2, 1), (2, 3)})
        >>> g1.shd_skeleton(g2)
        0

        >>> g1 = cd.DAG(arcs={(1, 2)})
        >>> g2 = cd.DAG(arcs={(1, 2), (2, 3)})
        >>> g1.shd_skeleton(g2)
        1
        """
        if isinstance(other, DAG):
            return len(self.skeleton.symmetric_difference(other.skeleton))

    def markov_equivalent(self, other, interventions=None) -> bool:
        """Check if this DAG is (interventionally) Markov equivalent to some other DAG
        """
        if interventions is None:
            return self.cpdag() == other.cpdag()
        else:
            return self.interventional_cpdag(interventions, self.cpdag()) == other.interventional_cpdag(interventions, other.cpdag())

    def local_markov_statements(self):
        statements = set()
        for node in self._nodes:
            parents = self._parents[node]
            nondescendants = self._nodes - {node} - self.downstream(node) - parents
            statements.add((node, frozenset(nondescendants), frozenset(parents)))
        return statements

    def is_imap(self, other):
        return all(other.dsep(node, nondesc, parents) for node, nondesc, parents in self.local_markov_statements())

    def is_minimal_imap(self, other, certify=False, check_imap=True):
        if check_imap and not self.is_imap(other):
            if certify: return False, None
            else: return False

        certificate = next(((i, j) for i, j in self._arcs if other.dsep(i, j, self._parents[j] - {i})), None)
        if certify: return certificate is None, certificate
        else: return certificate is None

    # === CONVENIENCE
    def _add_downstream(self, downstream, node):
        for child in self._children[node]:
            if child not in downstream:
                downstream.add(child)
                self._add_downstream(downstream, child)

    def downstream(self, node):
        """Return the nodes downstream of node

        Parameters
        ----------
        node:
            The node.

        See Also
        --------
        upstream

        Return
        ------
        Set[node]
            Return all nodes j such that there is a directed path from node to j.

        Example
        -------
        >>> g = cd.DAG(arcs={(1, 2), (2, 3)})
        >>> g.downstream(1)
        {2, 3}
        """
        downstream = set()
        self._add_downstream(downstream, node)
        return downstream

    def _add_upstream(self, upstream, node):
        for parent in self._parents[node]:
            if parent not in upstream:
                upstream.add(parent)
                self._add_upstream(upstream, parent)

    def upstream(self, node):
        """Return the nodes upstream of node

        Parameters
        ----------
        node:
            The node.

        See Also
        --------
        downstream

        Return
        ------
        Set[node]
            Return all nodes j such that there is a directed path from j to node.

        Example
        -------
        >>> g = cd.DAG(arcs={(1, 2), (2, 3)})
        >>> g.upstream(3)
        {1, 2, 3g}
        """
        upstream = set()
        self._add_upstream(upstream, node)
        return upstream

    def incident_arcs(self, node):
        """Return all arcs adjacent to node

        Parameters
        ----------
        node:
            The node.

        See Also
        --------
        incoming_arcs, outgoing_arcs

        Return
        ------
        Set[arc]
            Return all arcs i->j such that either i=node of j=node.

        Example
        -------
        >>> g = cd.DAG(arcs={(1, 2), (1, 3), (2, 3)})
        >>> g.incident_arcs(2)
        {(1, 2), (2, 3)}
        """
        incident_arcs = set()
        for child in self._children[node]:
            incident_arcs.add((node, child))
        for parent in self._parents[node]:
            incident_arcs.add((parent, node))
        return incident_arcs

    def incoming_arcs(self, node):
        """Return all arcs with target node

        Parameters
        ----------
        node:
            The node.

        See Also
        --------
        incident_arcs, outgoing_arcs

        Return
        ------
        Set[arc]
            Return all arcs i->node.

        Example
        -------
        >>> g = cd.DAG(arcs={(1, 2), (1, 3), (2, 3)})
        >>> g.incoming_arcs(2)
        {(1, 2)}
        """
        incoming_arcs = set()
        for parent in self._parents[node]:
            incoming_arcs.add((parent, node))
        return incoming_arcs

    def outgoing_arcs(self, node):
        """Return all arcs with source node

        Parameters
        ----------
        node:
            The node.

        See Also
        --------
        incident_arcs, incoming_arcs

        Return
        ------
        Set[arc]
            Return all arcs node->j.

        Example
        -------
        >>> g = cd.DAG(arcs={(1, 2), (1, 3), (2, 3)})
        >>> g.outgoing_arcs(2)
        {(2, 3)}
        """
        outgoing_arcs = set()
        for child in self._children[node]:
            outgoing_arcs.add((node, child))
        return outgoing_arcs

    def outdegree(self, node):
        """Return the outdegree of node

        Parameters
        ----------
        node:
            The node.

        See Also
        --------
        indegree

        Return
        ------
        int
            Return the number of children of node.

        Example
        -------
        >>> g = cd.DAG(arcs={(1, 2), (1, 3), (2, 3)})
        >>> g.outdegree(1)
        2
        >>> g.outdegree(3)
        0
        """
        return len(self._children[node])

    def indegree(self, node):
        """Return the indegree of node

        Parameters
        ----------
        node:
            The node.

        See Also
        --------
        outdegree

        Return
        ------
        int
            Return the number of parents of node.

        Example
        -------
        >>> g = cd.DAG(arcs={(1, 2), (1, 3), (2, 3)})
        >>> g.indegree(1)
        0
        >>> g.indegree(2)
        2
        """
        return len(self._parents[node])

    def upstream_most(self, s):
        """
        Parameters
        ----------
        s:
            Set of nodes

        Returns
        -------
        The set of nodes in s with no ancestors in s
        """
        return {node for node in s if not self.upstream(node) & s}

    # === CONVERTERS
    def resolved_sinks(self, other):
        res_sinks = set()
        while True:
            new_resolved = {
                node for node in self._nodes - res_sinks
                if not (self._children[node] - res_sinks) and
                   not (other._children[node] - res_sinks) and
                   self._parents[node] == other._parents[node]
            }
            res_sinks.update(new_resolved)
            if not new_resolved:
                break

        return res_sinks

    def chickering_sequence(self, imap, verbose=False):
        curr_graph = self

        ch_seq = []
        moves = []
        last_sink = None
        while curr_graph != imap:
            ch_seq.append(curr_graph)
            curr_graph, last_sink, move = curr_graph.apply_edge_operation(imap, seed_sink=last_sink, verbose=verbose)
            moves.append(move)

        ch_seq.append(imap)
        return ch_seq, moves

    def apply_edge_operation(self, imap, seed_sink=None, verbose=False):
        new_graph = self.copy()

        # STEP 2: REMOVE RESOLVED SINKS
        resolved_sinks = self.resolved_sinks(imap)
        self_subgraph = self.induced_graph(self._nodes - resolved_sinks)
        imap_subgraph = imap.induced_graph(imap._nodes - resolved_sinks)

        # STEP 3: PICK A SINK IN THE IMAP
        imap_sinks = imap_subgraph.sinks()
        sink = random.choice(list(imap_sinks)) if seed_sink is None or seed_sink not in imap_sinks else seed_sink
        if verbose: print(f"Step 3: Picked {sink}")

        # STEP 4: ADD A PARENT IF Y IS A SINK IN G
        if sink in self_subgraph.sinks():
            x = random.choice(list(imap_subgraph._parents[sink] - self_subgraph._parents[sink]))
            new_graph.add_arc(x, sink)
            if verbose: print(f"Step 4: Added {x}->{sink}")
            return new_graph, sink, 4

        # STEP 5: PICK A SPECIFIC CHILD OF Y IN G
        d = list(imap_subgraph.upstream_most(self_subgraph.downstream(sink)))[0]
        valid_children = self_subgraph.upstream_most(self_subgraph._children[sink]) & (self_subgraph.upstream(d) | {d})
        z = random.choice(list(valid_children))
        if verbose: print(f"Step 5: Picked z={z}")

        # STEP 6
        if self_subgraph.is_reversible(sink, z):
            new_graph.reverse_arc(sink, z)
            if verbose: print(f"Step 6: Reversing {sink}->{z}")
            return new_graph, sink, 6

        # STEP 7
        par_z = self_subgraph._parents[z] - self_subgraph._parents[sink] - {sink}
        if par_z:
            x = random.choice(list(par_z))
            if verbose: print(f"Step 7: Picked x={x}")
            new_graph.add_arc(x, sink)
            if verbose: print(f"Step 7: Adding {x}->{sink}")
            return new_graph, sink, 7

        # STEP 8
        par_sink = self_subgraph._parents[sink] - self_subgraph._parents[z]
        x = random.choice(list(par_sink))
        if verbose: print(f"Step 8: Picked x={x}")
        new_graph.add_arc(x, z)
        if verbose: print(f"Step 8: Adding {x}->{z}")
        return new_graph, sink, 8

    def marginal_mag(self, latent_nodes, relabel=None, new=True):
        from .ancestral_graph import AncestralGraph

        if not new:
            latent_nodes = core_utils.to_set(latent_nodes)

            new_nodes = self._nodes - latent_nodes
            directed = set()
            bidirected = set()
            for i, j in itr.combinations(self._nodes - latent_nodes, r=2):
                adjacent = all(not self.dsep(i, j, S) for S in core_utils.powerset(self._nodes - {i, j} - latent_nodes))
                if adjacent:
                    if self.is_upstream_of(i, j):
                        directed.add((i, j))
                    elif self.is_upstream_of(j, i):
                        directed.add((j, i))
                    else:
                        bidirected.add((i, j))

            if relabel:
                t = self.topological_sort()
                t_new = [node for node in t if node not in latent_nodes]
                node2new_label = dict(map(reversed, enumerate(t_new)))
                new_nodes = {node2new_label[node] for node in new_nodes}
                directed = {(node2new_label[i], node2new_label[j]) for i, j in directed}
                bidirected = {(node2new_label[i], node2new_label[j]) for i, j in bidirected}

            return AncestralGraph(nodes=new_nodes, directed=directed, bidirected=bidirected)

        else:
            ag = AncestralGraph(nodes=self._nodes, directed=self._arcs)
            curr_directed = ag.directed
            curr_bidirected = ag.bidirected

            while True:
                for node in latent_nodes:
                    for j, i in itr.product(ag._parents[node], ag._children[node]):
                        ag._add_directed(j, i, ignore_error=True)
                    for i, j in itr.combinations(ag._children[node], 2):
                        ag._add_bidirected(i, j, ignore_error=True)
                    for i, j in itr.product(ag._children[node], ag._spouses[node]):
                        ag._add_bidirected(i, j, ignore_error=True)

                last_directed = curr_directed
                last_bidirected = curr_bidirected
                curr_directed = ag.directed
                curr_bidirected = ag.bidirected
                if curr_directed == last_directed and curr_bidirected == last_bidirected:
                    break
            for node in latent_nodes:
                ag.remove_node(node, ignore_error=True)

            if relabel is not None:
                if relabel == 'default':
                    relabel = {node: ix for ix, node in enumerate(sorted(self._nodes - set(latent_nodes)))}
                new_nodes = {relabel[node] for node in self._nodes - set(latent_nodes)}
                directed = {(relabel[i], relabel[j]) for i, j in ag.directed}
                bidirected = {(relabel[i], relabel[j]) for i, j in ag.bidirected}
                return AncestralGraph(new_nodes, directed=directed, bidirected=bidirected)

            return ag



    def save_gml(self, filename):
        tab = '  '
        indent = 0
        newline = lambda indent: '\n' + (tab * indent)
        with open(filename, 'w') as f:
            f.write('graph [')
            indent += 1
            f.write(newline(indent))
            f.write('directed 1')
            f.write(newline(indent))
            node2ix = core_utils.ix_map_from_list(self._nodes)
            for node, ix in node2ix.items():
                f.write('node [')
                indent += 1
                f.write(newline(indent))
                f.write('id %s' % ix)
                f.write(newline(indent))
                f.write('label "%s"' % node)
                indent -= 1
                f.write(newline(indent))
                f.write(']')
                f.write(newline(indent))
            for source, target in self._arcs:
                f.write('edge [')
                indent += 1
                f.write(newline(indent))
                f.write('source %s' % source)
                f.write(newline(indent))
                f.write('target %s' % target)
                indent -= 1
                f.write(newline(indent))
                f.write(']')
                f.write(newline(indent))
            f.write(']')

    def to_dataframe(self, node_list=None):
        if not node_list:
            node_list = sorted(self._nodes)
        node2ix = {node: i for i, node in enumerate(node_list)}

        shape = (len(self._nodes), len(self._nodes))
        amat = np.zeros(shape, dtype=int)
        for source, target in self._arcs:
            amat[node2ix[source], node2ix[target]] = 1

        from pandas import DataFrame
        return DataFrame(amat, index=node_list, columns=node_list)

    @classmethod
    def from_dataframe(cls, df):
        g = DAG(nodes=set(df.index)|set(df.columns))
        for (i, j), val in np.ndenumerate(df.values):
            if val != 0:
                g.add_arc(df.index[i], df.columns[j])
        return g

    @classmethod
    def from_nx(cls, nx_graph):
        return DAG(nodes=set(nx_graph.nodes), arcs=set(nx_graph.edges))

    def to_nx(self):
        g = nx.DiGraph()
        g.add_nodes_from(self._nodes)
        g.add_edges_from(self._arcs)
        return g

    def to_amat(self, node_list=None) -> (np.ndarray, list):
        """Return an adjacency matrix for DAG

        Parameters
        ----------
        node_list:
            List indexing the rows/columns of the matrix.

        See Also
        --------
        from_amat

        Return
        ------
        (amat, node_list)

        Example
        -------
        >>> g = cd.DAG(arcs={(1, 2), (1, 3), (2, 3)})
        >>> g.to_amat()[0]
        array([[0, 1, 1],
               [0, 0, 1],
               [0, 0, 0]])
        >>> g.to_amat()[1]
        [1, 2, 3]
        """
        if not node_list:
            node_list = sorted(self._nodes)
        node2ix = {node: i for i, node in enumerate(node_list)}

        shape = (len(self._nodes), len(self._nodes))
        amat = np.zeros(shape, dtype=int)

        for source, target in self._arcs:
            amat[node2ix[source], node2ix[target]] = 1

        return amat, node_list

    def subgraph(self, nodes):
        return DAG(nodes, {(i, j) for i, j in self._arcs if i in nodes and j in nodes})

    # === OPTIMAL INTERVENTIONS
    def directed_clique_tree(self, verbose=False):
        # === get max cliques
        g = nx.Graph()
        g.add_edges_from(self._arcs)
        max_cliques = {frozenset(c) for c in nx.chordal_graph_cliques(g)}

        clique_tree = nx.MultiDiGraph()
        # === return single node graph if already complete
        if len(max_cliques) == 1:
            clique_tree.add_node(max_cliques.pop())
            return clique_tree

        # === get edge weights and directions b/t cliques
        overlap_to_edges = defaultdict(set)
        is_bidirected_dict = dict()
        for c1, c2 in itr.combinations(max_cliques, 2):
            shared = c1 & c2
            if shared:
                all_into_c1 = all((s, c) in self._arcs for s, c in itr.product(shared, c1 - shared))
                all_into_c2 = all((s, c) in self._arcs for s, c in itr.product(shared, c2 - shared))
                is_bidirected = all_into_c1 and all_into_c2
                if not is_bidirected:
                    c1, c2 = (c1, c2) if all_into_c2 else (c2, c1)  # switch directions so c1 first
                is_bidirected_dict[(c1, c2)] = is_bidirected
                overlap_to_edges[len(c1 & c2)].add((c1, c2))

        if verbose: print(overlap_to_edges, is_bidirected_dict)
        current_threshold = max(overlap_to_edges)

        # greedily choose edges to create a directed clique tree
        for _ in range(len(max_cliques)-1):
            while current_threshold > 0:
                candidate_edges = list(overlap_to_edges[current_threshold])
                candidate_trees = [clique_tree.copy() for _ in candidate_edges]
                for t, (c1, c2) in zip(candidate_trees, candidate_edges):
                    if is_bidirected_dict[(c1, c2)]:
                        t.add_edge(c1, c2)
                        t.add_edge(c2, c1)
                    else:
                        t.add_edge(c1, c2)

                # only keep forests
                candidate_trees = [t for t in candidate_trees if nx.is_forest(t.to_undirected())]

                if not candidate_trees:
                    current_threshold -= 1
                    continue

                # only keep if single source in each component
                candidate_trees_no_collider = []
                for t in candidate_trees:
                    components = nx.strongly_connected_component_subgraphs(t)
                    components2parents = [set.union(*(set(t.predecessors(node)) - c.nodes() for node in c)) for c in components]
                    if all(len(parents) <= 1 for parents in components2parents):
                        candidate_trees_no_collider.append(t)
                if not candidate_trees_no_collider:
                    raise Exception("Can't find a collider-free tree")

                # choose clique tree without new -><->, if possible
                preferred_candidate_trees = []
                for t in candidate_trees_no_collider:
                    new_edge = set(t.edges()) - set(clique_tree.edges())
                    c1, c2 = list(new_edge)[0]
                    if not t.has_edge(c2, c1):
                        preferred_candidate_trees.append(t)
                    else:
                        if not set(t.predecessors(c1)) - {c2} and not set(t.predecessors(c2)) - {c1}:
                            preferred_candidate_trees.append(t)

                clique_tree = preferred_candidate_trees[0] if preferred_candidate_trees else candidate_trees_no_collider[0]
                if verbose: print(clique_tree.edges())
                break

        return clique_tree

    def cpdag(self):
        """Return the completed partially directed acyclic graph (CPDAG, aka essential graph) that represents the
        Markov equivalence class of this DAG
        """
        from causaldag import PDAG
        pdag = PDAG(nodes=self._nodes, arcs=self._arcs, known_arcs=self.arcs_in_vstructures())
        pdag.remove_unprotected_orientations()
        return pdag

    def moral_graph(self):
        from causaldag import UndirectedGraph
        edges = {(i, j) for i, j in self._arcs} | {(p1, p2) for p1, node, p2 in self.vstructures()}
        return UndirectedGraph(self._nodes, edges)

    def interventional_cpdag(self, interventions, cpdag=None):
        """Return the interventional essential graph (aka CPDAG) associated with this DAG."""
        from causaldag import PDAG

        if cpdag is None:
            raise ValueError('Need the CPDAG')
            # dag_cut = self.copy()
            # known_arcs = set()
            # for node in intervened_nodes:
            #     for i, j in dag_cut.incoming_arcs(node):
            #         dag_cut.remove_arc(i, j)
            #         known_arcs.update(self.outgoing_arcs(node))
            # known_arcs.update(dag_cut.vstructs())
            # pdag = PDAG(dag_cut._nodes, dag_cut._arcs, known_arcs=known_arcs)
        else:
            cut_edges = set()
            for iv_nodes in interventions:
                cut_edges.update({(i, j) for i, j in self._arcs if len({i, j} & set(iv_nodes)) == 1})
            known_arcs = cut_edges | cpdag._known_arcs
            pdag = PDAG(self._nodes, self._arcs, known_arcs=known_arcs)

        pdag.remove_unprotected_orientations()
        return pdag

    def greedy_optimal_single_node_intervention(self, cpdag=None, num_interventions=1):
        """
        Find the num_interventions single-node interventions which orient the most edges in this graph, using a greedy
        strategy. By submodularity, this will orient at least (1 - 1/e) as many edges as the true optimal intervention
        set.

        Parameters
        ----------
        cpdag:
            the starting CPDAG containing known orientations. If None, use the observational essential graph.
        num_interventions:
            the number of single-node interventions used. Default is 1.

        Return
        ------
        (interventions, cpdags)
            The selected interventions and the associated cpdags that they induce.
        """
        if cpdag is None:
            cpdag = self.cpdag()
        if len(cpdag.edges) == 0:
            return [None]*num_interventions, [cpdag]*num_interventions

        nodes2icpdags = {
            node: self.interventional_cpdag([{node}], cpdag=cpdag)
            for node in self._nodes - cpdag.dominated_nodes
        }
        nodes2num_oriented = {
            node: len(icpdag._arcs)
            for node, icpdag in nodes2icpdags.items()
        }

        best_iv = max(nodes2num_oriented.items(), key=op.itemgetter(1))[0]
        icpdag = nodes2icpdags[best_iv]

        if num_interventions == 1:
            return [best_iv], [icpdag]
        else:
            best_ivs, icpdags = self.greedy_optimal_single_node_intervention(cpdag=icpdag, num_interventions=num_interventions-1)
            return [best_iv] + best_ivs, [icpdag] + icpdags

    def greedy_optimal_fully_orienting_interventions(self, cpdag=None):
        """
        Find a set of interventions which fully orients a CPDAG into this DAG, using greedy selection of the
        interventions. By submodularity, the number of interventions is a (1 + ln K) multiplicative approximation
        to the true optimal number of interventions, where K is the number of undirected edges in the CPDAG.

        Parameters
        ----------
        cpdag
            the starting CPDAG containing known orientations. If None, use the observational essential graph.

        Returns
        -------
        (interventions, cpdags)
            The selected interventions and the associated cpdags that they induce.
        """
        if cpdag is None: cpdag = self.cpdag()
        curr_cpdag = cpdag
        ivs = []
        icpdags = []
        while len(curr_cpdag.edges) != 0:
            iv, icpdag = self.greedy_optimal_single_node_intervention(cpdag=curr_cpdag)
            iv = iv[0]
            icpdag = icpdag[0]
            curr_cpdag = icpdag
            ivs.append(iv)
            icpdags.append(icpdag)
        return ivs, icpdags

    def optimal_fully_orienting_interventions(self, cpdag=None):
        """
        Find the smallest set of interventions which fully orients the CPDAG into this DAG.

        Parameters
        ----------
        cpdag
            the starting CPDAG containing known orientations. If None, use the observational essential graph.

        Returns
        -------
        interventions
            A minimum-size set of interventions which fully orients the DAG.
        """
        cpdag = self.cpdag() if cpdag is None else cpdag
        node2oriented = {
            node: self.interventional_cpdag([{node}], cpdag=cpdag).arcs
            for node in self._nodes - cpdag.dominated_nodes
        }
        for ss in core_utils.powerset(self._nodes - cpdag.dominated_nodes, r_min=1):
            oriented = set.union(*(node2oriented[node] for node in ss))
            if len(oriented) == len(cpdag.edges) + len(cpdag.arcs):
                return ss

    def backdoor(self, i, j):
        """Return a set of nodes S satisfying the backdoor criterion if such an S exists, otherwise False.

        S satisfies the backdoor criterion if
        (i) S blocks every path from i to j with an arrow into i
        (ii) no node in S is a descendant of i


        """
        raise NotImplementedError
        pass

    def frontdoor(self, i, j):
        """Return a set of nodes S satisfying the frontdoor criterion if such an S exists, otherwise False.

        S satisfies the frontdoor criterion if
        (i) S blocks all directed paths from i to j
        (ii) there are no unblocked backdoor paths from i to S
        (iii) i blocks all backdoor paths from S to j

        """
        raise NotImplementedError()

    # === SEPARATIONS
    def dsep(self, A, B, C=set(), verbose=False, certify=False):
        """
        Check if A and B are d-separated given C, using the Bayes ball algorithm.

        Parameters
        ----------
        A:
            First set of nodes.
        B:
            Second set of nodes.
        C:
            Separating set of nodes.
        verbose:
            If True, print moves of the algorithm.

        See Also
        --------
        dsep_from_given

        Return
        ------
        is_dsep

        Example
        -------
        >>> g = cd.DAG(arcs={(1, 2), (3, 2)})
        >>> g.dsep(1, 3)
        True
        >>> g.dsep(1, 3, 2)
        False
        """
        # type coercion
        A = core_utils.to_set(A)
        B = core_utils.to_set(B)
        C = core_utils.to_set(C)

        # shade ancestors of C
        shaded_nodes = set(C)
        for node in C:
            self._add_upstream(shaded_nodes, node)

        visited = set()
        # marks for which direction the path is traveling through the node
        _c = '_c'  # child
        _p = '_p'  # parent

        schedule = {(node, _c) for node in A}
        while schedule:
            if verbose:
                print('Current schedule:', schedule)

            node, _dir = schedule.pop()
            if node in B and not certify: return False
            if node in B and certify: return False, node
            if (node, _dir) in visited: continue
            visited.add((node, _dir))

            if verbose:
                print('Going through node', node, 'in direction', _dir)

            # if coming from child, won't encounter v-structure
            if _dir == _c and node not in C:
                schedule.update({(parent, _c) for parent in self._parents[node]})
                schedule.update({(child, _p) for child in self._children[node]})

            if _dir == _p:
                # if coming from parent and see shaded node, can go through v-structure
                if node in shaded_nodes:
                    schedule.update({(parent, _c) for parent in self._parents[node]})

                # if coming from parent and see unconditioned node, can go through children
                if node not in C:
                    schedule.update({(child, _p) for child in self._children[node]})

        return True

    def is_invariant(self, A, intervened_nodes, cond_set=set(), verbose=False):
        """
        Check if the distribution of A given cond_set is invariant to an intervention on intervened_nodes.

        :math:`f^\emptyset(A|C) = f^I(A|C)` if the "intervention node" I with intervened_nodes as its children
        is d-separated from A given C. Equivalently, the :math:`f^\emptyset(A|C) \neq f^I(A|C)` if:

        - there is an active path to an intervened node that ends in an arrowhead, and that intervened node
            or one of its descendants is conditioned on.
        - there is an active path to an intervened node that ends in a tail, and that intervened node
            is not conditioned on.

        Parameters
        ----------
        A:
            Set of nodes.
        intervened_nodes:
            Nodes on which an intervention has occurred.
        cond_set:
            Conditioning set for the tested distribution.
        verbose:
            If True, print moves of the algorithm.
        """
        # type coercion
        A = core_utils.to_set(A)
        I = core_utils.to_set(intervened_nodes)
        C = core_utils.to_set(cond_set)

        # shade ancestors of C
        shaded_nodes = set(C)
        for node in C:
            self._add_upstream(shaded_nodes, node)

        visited = set()
        # marks for which direction the path is traveling through the node
        _c = '_c'  # child
        _p = '_p'  # parent

        schedule = {(node, _c) for node in A}
        while schedule:
            if verbose:
                print('Current schedule:', schedule)

            node, _dir = schedule.pop()
            if node in I and _dir == _p and node in shaded_nodes: return False
            if node in I and _dir == _c and node not in C: return False
            if (node, _dir) in visited: continue
            visited.add((node, _dir))

            if verbose:
                print('Going through node', node, 'in direction', _dir)

            # if coming from child, won't encounter v-structure
            if _dir == _c and node not in C:
                schedule.update({(parent, _c) for parent in self._parents[node]})
                schedule.update({(child, _p) for child in self._children[node]})

            if _dir == _p:
                # if coming from parent and see shaded node, can go through v-structure
                if node in shaded_nodes:
                    schedule.update({(parent, _c) for parent in self._parents[node]})

                # if coming from parent and see unconditioned node, can go through children
                if node not in C:
                    schedule.update({(child, _p) for child in self._children[node]})

        return True

    def dsep_from_given(self, A, C=set()):
        """
        Find all nodes d-separated from A given C .

        Uses algorithm in Geiger, D., Verma, T., & Pearl, J. (1990).
        Identifying independence in Bayesian networks. Networks, 20(5), 507-534.
        """
        A = core_utils.to_set(A)
        C = core_utils.to_set(C)

        determined = set()
        descendants = set()

        for c in C:
            determined.add(c)
            descendants.add(c)
            self._add_upstream(descendants, c)
            
        reachable = set()
        i_links = set()
        labeled_links = set()

        for a in A:
            i_links.add((None, a)) 
            reachable.add(a)
       
        while True:
            i_p_1_links = set()
            #Find all unlabled links v->w adjacent to at least one link u->v labeled i, such that (u->v,v->w) is a legal pair.
            for link in i_links:
                u, v = link
                for w in self._neighbors[v]:
                    if not u == w and (v, w) not in labeled_links:
                        if v in self._children[u] and v in self._children[w]:  #Is collider?
                            if v in descendants:
                                i_p_1_links.add((v,w))
                                reachable.add(w)
                        else:  #Not collider
                            if v not in determined:
                                i_p_1_links.add((v,w))
                                reachable.add(w)

            if len(i_p_1_links) == 0:
                break

            labeled_links = labeled_links.union(i_links)
            i_links = i_p_1_links

        return self._nodes.difference(A).difference(C).difference(reachable)


if __name__ == '__main__':
    d = DAG(arcs={(1, 2), (1, 3), (3, 4), (2, 4), (3, 5)})
    d.save_gml('test_mine.gml')

    def adversarial(p):
        arcs = set(itr.combinations(2**p, 2))

    



