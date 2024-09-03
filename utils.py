import os
from nltk.tree import Tree
from thompson_nfa import ThompsonNFA
from infix2postfix import infix_to_postfix
from tree import postfix_to_tree
from afn_to_afd import AFNtoAFD
from afd_to_minimized import AFDMinimizer 

def process_file(filename, test_string):
    afns = []
    afds = []
    minimized_afds = []

    # Crear directorios si no existen
    afn_directory = "AFNs"
    afd_directory = "AFDs"
    
    if not os.path.exists(afn_directory):
        os.makedirs(afn_directory)
    
    if not os.path.exists(afd_directory):
        os.makedirs(afd_directory)

    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    i = 1
    for line in lines:
        line = line.strip()
        print(f'Procesando: {line}')
        postfix = infix_to_postfix(line)
        print(f'Expresion postfix: {postfix}')
        arbol = postfix_to_tree(postfix)
        #arbol.draw()
        
        # Construir el AFN usando Thompson
        nfa = ThompsonNFA()
        start, end = nfa.build_from_tree(arbol)
        nfa.finalize(start, end) 
        afn_path = os.path.join(afn_directory, f'AFN_{i}')
        nfa.plot(afn_path)  
        #nfa.plot(str(i))
        afns.append(nfa) 

        # Convertir el AFN a un AFD
        afd = AFNtoAFD(nfa)
        afd_transitions, afd_states, afd_accepting_states = afd.convert()
        afds.append(afd)  # Agregar el AFD a la lista
        afd.print_afd()
        afd_path = os.path.join(afd_directory, f'AFD_{i}')
        afd.plot_afd(afd_path)
        #afd.plot_afd(f'AFD{i}')

        # Minimizar el AFD 
        minimizer = AFDMinimizer(afd_transitions, afd_states, afd_accepting_states)
        minimizer.minimize()
        minimized_afds.append(minimizer)
        minimized_afd_path = os.path.join(afd_directory, f'AFD_minimizado_{i}')
        minimizer.plot_minimized_afd(minimized_afd_path)

        print('-' * 50)
        i += 1

    # Verificar la cadena de prueba tanto en los AFN como en los AFD
    for idx, (nfa, afd) in enumerate(zip(afns, afds)):
        nfa_result = nfa.simulate(test_string)
        afd_result = afd.simulate(test_string)
        
        print(f"La cadena '{test_string}' {'SI' if nfa_result else 'NO'} es aceptada por el AFN {idx + 1}")
        print(f"La cadena '{test_string}' {'SI' if afd_result else 'NO'} es aceptada por el AFD {idx + 1}")
