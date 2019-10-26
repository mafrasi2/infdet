import networkx as nx
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

def determinize(T, A, S):
    D = nx.MultiDiGraph()
    init_node = (A.graph["init"], frozenset(
        i, "" if i in S for i in T.graph["init"]
    ))
    D.add_node(init_node)
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
A = nx.DiGraph(init="A")
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

D = determinize(T, A, {1})

trans_create_labels(D)
a = to_agraph(D)
a.layout("dot")
a.draw("T.pdf", format="pdf")
