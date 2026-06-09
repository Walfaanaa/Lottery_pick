from graphviz import Digraph

dot = Digraph("MLOps_Cycle", format="png")

# -------------------------
# Global styling (important for modern look)
# -------------------------
dot.attr(
    rankdir="LR",
    splines="curved",
    bgcolor="#0f172a",   # dark background like your image
    fontname="Helvetica"
)

dot.attr("node",
    shape="circle",
    style="filled",
    fontname="Helvetica",
    fontsize="10",
    color="white"
)

dot.attr("edge",
    color="#94a3b8",
    penwidth="2"
)

# -------------------------
# Nodes (MLOps lifecycle)
# -------------------------
dot.node("A", "Develop", fillcolor="#60a5fa")
dot.node("B", "Data Prep", fillcolor="#93c5fd")
dot.node("C", "EDA", fillcolor="#bfdbfe")
dot.node("D", "(Re-)Train", fillcolor="#3b82f6")
dot.node("E", "Review", fillcolor="#fbbf24")
dot.node("F", "Deploy", fillcolor="#f59e0b")
dot.node("G", "Inference", fillcolor="#f97316")
dot.node("H", "Monitor", fillcolor="#facc15")

# -------------------------
# Circular flow
# -------------------------
dot.edges([
    ("A", "B"),
    ("B", "C"),
    ("C", "D"),
    ("D", "E"),
    ("E", "F"),
    ("F", "G"),
    ("G", "H"),
    ("H", "D")   # loop back (MLOps cycle)
])

# -------------------------
# Render
# -------------------------
dot.render("mlops_cycle", view=True)