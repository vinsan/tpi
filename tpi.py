import snap
import GraphTools

def test_graph_1():
    G1 = snap.TUNGraph.New()
    for i in range(0,7):
         G1.AddNode(i)
    for i in range(0, 7):
         for j in range(i+1, 7):
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
    

def neighbor(g):
     N = {}
     for NI in g.Nodes():
         k = []
         for Id in NI.GetOutEdges():
             k.append(Id)
         N[NI.GetId()] = k
     return N

def computeValue(W, k, delta, g):
    index = -1
    max = -1
    for node in W:
        t = k[node]
        d = delta[node]
        if t > d:
            return node, None
        if(d!=0):
            newValue = (t*(t+1))/(d*(d+1))
            if max < newValue:
                index = node
                max = newValue
    return None, index   

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
     N = neighbor(g)	#6
     while(len(W)>0):	#7
          v = computeValue(W, k, delta, g)	#8
          if v[0] != None:
              v = v[0]
              s[v] = s[v]+k[v]-delta[v]	#9
              k[v] = delta[v]	#10
              if(k[v]==0):	#11
                    W.pop(v)	#12
          else:	#13
              v = v[1]	#14
              neighbors = N[v]
              for u in neighbors:	#15
                    delta[u] = delta[u]-1	#16
              W.pop(v)
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
