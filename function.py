import pygraphviz as pgv
from collections import defaultdict, deque

class FiniteAutomaton:
    def __init__(self, states, transitions, start_state, accepting_states):
        self.states = set(states)
        self.transitions = defaultdict(list)
        for from_state, to_state, symbol in transitions:
            self.transitions[from_state].append((symbol, to_state))
        self.start_state = start_state
        self.accepting_states = set(accepting_states)
        self.alphabet = set(symbol for _, _, symbol in transitions if symbol)

    def is_deterministic(self):
        transition_dict = defaultdict(dict)
        for from_state in self.transitions:
            for symbol, to_state in self.transitions[from_state]:
                if symbol in transition_dict[from_state]:
                    return False
                transition_dict[from_state][symbol] = to_state
        return True

    def accepts_string(self, string):
        current_states = self.epsilon_closure({self.start_state})
        for symbol in string:
            next_states = set()
            for state in current_states:
                if state in self.transitions:
                    for trans_symbol, to_state in self.transitions[state]:
                        if trans_symbol == symbol:
                            next_states.update(self.epsilon_closure({to_state}))
            current_states = next_states
        return bool(current_states & self.accepting_states)


    def epsilon_closure(self, states):
        stack = list(states)
        closure = set(states)
        while stack:
            state = stack.pop()
            if state in self.transitions:
                for symbol, to_state in self.transitions[state]:
                    if symbol == 'ε' and to_state not in closure:
                        closure.add(to_state)
                        stack.append(to_state)
        return closure

    def convert_to_dfa(self):
        dfa_states = {}
        dfa_transitions = []
        dfa_start_state = frozenset(self.epsilon_closure({self.start_state}))
        dfa_states[dfa_start_state] = 'q0'
        unmarked_states = deque([dfa_start_state])
        dfa_accepting_states = set()

        state_count = 1
        while unmarked_states:
            current = unmarked_states.popleft()
            current_name = dfa_states[current]

            if current & self.accepting_states:
                dfa_accepting_states.add(current_name)

            for symbol in self.alphabet:
                if symbol == 'ε':
                    continue
                next_state = frozenset(self.epsilon_closure(
                    {to_state for from_state in current if from_state in self.transitions for trans_symbol, to_state in self.transitions[from_state] if trans_symbol == symbol}
                ))
                if not next_state:
                    continue

                if next_state not in dfa_states:
                    dfa_states[next_state] = f'q{state_count}'
                    state_count += 1
                    unmarked_states.append(next_state)

                dfa_transitions.append((current_name, dfa_states[next_state], symbol))

        return FiniteAutomaton(list(dfa_states.values()), dfa_transitions, 'q0', dfa_accepting_states)

    def minimize_dfa(self):
        if not self.is_deterministic():
            raise ValueError("The automaton is not deterministic and cannot be minimized.")

        partition = [self.accepting_states, self.states - self.accepting_states]
        new_partition = []
        while True:
            for group in partition:
                if len(group) == 1:
                    new_partition.append(group)
                    continue

                rep = next(iter(group))
                same = {rep}
                diff = set()
                for state in group:
                    if state == rep:
                        continue
                    if all(
                        any(
                            (self._get_next_state(rep, symbol) in sub_group) == (self._get_next_state(state, symbol) in sub_group)
                            for sub_group in partition
                        )
                        for symbol in self.alphabet
                    ):
                        same.add(state)
                    else:
                        diff.add(state)
                new_partition.append(same)
                if diff:
                    new_partition.append(diff)
            if partition == new_partition:
                break
            partition, new_partition = new_partition, []

        state_mapping = {frozenset(group): f'q{index}' for index, group in enumerate(partition)}
        new_start_state = state_mapping[next(frozenset(group) for group in partition if self.start_state in group)]
        new_accepting_states = {state_mapping[frozenset(group)] for group in partition if group & self.accepting_states}

        new_transitions = []
        for group in partition:
            rep = next(iter(group))
            for symbol in self.alphabet:
                next_state = self._get_next_state(rep, symbol)
                if next_state:
                    next_group = next(frozenset(group) for group in partition if next_state in group)
                    new_transitions.append(
                        (state_mapping[frozenset(group)], state_mapping[next_group], symbol)
                    )

        return FiniteAutomaton(list(state_mapping.values()), new_transitions, new_start_state, new_accepting_states)


    def _get_next_state(self, state, symbol):
        if state in self.transitions:
            for trans_symbol, to_state in self.transitions[state]:
                if trans_symbol == symbol:
                    return to_state
        return None

    def generate_fa_image(self, filename="fa.png"):
        graph = pgv.AGraph(directed=True)

        for state in self.states:
            if state in self.accepting_states:
                graph.add_node(state, shape="doublecircle")
            else:
                graph.add_node(state, shape="circle")

        graph.add_node("start", shape="none", label="")
        graph.add_edge("start", self.start_state)

        for from_state in self.transitions:
            for symbol, to_state in self.transitions[from_state]:
                graph.add_edge(from_state, to_state, label=symbol if symbol else "ε")

        graph.layout(prog="dot")
        graph.draw(filename)


# # Example usage
# states = ['q0', 'q1', 'q2']
# transitions = [
#     ('q0', 'q0', 'a'),
#     ('q0', 'q1', 'a'),
#     ('q0', 'q0', 'b'),
#     ('q1', 'q2', 'b'),
#     ('q2', 'q3', 'b'),
#     ('q3', 'q3', 'a'),
#     ('q3', 'q3', 'b')
#     # ('q0', 'q1', 'a'),
#     # ('q0', 'q2', 'b')
    
    
# ]
# start_state = 'q0'
# accepting_states = ['q2']

# fa = FiniteAutomaton(states, transitions, start_state, accepting_states)

# # Generate FA image
# fa.generate_fa_image("fa.png")

# # Check if FA is deterministic
# print(fa.is_deterministic())

# # Check if FA accepts a string
# print(fa.accepts_string("aabbb"))

# # Convert NFA to DFA
# dfa = fa.convert_to_dfa()
# dfa.generate_fa_image("dfa.png")

# # Minimize DFA
# minimized_dfa = dfa.minimize_dfa()
# minimized_dfa.generate_fa_image("minimized_dfa.png")
