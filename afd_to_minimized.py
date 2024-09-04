from collections import defaultdict
from graphviz import Digraph

class AFDMinimizer:
    def __init__(self, afd_transitions, afd_states, afd_accepting_states):
        self.afd_transitions = afd_transitions
        self.afd_states = afd_states
        self.afd_accepting_states = afd_accepting_states
        self.initial_state = None

    def minimize(self):
        accepting_states = set(self.afd_accepting_states)
        non_accepting_states = set(self.afd_states.values()) - accepting_states

        partitions = [non_accepting_states, accepting_states] if non_accepting_states else [accepting_states]

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
                    key = tuple(
                        frozenset(get_state_class(self.afd_transitions[state][symbol]))
                        if symbol in self.afd_transitions[state] else None
                        for symbol in self.afd_transitions[state].keys()
                    )
                    split_partitions[key].add(state)
                
                new_partitions.extend(split_partitions.values())
            
            if len(new_partitions) == len(partitions):
                break
            partitions = new_partitions

        old_initial_state = list(self.afd_states.values())[0]  
        new_transitions = defaultdict(dict)
        new_states = {}
        new_accepting_states = set()

        for idx, partition in enumerate(partitions):
            new_state = f'q{idx}'
            for old_state in partition:
                new_states[old_state] = new_state
                if old_state in accepting_states:
                    new_accepting_states.add(new_state)
                if old_state == old_initial_state:
                    self.initial_state = new_state

        print(f"Estado inicial después de la minimización: {self.initial_state}")

        for old_state, transitions in self.afd_transitions.items():
            for symbol, next_state in transitions.items():
                new_transitions[new_states[old_state]][symbol] = new_states[next_state]
                #print(f"Transición: {new_states[old_state]} --{symbol}--> {new_states[next_state]}")

        self.afd_transitions = new_transitions
        self.afd_states = {frozenset(states): new_states[list(states)[0]] for states in partitions}
        self.afd_accepting_states = new_accepting_states

        print(f"Estados de aceptación en el AFD minimizado: {self.afd_accepting_states}")

    def plot_minimized_afd(self, filename):
        dot = Digraph(format='png')
        dot.attr(rankdir='LR')
        for state_name in self.afd_states.values():
            shape = 'doublecircle' if state_name in self.afd_accepting_states else 'ellipse'
            dot.node(state_name, state_name, shape=shape)

        start_state = self.initial_state
        dot.node('start', '', shape='none', width='0', height='0')
        dot.edge('start', start_state, label='start')

        for state, transitions in self.afd_transitions.items():
            for symbol, next_state in transitions.items():
                dot.edge(state, next_state, label=symbol)

        dot.render(filename, cleanup=True)
        print(f"AFD Minimizado guardado como '{filename}.png'")

    def simulate(self, input_string):
        current_state = self.initial_state
        ##print(f"Iniciando simulación en el estado: {current_state}")  

        for symbol in input_string:
            if symbol in self.afd_transitions[current_state]:
                current_state = self.afd_transitions[current_state][symbol]
                ##print(f"Transición: {symbol} --> {current_state}")  
            else:
                return False  
        return current_state in self.afd_accepting_states
