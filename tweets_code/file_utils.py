def count_lines(filepath):
    '''Only used to calculate max results for progress bar.'''
    with open(filepath, 'r', encoding='utf-16-le') as f:
        return len(f.readlines())

def handle_identifiers(line):
    # A bit of a hacky fix, but this handles leading BOM bytes in some tweets
    i = 0
    while True:
        try:
            return eval(eval(line[i:]))
        except SyntaxError: # unexpected char in identifier
            i += 1