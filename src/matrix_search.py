# returns list of tuples
# each tuple contains the word found, and the path to create that word
def search_entire_matrix(matrix, dictionary):
    rows, columns = matrix.shape
    words = []
    search_grid = [[False for _ in range(columns)] for _ in range(rows)]
    for y in range(rows):
        for x in range(columns):
            words.extend(search_matrix(matrix, (x, y), dictionary, search_grid=search_grid))
    return words

# returns list of words starting from a specified position in the matrix
def search_matrix(matrix, start_pos, dictionary, search_grid=None, path=[], word=""):
    x, y = start_pos
    rows, columns = matrix.shape
    path = path+[start_pos,]
    
    if x < 0 or x >= columns:
        return []
    
    if y < 0 or y >= rows:
        return []
    
    if search_grid and search_grid[y][x] is True:
        return []

    char = matrix[y][x]
    word = word+char

    if not dictionary.is_branch(word):
        return []

    found_words = []
    if dictionary.is_word(word):
        found_words.append((word, path))
    
    search_grid[y][x] = True
    for x_off in (-1, 0, 1):
        for y_off in (-1, 0, 1):
            if x_off == 0 and y_off == 0:
                continue
            words = search_matrix(matrix, (x+x_off, y+y_off), dictionary, search_grid, path, word)
            found_words.extend(words)
    
    search_grid[y][x] = False
    return found_words
    
