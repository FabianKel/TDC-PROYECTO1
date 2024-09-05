from nltk.tree import Tree

def postfix_to_tree(postfix):
    stack = []
    i = 0

    while i < len(postfix):
        char = postfix[i]

        if char == '\\' and i + 1 < len(postfix):
            escaped_char = postfix[i+1]
            
            stack.append(Tree(f'\\{escaped_char}', []))
            i += 1 

        elif char == '*':
            if stack:
                operand = stack.pop()
                stack.append(Tree('*', [operand]))

        elif char in '•|':
            if len(stack) >= 2:
                right = stack.pop()
                left = stack.pop()
                stack.append(Tree(char, [left, right]))

        else: 
            stack.append(Tree(char, []))

        i += 1

    if len(stack) != 1:
        raise ValueError("Error en la construcción del árbol: la pila no tiene exactamente un árbol al final.")
    
    print('------------------------------------------------')
    print(f'ARBOL FINAL')
    print('------------------------------------------------')
    return stack[0]

