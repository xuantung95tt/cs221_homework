import collections

############################################################
# Problem 3a

def computeMaxWordLength(text):
    """
    Given a string |text|, return the longest word in |text|.  If there are
    ties, choose the word that comes latest in the alphabet.
    A word is defined by a maximal sequence of characters without whitespaces.
    You might find max() and list comprehensions handy here.
    """
    # BEGIN_YOUR_CODE (around 1 line of code expected)
    lengths = [len(k) for k in text.split()]
    return max([m for m in text.split() if len(m) == max(lengths)])
    # END_YOUR_CODE

############################################################
# Problem 3b

def manhattanDistance(loc1, loc2):
    """
    Return the Manhattan distance between two locations, where the locations
    are pairs of numbers (e.g., (3, 5)).
    """
    # BEGIN_YOUR_CODE (around 1 line of code expected)
    return sum([abs(loc1[i] - loc2[i]) for i in range(0,2)])
    # END_YOUR_CODE

############################################################
# Problem 3c

def mutateSentences(sentence):
    """
    High-level idea: generate sentences similar to a given sentence.
    Given a sentence (sequence of words), return a list of all possible
    alternative sentences of the same length, where each pair of adjacent words
    also occurs in the original sentence.  Notes:
    - The order of the sentences you output doesn't matter.
    - You must not output duplicates.
    - Your generated sentence can use a word in the original sentence more than
      once.
    """
    # BEGIN_YOUR_CODE (around 20 lines of code expected)
    wordlist = sentence.split()
    wordadlist = {}
    for i in range(0, len(wordlist)-1):
        word = wordlist[i]
        if word not in wordadlist:
            wordadlist[word] = set()
        wordadlist[word].add(wordlist[i+1])

    new_sentences = [[w] for w in wordadlist]
    for i in range(1, len(wordlist)):
        next_sentences = []
        for sent in new_sentences:
            last_word = sent[-1]
            if last_word in wordadlist:
                for next_word in wordadlist[last_word]:
                    nsent = sent + [next_word]
                    next_sentences.append(nsent)
            else:
                next
        new_sentences = next_sentences

    return [ ' '.join(sent) for sent in new_sentences ]
    # END_YOUR_CODE

############################################################
# Problem 3d

def sparseVectorDotProduct(v1, v2):
    """
    Given two sparse vectors |v1| and |v2|, each represented as Counters, return
    their dot product.
    You might find it useful to use sum() and a list comprehension.
    This function will be useful later for linear classifiers.
    """
    # BEGIN_YOUR_CODE (around 5 lines of code expected)
    return sum([v1[m] * v2[m] for m in list(v1)])
    # END_YOUR_CODE

############################################################
# Problem 3e

def incrementSparseVector(v1, scale, v2):
    """
    Given two sparse vectors |v1| and |v2|, perform v1 += scale * v2.
    This function will be useful later for linear classifiers.
    """
    # BEGIN_YOUR_CODE (around 2 lines of code expected)
    v2_new = collections.Counter({b: v2[b]*scale for b in list(v2)})
    v1.update(v2_new)
    # END_YOUR_CODE

############################################################
# Problem 3f

def computeMostFrequentWord(text):
    """
    Splits the string |text| by whitespace and returns two things as a pair: 
        the set of words that occur the maximum number of times, and
	their count, i.e.
	(set of words that occur the most number of times, that maximum number/count)
    You might find it useful to use collections.Counter().
    """
    # BEGIN_YOUR_CODE (around 5 lines of code expected)
    words = collections.Counter(text.split())
    if ( len(list(words)) == 0 ) :
        return [()]
    k = set([m[0] for m in words.items() if m[1] == words.most_common(1)[0][1]])
    return ( k, words.most_common(1)[0][1]) 
    # END_YOUR_CODE

############################################################
# Problem 3g

def computeLongestPalindrome(text):
    """
    A palindrome is a string that is equal to its reverse (e.g., 'ana').
    Compute the length of the longest palindrome that can be obtained by deleting
    letters from |text|.
    For example: the longest palindrome in 'animal' is 'ama'.
    Your algorithm should run in O(len(text)^2) time.
    You should first define a recurrence before you start coding.
    """
    # BEGIN_YOUR_CODE (around 20 lines of code expected)
    letters = collections.Counter(text)
    panlindromes = []
    if len(text) <= 1:
        return len(text)
    for l in text:
        if ( letters[l] < 2 ):
            panlindromes.append(1)
            continue
        else:
            next_text = l.join(text.split(l)[1:-1])
            panlindrome = 2 + computeLongestPalindrome(next_text)
            panlindromes.append(panlindrome)
            break

    return max(panlindromes)
    # END_YOUR_CODE
