from util import PeriodicWord, longest_common_prefix, EPSILON

import networkx as nx
import subprocess as sp
from collections import deque
from networkx.drawing.nx_agraph import to_agraph
from pprint import pprint

def trans_create_labels(T):
    for _,_,attr in T.edges(data=True):
        inp = attr["input"]
        out = attr["output"]
        if inp == "":
            inp = EPSILON
        if out == "":
            out = EPSILON
        attr["texlbl"] = f"${inp},{out}$"
    for node, attr in T.nodes(data=True):
        if isinstance(node, frozenset):
            P_str = "\\\\".join(f"{q},{z if z else EPSILON}" for q, z in node)
            attr["texlbl"] = f"$\\begin{{aligned}}{P_str}\\end{{aligned}}$"

def render(T):
    trans_create_labels(T)
    a = to_agraph(T)
    a.write("G.dot")
    sp.check_call(["./render_tex.sh"])

def lcp(u, v):
    prefix = ""
    for i in range(min(len(u), len(v))):
        if u[i] == v[i]:
            prefix += u[i]
        else:
            break
    return prefix

def determinize(T, input_alphabet):
    D = nx.MultiDiGraph()
    init_state = frozenset(
        (i, "") for i in T.graph["init"]
    )
    D.add_node(init_state)
    D.graph["init"] = {init_state}
    D.graph["final"] = {}
    todo = deque([(init_state, a) for a in input_alphabet])
    while todo:
        P, a = todo.popleft()
        print(f"edges for symbol {a}:")
        R = set()
        w = None
        #render(D)
        #import pdb; pdb.set_trace()
        for (p, u) in P:
            for _, q, attr in T.edges(p, data=True):
                if attr["input"] != a:
                    continue
                conc = u + attr["output"]
                if w is None:
                    w = conc
                else:
                    w = lcp(w, conc)
                R.add((q, conc))
        if w is not None:
            assert R
            Pp = set()
            final = None
            for q, u in R:
                residual = u[len(w):]
                Pp.add((q, residual))
                if q in T.graph["final"]:
                    if final is not None:
                        assert final == residual
                    else:
                        final = residual
            Pp = frozenset(Pp)
            pprint(Pp)
            if Pp not in D.nodes():
                D.add_node(Pp)
                if final is not None:
                    D.graph["final"][Pp] = final
                todo.extend([(Pp, a) for a in input_alphabet])
            D.add_edge(P, Pp, input=a, output=w)
    return D

input_alphabet = "ab"
output_alphabet = "a"
T = nx.MultiDiGraph(init={0},final={4:"",5:""})
T.add_nodes_from([0,1,2,3,4,5])
T.add_edges_from([
    (0, 1, {"input": "a", "output": "b"}),
    (0, 2, {"input": "a", "output": "ba"}),
    (0, 3, {"input": "a", "output": "ba"}),
    (1, 2, {"input": "a", "output": ""}),
    (2, 1, {"input": "a", "output": ""}),
    (2, 5, {"input": "b", "output": "ac"}),
    (3, 4, {"input": "a", "output": ""}),
    (4, 3, {"input": "a", "output": ""}),
    (5, 5, {"input": "a", "output": "a"}),
])

D = determinize(T, input_alphabet)

render(D)
#a.layout("dot")
#a.draw("G.pdf", format="pdf")
