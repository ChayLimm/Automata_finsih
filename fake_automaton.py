import pygraphviz as pgv
from collections import defaultdict

class FakeAutomaton:
    def __init__(self, states, transitions, start_state, accepting_states):
        self.states = set(states)
        self.transitions = defaultdict(list)
        for from_state, to_state, symbol in transitions:
            self.transitions[(from_state, to_state)].append(symbol)
        self.start_state = start_state
        self.accepting_states = set(accepting_states)
        self.alphabet = set(symbol for _, _, symbol in transitions if symbol)

    def epsilon_closure(self, states):
        stack = list(states)
        closure = set(states)
        while stack:
            state = stack.pop()
            for (from_state, to_state), symbols in self.transitions.items():
                if from_state == state:
                    for symbol in symbols:
                        if symbol == 'ε' and to_state not in closure:
                            closure.add(to_state)
                            stack.append(to_state)
        return closure
    
    def _get_next_state(self, state, symbol):
        for (from_state, to_state), symbols in self.transitions.items():
            if from_state == state and symbol in symbols:
                return to_state
        return None

    def generate_fa_image(self, filename="nfa.png"):
        graph = pgv.AGraph(directed=True)

        # Add states to the graph
        for state in self.states:
            if state in self.accepting_states:
                graph.add_node(state, shape="doublecircle")
            else:
                graph.add_node(state, shape="circle")

        # Add start state indicator
        graph.add_node("start", shape="none", label="")
        graph.add_edge("start", self.start_state)

        # Add transitions to the graph
        for (from_state, to_state), symbols in self.transitions.items():
            combined_label = '/'.join(symbols)
            graph.add_edge(from_state, to_state, label=combined_label)

        # Render and save the graph
        graph.layout(prog="dot")
        graph.draw(filename)

# Example usage:
# states = ['q0', 'q1', 'q2']
# transitions = [
#     ('q0', 'q1', 'A'),
#     ('q0', 'q1', 'B'),
#     ('q1', 'q2', 'C'),
#     ('q2', 'q0', 'D')
# ]
# start_state = 'q0'
# accepting_states = ['q2']

# fa = FakeAutomaton(states, transitions, start_state, accepting_states)
# fa.generate_fa_image("fa_combined.png")
