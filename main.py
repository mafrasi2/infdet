from util import PeriodicWord, longest_common_prefix

import networkx as nx
from collections import deque
from networkx.drawing.nx_agraph import to_agraph

def trans_create_labels(T):
    for _,_,attr in T.edges(data=True):
        inp = attr["input"]
        out = attr["output"]
        if inp == "":
            inp = "ɛ"
        if out == "":
            out = "ɛ"
        attr["label"] = f"{inp}|{out}"

def compute_R(P, a, T, S):
    s = set()
    for q, z in P:
        for _, qp, attr in T.edges(q, data=True):
            if attr["input"] != a:
                continue
            if qp not in S and q not in S:
                s.add((qp, z + attr["output"]))
            elif qp in S and q not in S:
                s.add((qp, z + attr["output"] + S[qp]))
            elif qp in S and q in S:
                s.add((qp, z))
            else:
                raise ValueError("all states reachable from constant states must be constant, too")
    return frozenset(s)

def find_dba_edge(A, p, a):
    for _, pp, attr in A.edges(p, data=True):
        if a == attr["label"]:
            return pp
    return None

def determinize(T, A, S, input_alphabet):
    D = nx.MultiDiGraph()
    init_state = (A.graph["init"], frozenset(
        (i, S[i]) if i in S else (i, "") for i in T.graph["init"]
    ))
    D.add_node(init_state)

    todo = deque([(init_state, a) for a in input_alphabet])
    while todo:
        (p, P), a = todo.pop()
        pp = find_dba_edge(A, p, a)
        if pp is None:
            continue
        R = compute_R(P, a, T, S)
        if pp not in A.graph["final"]:
            v = ""
        else:
            v = longest_common_prefix([z for _, z in R])
            if isinstance(v, PeriodicWord):
                v = v.expand(1)
        print(R)
        Pp = set()
        for (qp, w) in R:
            if isinstance(w, PeriodicWord):
                z = w.without_prefix(len(v))
            else:
                z = w[len(v):]
            Pp.add((qp, z))
        Pp = frozenset(Pp)
        target_node = (pp, Pp)
        if target_node not in D.nodes():
            D.add_node(target_node)
            todo.extend([(target_node, a) for a in input_alphabet])
        D.add_edge((p, P), target_node, input=a, output=v)
    return D

input_alphabet = "abc"
output_alphabet = "a"
T = nx.MultiDiGraph(init={0})
T.add_nodes_from([0, 1])
T.add_edges_from([
    (0, 0, {"input": "a", "output": "a"}),
    (0, 0, {"input": "b", "output": "b"}),
    (0, 1, {"input": "a", "output": ""}),
    (1, 1, {"input": "a", "output": ""}),
    (1, 1, {"input": "c", "output": "aa"}),
])
A = nx.DiGraph(init="A", final={"A", "B", "C"})
A.add_nodes_from(["A", "B", "C", "D"])
A.add_edges_from([
    ("A", "A", {"label": "b"}),
    ("A", "B", {"label": "a"}),
    ("B", "A", {"label": "b"}),
    ("B", "B", {"label": "a"}),
    ("B", "C", {"label": "c"}),
    ("C", "C", {"label": "c"}),
    ("C", "D", {"label": "a"}),
    ("D", "C", {"label": "c"}),
    ("D", "D", {"label": "a"}),
])

D = determinize(T, A, {1: PeriodicWord("", "a")}, input_alphabet)

trans_create_labels(D)
a = to_agraph(D)
a.layout("dot")
a.draw("T.pdf", format="pdf")
