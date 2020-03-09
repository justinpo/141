class Graph:
    def __init__(self, size):
        self._adj = []
        self._size = size
        for x in range(size):
            self._adj.append([])
    
    def addEdge(self, i, j):
        if i < 0 or i > self._size-1 or j < 0 or j > self._size-1:
            raise Exception("Does not exist")
        else:
            self._adj[i].append(j)

    def removeEdge(self, i, j):
        if i < 0 or i > self._size-1 or j < 0 or j > self._size-1:
            raise Exception("Does not exist")
        else:
            self._adj[i].remove(j)        

    def hasEdge(self, i, j):
        if i < 0 or i > self._size-1 or j < 0 or j > self._size-1:
            return False
        for x in self._adj[i]:
            if x == j:
                return True

        return False    
    
    def isPath(self, i, j):
        q = []

        q.append(i)
        visit = []
        for x in range(self._size):
            visit.append(False)
        
        while len(q) > 0:
            v = q[0]
            q.pop(0)
            if v == j:
                return True
            else:
                for x in self._adj[v]:
                    if not visit[x]:
                        q.append(x)
                        visit[x] = True
        return False

    def bfs(self, s):
        q = []

        visit = []
        for x in range(self._size):
            visit.append(False)
        q.append(s)
        visit[s] = True
        while len(q) > 0:
            v = q[0]
            print(v)
            q.pop(0)
            for x in self._adj[v]:
                if not visit[x]:
                    q.append(x)
                    visit[x] = True
        print("\n")

    def dfs(self, start):
        s = []

        visit = []
        for x in range(self._size):
            visit.append(False)

        s.append(start)

        while len(s) > 0:
            v = s[-1]
            if not visit[v]:
                print(v)
            visit[v] = True
            s.pop()
            adjv = []
            for x in self._adj[v]:
                adjv.insert(0, x)

            for x in adjv:
                if not visit[x]:
                    s.append(x)

        print("\n")

# g = Graph(9)

# g.addEdge(0,2)
# g.addEdge(0,4)

# g.addEdge(2,0)
# g.addEdge(2,3)
# g.addEdge(2,4)
# g.addEdge(2,7)

# g.addEdge(3,2)
# g.addEdge(3,4)
# g.addEdge(3,7)

# g.addEdge(4,0)
# g.addEdge(4,2)
# g.addEdge(4,3)
# g.addEdge(4,5)
# g.addEdge(4,6)
# g.addEdge(4,7)

# g.addEdge(5,4)

# g.addEdge(6,4)

# g.addEdge(7,2)
# g.addEdge(7,3)
# g.addEdge(7,4)
# g.addEdge(7,8)

# g.addEdge(8,7)

# print(g.isPath(0,1))
# print(g.isPath(0,8))
# print(g.isPath(8,0))

# g.bfs(4)
# g.dfs(4)