import os
import argparse
import numpy as np


from src.matrix_search import search_entire_matrix
from src.util import load_tree



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dictionary", default="assets/dictionaries/compact_dictionary.txt")

    args = parser.parse_args()


    matrix = [
        "o e x m",
        "e o h x",
        "k n s i",
        "i t c c"
    ]
    matrix = np.array([row.split(" ") for row in matrix])

    rows = len(matrix)
    columns = len(matrix[0])

    word_tree = load_tree(args.dictionary)

    words = search_entire_matrix(matrix, word_tree)
    print(words)
    



if __name__ == '__main__':
    main()
