from nltk.tree import Tree
from thompson_nfa import ThompsonNFA
from infix2postfix import infix_to_postfix
from tree import postfix_to_tree

def postfix_to_tree(postfix):
    stack = []
    for char in postfix:
        if char.isalnum() or char in '.@':
            stack.append(Tree(char, []))
        elif char in '*|•':
            if char == '*':
                operand = stack.pop()
                stack.append(Tree('*', [operand]))
            elif char in '•|':
                right = stack.pop()
                left = stack.pop()
                stack.append(Tree(char, [left, right]))
    return stack[0]

def process_file(filename, test_string):
    afns = []  # Almacena los AFN generados

    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    i = 1
    for line in lines:
        line = line.strip()
        print(f'Procesando: {line}')
        postfix = infix_to_postfix(line)
        print(f'Expresion postfix: {postfix}')
        arbol = postfix_to_tree(postfix)
        arbol.draw()
        
        nfa = ThompsonNFA()
        start, end = nfa.build_from_tree(arbol)
        nfa.finalize(start, end)  
        nfa.plot(str(i))
        afns.append(nfa) 
        
        print('-' * 50)
        i += 1

    for idx, nfa in enumerate(afns):
        if nfa.simulate(test_string):
            print(f"La cadena '{test_string}' SI es aceptada por el AFN {idx + 1}.")
        else:
            print(f"La cadena '{test_string}' NO es aceptada por el AFN {idx + 1}.")
