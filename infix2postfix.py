from format_regex import convert_extensions

def get_precedence(c):
    precedences = {'(': 1, '[': 1, '{':1, '|': 2, '•': 3, '?': 4, '*': 4, '+': 4, '^': 5}
    return precedences.get(c, 6)  # Los operadores no listados tienen la mayor precedencia


def infix_to_postfix(regex):
    postfix = []
    stack = []
    converted_regex = convert_extensions(regex)
    
    for i in range(len(converted_regex)):
        c = converted_regex[i]
        if c.isalnum() or c == 'ε' or c == '.':
            postfix.append(c)
            #print(f'Output: {c} -> Postfix: {"".join(postfix)}, Stack: {stack}')

        elif c == '\\':
            if converted_regex[i+1] in '([{)]}':
                postfix.append(converted_regex[i+1])
            if converted_regex[i+1] == 'n':
                postfix.append('\\')

        elif c in '([{':
            stack.append(c)
            #print(f'Push: {c} -> Postfix: {"".join(postfix)}, Stack: {stack}')
        elif c in ')]}':
            opening = '(' if c == ')' else '[' if c == ']' else '{' if c == '}' else None
            while stack and stack[-1] != opening:
                postfix.append(stack.pop())
                #print(f'Pop: {c} -> Postfix: {"".join(postfix)}, Stack: {stack}')
            stack.pop()  
            #print(f'Pop: {opening} -> Postfix: {"".join(postfix)}, Stack: {stack}')
        else:
            while stack and get_precedence(stack[-1]) >= get_precedence(c):
                postfix.append(stack.pop())
                #print(f'Pop: {c} -> Postfix: {"".join(postfix)}, Stack: {stack}')
            stack.append(c)
            #print(f'Push: {c} -> Postfix: {"".join(postfix)}, Stack: {stack}')
    
    while stack:
        postfix.append(stack.pop())
        #print(f'Pop all -> Postfix: {"".join(postfix)}, Stack: {stack}')
    
    return ''.join(postfix)
