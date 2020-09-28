import argparse
import pickle

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("words", help="List of words in your dictionary")
    parser.add_argument("--out", default="dictionary.pickle", help="Output path of dictionary (pickled)")
    parser.add_argument("--override", action="store_true", help="Override if it exists")
    
    args = parser.parse_args()

    dictionary = {}

    def add_word(word):
        for i in range(len(word)):
            branch = word[:i]
            dictionary.setdefault(branch, False)
        dictionary[word] = True

    pickle_out = open(args.out, "wb+" if args.override else "wb")

    try:
        with open(args.words, "r") as fp:
            for line in fp.readlines():
                word = line.strip('\n')
                word = word.strip()
                add_word(word)
    finally:
        pickle.dump(dictionary, pickle_out, pickle.HIGHEST_PROTOCOL)
        pickle_out.close()

if __name__ == '__main__':
    main()