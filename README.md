# pubs
```
from pubs import pNode, pGraph

graph = pGraph.PGraph("test")
a = graph.addNode('A')
b = graph.addNode('B',a)
c = graph.addNode('C',b)
a.getChildren()
d = graph.addNode('D')
d.getChildren()
c2 = graph.addNode('C',d)
graph.nodes()
graph.log()
```
