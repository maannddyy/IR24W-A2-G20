import re
import sys

# O(n) linear time complexity, with n = size of input file; since we are iterating through the file once to read it and then once more to find the regular expression
def tokenize(file_name):
    file = open(file_name, "r")
    content = file.read()

    tokens = re.findall(r'[a-z0-9]+', content.lower())

    file.close()
    return tokens

# O(n) linear time complexity, with n = size of input list of tokens; since we are iterating through our list of tokens once
def computeWordFrequencies(tokens):
    frequencies = dict()

    for token in tokens:
        frequencies[token] = frequencies.get(token, 0) + 1

    return frequencies

# O(n log n) time complexity, with n = number of unique tokens; since we are using python's built-in sort function, the time complexity is O(n)
def printFrequencies(frequencies):
    frequencies_list = [(-v,k) for k,v in frequencies.items()] # O(n)

    frequencies_list.sort() # sorting is O(n log n)

    for token in frequencies_list:
        print(token[1], -token[0])
    

if __name__ == '__main__':
    tokens = tokenize(sys.argv[1])
    frequencies = computeWordFrequencies(tokens)
    printFrequencies(frequencies)