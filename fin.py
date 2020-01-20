from util import PeriodicWord, longest_common_prefix, EPSILON

import networkx as nx
import subprocess as sp
import random
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
        final = None
        P_list = []
        if node in T.graph["init"]:
            P_list.append(f"\\leftarrow &,")
        if isinstance(node, frozenset):
            P_list.extend(f"{q}&,{z if z else EPSILON}" for q, z in node)
        else:
            P_list.append(str(node))
        if node in T.graph["final"]:
            final = T.graph["final"][node]
            P_list.append(f"\\rightarrow &{final}")
        P_str = "\\\\".join(P_list)
        attr["texlbl"] = f"$\\begin{{aligned}}{P_str}\\end{{aligned}}$"

def render(T, outf):
    trans_create_labels(T)
    a = to_agraph(T)
    a.write("G.dot")
    sp.check_call(["./render_tex.sh", outf])

def lcp(u, v):
    prefix = ""
    for i in range(min(len(u), len(v))):
        if u[i] == v[i]:
            prefix += u[i]
        else:
            break
    return prefix

def gen_trans(rand, input_alphabet, output_alphabet):
    num_nodes = 3
    num_final = rand.randrange(1,num_nodes+1)
    final = rand.sample(range(num_nodes), num_final)
    T = nx.MultiDiGraph(init={0},final={f: "" for f in final})
    T.add_nodes_from(list(range(num_nodes)))
    for src in range(num_nodes):
        for a in input_alphabet:
            num_edges = rand.randrange(0, 3)
            for _ in range(num_edges):
                dest = rand.randrange(0, num_nodes)
                if T.has_edge(src, dest):
                    continue
                out_len = rand.randrange(0, 3)
                out = "".join(rand.choices(output_alphabet, k=out_len))
                T.add_edge(src, dest, input=a, output=out)
    return T

class Reject(Exception):
    pass

def determinize(T, input_alphabet):
    D = nx.MultiDiGraph()
    init_state = frozenset(
        (i, "") for i in T.graph["init"]
    )
    D.add_node(init_state)
    D.graph["init"] = {init_state}
    D.graph["final"] = {}
    todo = deque([(init_state, a) for a in input_alphabet])
    num_steps = 0
    MAX_STEPS = 20
    non_trivial_final = False
    while todo:
        num_steps += 1
        if num_steps >= MAX_STEPS:
            raise Reject("max steps reached")
        P, a = todo.popleft()
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
                        if final != residual:
                            raise Reject("non subsequential transducer")
                        if len(residual) > 0:
                            non_trivial_final = True
                    else:
                        final = residual
            Pp = frozenset(Pp)
            if Pp not in D.nodes():
                D.add_node(Pp)
                if final is not None:
                    D.graph["final"][Pp] = final
                todo.extend([(Pp, a) for a in input_alphabet])
            D.add_edge(P, Pp, input=a, output=w)
    if not non_trivial_final:
        raise Reject("no nontrivial final reached")
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

rnd = random.Random()
while True:
    try:
        T = gen_trans(rnd, input_alphabet, output_alphabet)
        D = determinize(T, input_alphabet)
        render(T, "T.pdf")
        render(D, "D.pdf")
    except Reject as e:
        print(f"Rejection reason: {str(e)}")
        continue
    input("Press ENTER for the next one...")
#a.layout("dot")
#a.draw("G.pdf", format="pdf")
