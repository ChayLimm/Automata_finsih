import pygraphviz as pgv

# Initialize a dictionary to store transitions
transitions = {}

# Function to add a transition
def add_transition(state, tostate, symbol):
    if (state, tostate) in transitions:
        transitions[(state, tostate)].append(symbol)
    else:
        transitions[(state, tostate)] = [symbol]

# Collect transitions (example user inputs)
add_transition('q0', 'q1', 'A')
add_transition('q0', 'q1', 'B')
add_transition('q1', 'q2', 'C')
add_transition('q2', 'q0', 'D')

# Create a new directed graph
G = pgv.AGraph(directed=True)

# Add states to the graph
states = set()
for (state, tostate) in transitions:
    states.add(state)
    states.add(tostate)

for state in states:
    G.add_node(state)

# Add transitions to the graph with combined labels
for (state, tostate), symbols in transitions.items():
    combined_label = '/'.join(symbols)
    G.add_edge(state, tostate, label=combined_label)

# Render and view the graph
G.layout(prog='dot')
G.draw('fsm_combined.png')
