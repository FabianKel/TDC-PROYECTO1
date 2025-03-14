from graphviz import Digraph
from collections import defaultdict

class ThompsonNFA:
    def __init__(self):
        self.dot = Digraph(format='png')
        self.dot.attr(rankdir='LR')
        self.node_count = 0  
        self.transitions = defaultdict(list) 
        
        self.start_node = '0'
        self.dot.node(self.start_node, self.start_node, shape='ellipse')
        
        self.accept_node = None 

    def new_node(self, label=None):
        self.node_count += 1
        node_name = f'{self.node_count}'
        self.dot.node(node_name, label if label else node_name, shape='ellipse')
        return node_name

    def add_transition(self, start, end, symbol):
        self.dot.edge(start, end, label=symbol)
        self.transitions[start].append((symbol, end))

    def add_star(self, start, end):
        start_new = self.new_node()
        end_new = self.new_node()

        self.add_transition(start_new, start, 'ε')
        self.add_transition(end, end_new, 'ε')
        self.add_transition(end, start, 'ε')
        self.add_transition(start_new, end_new, 'ε')

        return start_new, end_new

    def add_concat(self, nfa1, nfa2):
        start1, end1 = nfa1
        start2, end2 = nfa2

        self.add_transition(end1, start2, 'ε')
        return start1, end2

    def add_union(self, nfa1, nfa2):
        start1, end1 = nfa1
        start2, end2 = nfa2

        start_new = self.new_node()
        end_new = self.new_node()

        self.add_transition(start_new, start1, 'ε')
        self.add_transition(start_new, start2, 'ε')
        self.add_transition(end1, end_new, 'ε')
        self.add_transition(end2, end_new, 'ε')

        return start_new, end_new

    def build_from_tree(self, tree):
        if tree.label() == '*':
            start, end = self.add_star(*self.build_from_tree(tree[0]))
        elif tree.label() == '|':
            start, end = self.add_union(self.build_from_tree(tree[0]), self.build_from_tree(tree[1]))
        elif tree.label() == '•':
            start, end = self.add_concat(self.build_from_tree(tree[0]), self.build_from_tree(tree[1]))
        else:  # Nodo hoja
            start = self.new_node()
            end = self.new_node()
            self.add_transition(start, end, tree.label())

        return start, end

    def finalize(self, start, end):
        self.accept_node = f'{self.node_count + 1}'
        self.dot.node(self.accept_node, self.accept_node, shape='doublecircle')

        self.add_transition(self.start_node, start, 'ε')
        self.add_transition(end, self.accept_node, 'ε')

        self.dot.node('start', label='start', shape='plaintext')

        self.dot.edge('start', self.start_node, label='')


    def plot(self, i):
        self.dot.render(f'AFN{i}', cleanup=True)
        print(f"AFN guardada como 'AFN{i}.png'")

    def simulate(self, input_string):
        def epsilon_closure(states):
            stack = list(states)
            closure = set(states)
            while stack:
                state = stack.pop()
                for symbol, next_state in self.transitions[state]:
                    if symbol == 'ε' and next_state not in closure:
                        closure.add(next_state)
                        stack.append(next_state)
            return closure

        def process_state_set(state_set, input_string):
            current_states = epsilon_closure(state_set)
            for symbol in input_string:
                next_states = set()
                for state in current_states:
                    for trans_symbol, next_state in self.transitions[state]:
                        if trans_symbol == symbol:
                            next_states.add(next_state)
                current_states = epsilon_closure(next_states)
            return self.accept_node in current_states

        start_states = epsilon_closure({self.start_node})
        return process_state_set(start_states, input_string)
