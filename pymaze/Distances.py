from operator import itemgetter


class Distances(dict):
    def __init__(self, root):
        super().__init__()
        self.root = root
        self[self.root] = 0

    def cells(self):
        return self.keys()

    def path_to(self, goal):
        current = goal

        breadcrumbs = Distances(self.root)
        breadcrumbs[current] = self[current]

        while current != self.root:
            for neighbor in current.links:
                if self[neighbor] < self[current]:
                    breadcrumbs[neighbor] = self[neighbor]
                    current = neighbor
                    break

        return breadcrumbs

    def max(self):
        return max(self.items(), key=itemgetter(1))
