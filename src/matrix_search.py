# returns list of tuples
# each tuple contains the word found, and the path to create that word
def search_entire_matrix(matrix, word_tree):
    rows, columns = matrix.shape
    words = []
    for y in range(rows):
        for x in range(columns):
            words.extend(search_matrix(matrix, (x, y), word_tree))
    return words

# returns list of words starting from a specified position in the matrix
def search_matrix(matrix, start_pos, leaf, search_grid=None, path=[]):
    x, y = start_pos
    rows, columns = matrix.shape
    path = path+[start_pos,]
    found_words = []
    
    if x < 0 or x >= columns:
        return found_words
    
    if y < 0 or y >= rows:
        return found_words
    
    if search_grid and search_grid[y][x] is True:
        return found_words

    if not search_grid:
        search_grid = [[False for _ in range(columns)] for _ in range(rows)]
        
    char = matrix[y][x]
    child = leaf.get_leaf(char)
    if not child:
        return found_words
    
    if child.word:
        found_words.append((child.word, path))

    search_grid[y][x] = True
    for x_off in (-1, 0, 1):
        for y_off in (-1, 0, 1):
            if x_off == 0 and y_off == 0:
                continue
            words = search_matrix(matrix, (x+x_off, y+y_off), child, search_grid, path)
            found_words.extend(words)
    
    search_grid[y][x] = False
    return found_words
    
