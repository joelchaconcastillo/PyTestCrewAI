example_dijkstra = """
import heapq

class ShortestPath:
    \"""
    A class to compute the shortest path in a weighted graph using Dijkstra's algorithm.
    \"""

    def __init__(self, graph):
        \"""
        Initialize with a graph.
        Graph should be a dictionary of the form:
        {
            'A': {'B': 1, 'C': 4},
            'B': {'C': 2, 'D': 5},
            'C': {'D': 1},
            'D': {}
        }
        \"""
        self.graph = graph

    def dijkstra(self, start):
        \"""
        Compute shortest distances from the start node to all other nodes.

        :param start: The starting node.
        :return: A tuple (distances, predecessors)
                 - distances: dict with the shortest distance to each node.
                 - predecessors: dict with previous node in the optimal path.
        \"""
        # Initialize distances and predecessors
        distances = {node: float('inf') for node in self.graph}
        predecessors = {node: None for node in self.graph}
        distances[start] = 0

        # Priority queue: (distance, node)
        pq = [(0, start)]

        while pq:
            current_distance, current_node = heapq.heappop(pq)

            # Skip outdated distances
            if current_distance > distances[current_node]:
                continue

            for neighbor, weight in self.graph[current_node].items():
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    predecessors[neighbor] = current_node
                    heapq.heappush(pq, (distance, neighbor))

        return distances, predecessors

    def get_path(self, predecessors, start, end):
        \"""
        Reconstruct the shortest path from start to end.

        :param predecessors: dict returned by dijkstra()
        :param start: starting node
        :param end: destination node
        :return: list of nodes representing the shortest path
        \"""
        path = []
        current = end
        while current is not None:
            path.insert(0, current)
            current = predecessors[current]

        if path[0] != start:
            return []  # No path found
        return path


# Example usage:
if __name__ == "__main__":
    graph = {
        'A': {'B': 1, 'C': 4},
        'B': {'C': 2, 'D': 5},
        'C': {'D': 1},
        'D': {}
    }

    sp = ShortestPath(graph)
    distances, predecessors = sp.dijkstra('A')
    path = sp.get_path(predecessors, 'A', 'D')

    print("Shortest distances:", distances)
    print("Path from A to D:", path)
"""
