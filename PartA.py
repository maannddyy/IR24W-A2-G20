import re
import sys

STOP_WORDS = {"a","about","above","after","again","against","all","am","an","and","any","are","aren't","as","at","be","because","been","before","being","below","between","both","but","by","can't","cannot","could","couldn't","did","didn't","do","does","doesn't","doing","don't","down","during","each","few","for","from","further","had","hadn't","has","hasn't","have","haven't","having","he","he'd","he'll","he's","her","here","here's","hers","herself","him","himself","his","how","how's","i","i'd","i'll","i'm","i've","if","in","into","is","isn't","it","it's","its","itself","let's","me","more","most","mustn't","my","myself","no","nor","not","of","off","on","once","only","or","other","ought","our","ours","ourselves","out","over","own","same","shan't","she","she'd","she'll","she's","should","shouldn't","so","some","such","than","that","that's","the","their","theirs","them","themselves","then","there","there's","these","they","they'd","they'll","they're","they've","this","those","through","to","too","under","until","up","very","was","wasn't","we","we'd","we'll","we're","we've","were","weren't","what","what's","when","when's","where","where's","which","while","who","who's","whom","why","why's","with","won't","would","wouldn't","you","you'd","you'll","you're","you've","your","yours","yourself","yourselves"}

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
        if token not in STOP_WORDS:
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