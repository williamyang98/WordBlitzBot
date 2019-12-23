import argparse
import os

DICTONARY_DIR = "assets/dictionaries/"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=os.path.join(DICTONARY_DIR, "full_dictionary.txt"))
    parser.add_argument("--output", default=os.path.join(DICTONARY_DIR, "reduced_dictionary.txt"))

    args = parser.parse_args()

    with open(args.input, "r") as in_file, open(args.output, "w") as out_file:
        counter = 0
        for i, word in enumerate(in_file.readlines()):
            word = word.strip().lower()
            if word.isalpha() and len(word) <= 12 and len(word) > 1:
                counter += 1
                out_file.write(word+"\n")
                print(f"{counter}/{i+1} {word}", end="\r")



if __name__ == '__main__':
    main()
