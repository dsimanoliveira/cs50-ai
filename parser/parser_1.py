import nltk
import sys
import re

nltk.download('punkt')

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
    S -> NP VP | NP VP Conj NP VP | NP VP Conj VP NP
    NP -> N | Det N | P NP | Det AdjP N | N Adv | P Det N Adv | P Det N
    VP -> V | V NP | V NP NP | V NP NP NP | V Adv
    AdjP -> Adj | Adj Adj | Adj Adj Adj
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    list_of_words = nltk.tokenize.word_tokenize(sentence.lower())

    list_of_words = [word for word in list_of_words if has_alphabetic(word)]

    return list_of_words



    
def has_alphabetic(string):
    """
    Return True if string has at least one alphabetic character.
    Return False otherwise.
    """
    return bool(re.search('[a-zA-Z]', string))


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.   
    """
    all_np = []
    delete_np = []

    for sub_tree in tree.subtrees():
        if sub_tree.label() == "NP":
            all_np.append(sub_tree)

    for i in all_np:
        for j in all_np:
            if i == j:
                continue

            if is_substring(i.leaves(), j.leaves()):
                delete_np.append(j)
        
    return [x for x in all_np if x not in delete_np]


def is_substring(a, b):
    """
    Return True if the list of words a is a sublist of b. False otherwise.
    """
    string_a = " ".join(a)
    string_b = " ".join(b)

    return string_a in string_b
    


if __name__ == "__main__":
    main()
