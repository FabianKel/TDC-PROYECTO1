from collections import defaultdict, deque
from graphviz import Digraph

class AFDMinimizer:
    def __init__(self, afd_transitions, afd_states, nfa_accept_node):
        self.afd_transitions = afd_transitions
        self.afd_states = afd_states
        self.nfa_accept_node = nfa_accept_node

    def minimize(self):
        accepting_states = set()
        non_accepting_states = set()

        for closure in self.afd_states:
            if self.nfa_accept_node in closure:
                accepting_states.add(self.afd_states[closure])
            else:
                non_accepting_states.add(self.afd_states[closure])

        partitions = [non_accepting_states, accepting_states]

        def get_state_class(state):
            for partition in partitions:
                if state in partition:
                    return partition
            return None

        while True:
            new_partitions = []
            for partition in partitions:
                split_partitions = defaultdict(set)
                for state in partition:
                    key = tuple(frozenset(get_state_class(self.afd_transitions[state][symbol])) 
                                if symbol in self.afd_transitions[state] else None 
                                for symbol in self.afd_transitions[state].keys())
                    split_partitions[key].add(state)
                
                new_partitions.extend(split_partitions.values())
            
            if len(new_partitions) == len(partitions):
                break
            partitions = new_partitions

        new_transitions = defaultdict(dict)
        new_states = {}

        for idx, partition in enumerate(partitions):
            new_state = f'q{idx}'
            for old_state in partition:
                new_states[old_state] = new_state

        for old_state, transitions in self.afd_transitions.items():
            for symbol, next_state in transitions.items():
                new_transitions[new_states[old_state]][symbol] = new_states[next_state]

        self.afd_transitions = new_transitions
        print(partitions)
        for states in partitions:
            if states:
                self.afd_states = {frozenset(states): new_states[list(states)[0]]}

    def plot_minimized_afd(self, filename):
        dot = Digraph(format='png')
        dot.attr(rankdir='LR')
        for closure, state_name in self.afd_states.items():
            shape = 'doublecircle' if self.nfa_accept_node in closure else 'ellipse'
            dot.node(state_name, state_name, shape=shape)

        for state, transitions in self.afd_transitions.items():
            for symbol, next_state in transitions.items():
                dot.edge(state, next_state, label=symbol)

        dot.render(filename, cleanup=True)
        print(f"AFD Minimizado guardado como '{filename}.png'")

