import numpy as np
from .SolveResult import SolveResult

# Generates list of best words 
class Solver:
    def __init__(self, dictionary):
        self.dictionary = dictionary
        self.length_mapping = {
            2: 3,
            3: 4, 
            4: 6, 
            5: 9, 
            6: 11, 
            7: 14, 
        }

        self.default_scaling = 2

    def calculate_results(self, matrix):
        paths = self.calculate_paths(matrix.get_characters())

        path_table = {}
        for word, path in paths:
            score = self.calculate_score(matrix, path)
            result = SolveResult(word, path, score)

            other_result = path_table.get(word, None)
            if not other_result or result > other_result:
                path_table[word] = result
        
        results = path_table.values()
        results = sorted(results, reverse=True)

        return results

    def calculate_score(self, matrix, path):
        # score = sum(values)*product(word_multiplier) + length_score
        multiplier = 1
        product_sum = 0
        length = len(path)

        length_score = self.length_mapping.get(length, length*self.default_scaling)

        for position in path:
            cell = matrix.get_cell(position)
            product_sum += cell.value
            if cell.bonus == '3W':
                multiplier *= 3
            elif cell.bonus == '2W':
                multiplier *= 2
        
        score = (product_sum * multiplier) + length_score

        return score

    # paths are a list of (word, path)  
    def calculate_paths(self, characters):
        paths = []

        search_grid = np.full(characters.shape, None)
        for index in np.ndindex(characters.shape):
            sub_paths = self.calculate_paths_at_index(characters, index, search_grid, )
            paths.extend(sub_paths)

        return paths

    def calculate_paths_at_index(self, characters, position, search_grid, prev_path=[], prev_word=""):
        paths = []
        
        # check solution (IndexError doesnt work since negative values wrap around)
        y, x = position
        if x < 0 or x >= characters.shape[1]:
            return paths

        if y < 0 or y >= characters.shape[0]:
            return paths

        # if already searched
        already_searched = search_grid[position]
        if already_searched:
            return paths

        # check if branch or word            
        char = characters[position].lower()
        word = prev_word+char            
        if not self.dictionary.is_branch(word):
            return paths

        path = prev_path+[position,]
        # register if it is a word
        if self.dictionary.is_word(word):
            paths.append((word, path))

        # search neighbours
        search_grid[position] = True

        for x_off in (-1, 0, 1):
            for y_off in (-1, 0, 1):
                if x_off == 0 and y_off == 0:
                    continue
                next_position = (y+y_off, x+x_off)
                sub_paths = self.calculate_paths_at_index(characters, next_position, search_grid, path, word)
                paths.extend(sub_paths)

        search_grid[position] = False            

        return paths
        
        

