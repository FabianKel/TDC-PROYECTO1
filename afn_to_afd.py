from graphviz import Digraph
from collections import defaultdict, deque

class AFNtoAFD:
    def __init__(self, nfa):
        self.nfa = nfa
        self.afd_transitions = defaultdict(dict)
        self.afd_states = {}
        self.state_count = 0
        self.accepting_states = set()

    def epsilon_closure(self, states):
        closure = set(states)
        stack = list(states)
        while stack:
            state = stack.pop()
            for symbol, next_state in self.nfa.transitions[state]:
                if symbol == 'ε' and next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)
        return closure

    def move(self, states, symbol):
        move_set = set()
        for state in states:
            for trans_symbol, next_state in self.nfa.transitions[state]:
                if trans_symbol == symbol:
                    move_set.add(next_state)
        return move_set

    def convert(self):
        start_closure = self.epsilon_closure({self.nfa.start_node})
        start_closure = frozenset(start_closure)
        self.afd_states[start_closure] = f'q{self.state_count}'
        self.state_count += 1

        if self.is_accepting(start_closure):
            self.accepting_states.add(self.afd_states[start_closure])

        queue = deque([start_closure])
        while queue:
            current_closure = queue.popleft()

            for symbol in {sym for state in current_closure for sym, _ in self.nfa.transitions[state] if sym != 'ε'}:
                next_closure = self.epsilon_closure(self.move(current_closure, symbol))
                next_closure = frozenset(next_closure)

                if next_closure not in self.afd_states:
                    self.afd_states[next_closure] = f'q{self.state_count}'
                    self.state_count += 1
                    queue.append(next_closure)

                self.afd_transitions[self.afd_states[current_closure]][symbol] = self.afd_states[next_closure]

                if self.is_accepting(next_closure):
                    self.accepting_states.add(self.afd_states[next_closure])

        return self.afd_transitions, self.afd_states, self.accepting_states

    def is_accepting(self, closure):
        return self.nfa.accept_node in closure

    def print_afd(self):
        for state, transitions in self.afd_transitions.items():
            for symbol, next_state in transitions.items():
                print(f"{state} --{symbol}--> {next_state}")

    def plot_afd(self, filename):
        dot = Digraph(format='png')
        dot.attr(rankdir='LR')
        
        dot.node('start', label='start', shape='plaintext')

        initial_state_name = self.afd_states[frozenset(self.epsilon_closure({self.nfa.start_node}))]
        
        dot.edge('start', initial_state_name, label='')

        for closure, state_name in self.afd_states.items():
            shape = 'doublecircle' if self.is_accepting(closure) else 'ellipse'
            dot.node(state_name, state_name, shape=shape)

        for state, transitions in self.afd_transitions.items():
            for symbol, next_state in transitions.items():
                dot.edge(state, next_state, label=symbol)

        dot.render(filename, cleanup=True)
        print(f"AFD guardado como '{filename}.png'")


    def simulate(self, input_string):
        # Encontrar el estado inicial
        current_state = None
        for closure, state_name in self.afd_states.items():
            if self.nfa.start_node in closure:
                current_state = state_name
                break

        if current_state is None:
            raise ValueError("No se encontró el estado inicial en el AFD.")

        print(f"Estado inicial: {current_state}")
        
        i = 0
        while i < len(input_string):
            # Procesar símbolos, incluyendo los escapados
            if input_string[i] == '\\' and i + 1 < len(input_string):
                symbol = input_string[i] + input_string[i + 1]  # Toma '\|' como un solo símbolo
                i += 2  # Salta dos posiciones
            else:
                symbol = input_string[i]
                i += 1  # Avanza una posición

            print(f"Símbolo procesado: {symbol}, Estado actual: {current_state}")
            
            # Buscar la transición para el símbolo actual
            if symbol in self.afd_transitions[current_state]:
                next_state = self.afd_transitions[current_state][symbol]
                print(f"Transición encontrada: {current_state} --{symbol}--> {next_state}")
                current_state = next_state
            else:
                print(f"No se encontró transición para el símbolo '{symbol}' desde el estado {current_state}.")
                return False  # Si no hay transición, la cadena no es aceptada

        # Verificar si el estado final es de aceptación
        for closure, state_name in self.afd_states.items():
            if state_name == current_state:
                if self.is_accepting(closure):
                    print(f"La cadena es aceptada. Estado final: {current_state}")
                    return True
                else:
                    print(f"La cadena no es aceptada. Estado final: {current_state}")
                    return False

        return False

