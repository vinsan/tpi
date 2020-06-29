import snap
import GraphTools

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
              W.pop(v) #18
     return s #19

def sol_size(sol):
    activeNodes = 0
    totalIncentive = 0
    for n in sol:
        if(sol[n]>0):
            activeNodes = activeNodes+1
            totalIncentive = totalIncentive+sol[n]
    print("Number of nodes with incentive: "+str(activeNodes)+", Total Incentive: "+str(totalIncentive))
    return activeNodes, totalIncentive

def load_graph():
    g = GraphTools.load_graph_from_txt("com-youtube.ungraph.txt")
    print('Graph Nodes: %d, Edges: %d' % (g.GetNodes(), g.GetEdges()))
    return g
    

def deferred_decision_uniform():
    g = GraphTools.deferred_decisions_with_uniform_probability(load_graph())
    print('After Deferred decision Nodes: %d, Edges: %d' % (g.GetNodes(), g.GetEdges()))
    return g

def deferred_decision_proportional():
    g = GraphTools.deferred_decisions_with_proportional_to_the_degree(load_graph())
    print('After Deferred decision Nodes: %d, Edges: %d' % (g.GetNodes(), g.GetEdges()))
    return g

def uniform_constant():
   g = GraphTools.constant_threshold_assignment(deferred_decision_uniform(), 2)
   s = tpi(g)
   return sol_size(s)

def uniform_proportional():
    g = GraphTools.proportional_to_the_degree_threshold_assignment(deferred_decision_uniform())
    s = tpi(g)
    return sol_size(s)

def uniform_random():
    g = GraphTools.random_threshold_assignment(deferred_decision_uniform())
    s = tpi(g)
    return sol_size(s)

def proportional_constant():
   g = GraphTools.constant_threshold_assignment(deferred_decision_proportional(), 2)
   s = tpi(g)
   return sol_size(s)

def proportional_proportional():
    g = GraphTools.proportional_to_the_degree_threshold_assignment(deferred_decision_proportional())
    s = tpi(g)
    return sol_size(s)

def proportional_random():
    g = GraphTools.random_threshold_assignment(deferred_decision_proportional())
    s = tpi(g)
    return sol_size(s)

def ten_iteration(func):
    size = 0
    incentive = 0
    for i in range(0,10):
        sol = func()
        size = size+sol[0]
        incentive = size+sol[1]
    size = size/10
    incentive = incentive/10
    return size, incentive


def test():
    print("Deferred Decision Uniform - Constant Threshold Assignment")
    ten_iteration(uniform_constant)
    print("Deferred Decision Uniform - Proportional Threshold Assignment")
    ten_iteration(uniform_proportional)
    print("Deferred Decision Uniform - Random Threshold Assignment")
    ten_iteration(uniform_random)
    print("Deferred Decision Proportional - Constant Threshold Assignment")
    ten_iteration(proportional_constant)
    print("Deferred Decision Proportional - Proportional Threshold Assignment")
    ten_iteration(proportional_proportional)
    print("Deferred Decision Proportional - Random Threshold Assignment")
    ten_iteration(proportional_random)
