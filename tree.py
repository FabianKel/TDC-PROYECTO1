from nltk.tree import Tree

def postfix_to_tree(postfix):
    stack = []
    for i in range(len(postfix)):
        char = postfix[i]

        if char.isalnum() or char in '.@':
            stack.append(Tree(char, []))
        elif char in '\\':
            stack.append(Tree(postfix[i+1], []))
            continue


        elif char in '*|•':
            if char == '*':
                operand = stack.pop()
                stack.append(Tree('*', [operand]))
            
            elif char in '•|':
                right = stack.pop()
                left = stack.pop()
                stack.append(Tree(char, [left, right]))
    print('------------------------------------------------')
    print(f'ARBOL FINAL {stack}')
    print('------------------------------------------------')
    return stack[0]