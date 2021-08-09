def count_lines(filepath):
    '''Only used to calculate max results for progress bar.'''
    with open(filepath, 'r', encoding='utf-16-le') as f:
        return len(f.readlines())