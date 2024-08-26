from nltk.tree import Tree

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