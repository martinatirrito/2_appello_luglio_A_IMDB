
import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._idMapR = {}

    def buildGraph(self, date1, date2):
        self._graph.clear()
        nodi = DAO.getAllNodes(date1, date2)
        for n in nodi:
            self._idMapR[n.name_id] = n
        self._graph.add_nodes_from(nodi)

        edges = DAO.getAllEdges(self._idMapR, date1, date2)
        for e in edges:
            self._graph.add_edge(e.r1, e.r2, weight = e.peso)

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getBestDegree(self):  # GRADO MAGGIORE NODO
        if len(self._graph.nodes) == 0:
            return None, 0

        max_degree = -1
        best_regista = None
        for node, degree in self._graph.degree():
            if degree > max_degree:
                max_degree = degree
                best_regista = node
        return best_regista, max_degree

    def getSommaPesiIncidenti(self):  # PESI INCIDENTI MASSIMA
        if len(self._graph.nodes) == 0:
            return None, 0

        max_sum = -1
        best_regista = None
        for node in self._graph.nodes:
            weight_sum = sum(
                self._graph[node][neighbor]['weight']
                for neighbor in self._graph.neighbors(node)
            )
            if weight_sum > max_sum:
                max_sum = weight_sum
                best_regista = node
        return best_regista, max_sum

    def top5Archi(self):
        if len(self._graph.edges) == 0:
            return []

        edges_with_weights = []
        for u, v in self._graph.edges:
            u, v = sorted((u, v), key=lambda a: a.name)
            edges_with_weights.append((u, v, self._graph[u][v]['weight']))

        edges_sorted = sorted(edges_with_weights,
                              key=lambda x: (-x[2], x[0].name, x[1].name))

        return edges_sorted[:5]

    def getAllRegisti(self):
        return self._graph.nodes()
