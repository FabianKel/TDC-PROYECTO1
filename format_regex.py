def convert_extensions(regex):
    new_regex = []
    i = 0
    OrGroup = False
    temp_group = []

    while i < len(regex):
        c = regex[i]
        nextC = regex[i+1] if i+1 < len(regex) else None


        if OrGroup:
            if c == ']':
                p = 0
                temp_result = []
                while p < len(temp_group):
                    if temp_group[p] == '-' and p != 0 and p != len(temp_group) - 1:
                        start, end = temp_group[p-1], temp_group[p+1]
                        # Si es un rango de letras
                        if start.isalpha() and end.isalpha():
                            temp_result.extend(chr(j) for j in range(ord(start), ord(end) + 1))
                        # Si es un rango de números
                        elif start.isdigit() and end.isdigit():
                            temp_result.extend(str(j) for j in range(int(start), int(end) + 1))
                        p += 2  # Saltamos los siguientes 2 caracteres ya que forman el rango
                    else:
                        temp_result.append(temp_group[p])
                    p += 1

                # Agregar el resultado con OR
                new_regex.append('(' + '|'.join(temp_result) +')')

                OrGroup = False
                temp_group = []
            else:
                temp_group.append(c)
            
        else:
            if c == '[':
                OrGroup = True
            elif c == '\\':
                if i + 1 < len(regex):            
                    new_regex.append('(')
                    new_regex.append('\\' + regex[i+1])
                    new_regex.append(')')
                    i += 1
            elif c == '+':
                if new_regex[-1] in '])}':
                    start = len(new_regex) - 1
                    count = 0
                    while start >= 0:
                        if new_regex[start] in ')]}':
                            count += 1
                        elif new_regex[start] in '([{':
                            count -= 1
                        if count == 0:
                            break
                        start -= 1
                    
                    group = ''.join(new_regex[start:])
                    new_regex = new_regex[:start]
                    new_regex.append(group)
                    new_regex.append(group + '*')
                    
            elif c == '?':
                if new_regex:
                    prev_char = new_regex.pop()

                    if prev_char == ')' and new_regex[-2] == '\\':
                        expr = '\\' + new_regex.pop() + prev_char
                        new_regex.pop()
                        new_regex.append('(' + expr + '|ε)')
                    elif prev_char == ')' and new_regex[-1] != '\\':
                        expr = [prev_char]
                        while new_regex and new_regex[-1] != '(':
                            expr.append(new_regex.pop())
                        if new_regex:
                            expr.append(new_regex.pop())
                        expr.reverse()
                        new_regex.append('(' + ''.join(expr) + '|ε)')
                    else:
                        new_regex.append('(' + prev_char + '|ε)')
            else:
                new_regex.append(c)

        i += 1

    formated_regex = ''.join(new_regex)
    concatenated = concatenate(formated_regex)
    return ''.join(concatenated)

def concatenate(regex):
    new_regex = []
    i = 0
    conc = False

    while i < len(regex):
        c = regex[i]
        if c == '\\' and i > 0:
            if conc:
                new_regex.append('•')
                new_regex.append(c)
                new_regex.append(regex[i + 1])
                conc = True
                i += 1
            else:
                new_regex.append(c)
                new_regex.append(regex[i + 1])
                conc = True
                i += 1
            
        elif c in '({[':
            if conc:
                new_regex.append('•')
                new_regex.append(c)
            else:
                new_regex.append(c)
            conc = False
        elif c in ']})':
            new_regex.append(c)
            conc = True
        elif c == '|':
            new_regex.append(c)
            conc = False
        elif c == '*':
            new_regex.append(c)
            conc = True
        else:
            if conc:
                new_regex.append('•')
                new_regex.append(c)
            else:
                new_regex.append(c)
            conc = True
        i += 1

    # Revisión de concatenaciones repetidas
    i = 0
    while i < len(new_regex) - 1:
        if new_regex[i] == '•' and new_regex[i + 1] == '•':
            new_regex.pop(i + 1)
        elif new_regex[i] == '•' and new_regex[i + 1] in ['(', '{', '[', '|', '*', '?'] and new_regex[i + 2] == '•':
            new_regex.pop(i + 2)
        else:
            i += 1

    print_regex = ''.join(new_regex)
    print(f'Expresión Formateada: {print_regex}')
    return ''.join(new_regex)
