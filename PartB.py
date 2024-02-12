import sys
from PartA import tokenize, computeWordFrequencies

# O(n+m) time complexity with n = the number of tokens in the input file1 and m = the number of tokes in the input file2.
# Our tokenize() function is also linear time and converting it to a set is also linear time, so the first two lines of the function are O(n) and O(m)
# We iterate through the tokens of file1, and check to see if it is in the set of file2 tokens which has an O(1) lookup, so the for-loop is O(n)
def intersection(file1, file2):
    file1_tokens = set(tokenize(file1)) 
    file2_tokens = set(tokenize(file2))

    count = 0
    for token in file1_tokens:
        # O(1) set lookup
        if token in file2_tokens:
            count += 1
    return count


if __name__ == "__main__":
    file1, file2 = sys.argv[1], sys.argv[2]
    print(intersection(file1, file2))