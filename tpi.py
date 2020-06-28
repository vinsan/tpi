import snap
import GraphTools

def test_graph_1():
    G1 = snap.TUNGraph.New()
    for i in range(1,8):
         G1.AddNode(i)
    for i in range(1, 8):
         for j in range(i+1, 8):
              G1.AddEdge(i,j)
    return G1

def test_graph_2():
    G2 = snap.TUNGraph.New()
    for i in range(0, 10):
        G2.AddNode(i)
    G2.AddEdge(0,1)
    G2.AddEdge(0,3)
    G2.AddEdge(3,4)
    G2.AddEdge(4,5)
    G2.AddEdge(5,2)
    G2.AddEdge(5,6)
    G2.AddEdge(5,7)
    G2.AddEdge(7,8)
    G2.AddEdge(9,1)
    G2.AddEdge(9,2)
    G2.AddEdge(9,3)
    G2.AddEdge(9,6)
    G2.AddEdge(9,7)
    G2.AddEdge(9,8)
    return G2
    

def neighbor(g, nodeID):
     N = []
     for nodes in g.Nodes():
          if(nodes.IsNbrNId(nodeID)):
               N.append((nodes.GetId(), nodes))
     return N

def exist(W, k , delta, g):
     for node in W:
          t = k[node]
          d = delta[node]
          if t > d:
              return node, W[node]
     return None

def argmax(W, k, delta, g):
     arg = None
     index = -1
     max = -1
     for node in W:
          newValue = (k[node]*(k[node]+1))/(delta[node]*(delta[node]+1))
          if max < newValue:
               arg = W[node]
               index = node;
               max = newValue
     return arg, index

def tpi(g):
     s = {}	#1
     W = {}
     delta = {}
     k = {}
     N = {}
     nodes = g.Nodes()
     for node in nodes:	#2
          id = node.GetId()
          s[id] = 0.0	#3
          W[id] = node
          delta[id] = float(node.GetDeg())	#4
          k[id] = g.GetIntAttrDatN(id, "threshold")	#5
          N[id] = neighbor(g, id)	#6
     while(len(W)>0):	#7
          v = exist(W, k, delta, g)	#8
          if v != None:
              id = v[0]
              sol = s[id]+k[id]-delta[id]
              s[id] = sol	#9
              k[id] = delta[id]	#10
              if(k[id]==0):	#11
                    W.pop(v[0])	#12
          else:	#13
              v = argmax(W, k, delta, g)	#14
              id = v[1]
              neighbors = N[id]
              for u in neighbors:	#15
                    index = u[0]
                    delta[index] = delta[index]-1	#16
                    nu = neighbor(g, u[0])
                    nu.remove((v[1], v[0]))
                    N[index] = nu	#17
              W.pop(v[1])
     return s 

def sol_size(sol):
    activeNodes = 0
    totalIncentive = 0
    for n in sol:
        if(sol[n]>0):
            activeNodes = activeNodes+1
            totalIncentive = totalIncentive+sol[n]
    print("Number of nodes with incentive: "+str(activeNodes)+", Total Incentive: "+str(totalIncentive))
    return activeNodes, totalIncentive

def execute_test():
    g = GraphTools.load_graph_from_txt("com-youtube.ungraph.txt")
    print('Graph Nodes: %d, Edges: %d' % (g.GetNodes(), g.GetEdges()))
    g = GraphTools.deferred_decisions_with_uniform_probability(g)
    print('After Deferred decision Nodes: %d, Edges: %d' % (g.GetNodes(), g.GetEdges()))
    g = GraphTools.constant_threshold_assignment(g, 2)
    s = tpi(g)
    sol_size(s)


def test():
     g1 = test_graph_1()
     print('Graph Nodes: %d, Edges: %d' % (g1.GetNodes(), g1.GetEdges()))
     g1 =GraphTools.deferred_decisions_with_uniform_probability(g1)
     g1 = GraphTools.constant_threshold_assignment(g1, 2)
     print('After Deferred decision Nodes: %d, Edges: %d' % (g1.GetNodes(), g1.GetEdges()))
     s1 = tpi(g1)
     sol_size(s1)
     g2 = test_graph_2()
     print('Graph Nodes: %d, Edges: %d' % (g2.GetNodes(), g2.GetEdges()))
     g2 =GraphTools.deferred_decisions_with_uniform_probability(g2)
     g2 = GraphTools.constant_threshold_assignment(g2, 2)
     print('After Deferred decision Nodes: %d, Edges: %d' % (g2.GetNodes(), g2.GetEdges()))
     s2 = tpi(g2)
     sol_size(s2)
