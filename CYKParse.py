# Code for CS 171, Winter, 2021
import Tree

#a boolean variable to determine the status of uing more words than needed  
verbose = False


def printV(*args):
    if verbose:
        print(*args)

# A Python implementation of the AIMA CYK-Parse algorithm in Fig. 23.5 (p. 837).
def CYKParse(words, grammar):
    T = {}  #a dictionary T[X, i, j] is the most probable X tree spanning words
    P = {}  #a table that SHOULD STORE ALL PROBABILITY FOR EACH KEY
    #  P[X, i,k] is probability of tree T[X, i ,k]

    # Instead of explicitly initializing all P[X, i, k] to 0, store
    # only non-0 keys, and use this helper function to return 0 as needed.
    ### getP function initializes all keys to 0
    ### getP function returns a key in the tree X
    def getP(X, i, k):
        #key is a concatinated string to store into table P
        key = str(X) # + '/' + str(i) + '/' + str(k)
        if key in P:
            return P[key]
        else:
            return 0

    # Insert lexical categories for each word
    # for i in range(len(words)):
    for word in words:
        #X is a tree spanning words[i:k]
        for X, p in getGrammarLexicalRules(grammar, word):
            # P[X + '/' + str(i) + '/' + str(i)] = p
            P[X] = p

            # T[X] = Tree.Tree(X, None, None, lexiconItem=words[i])
            T[X] = word

    printV('P:', P)
    printV('T:', T)
    # printV('T:', [str(T[t]) for t in T])

    # printV('T:', [str(t)+':'+str(T[t]) for t in T])
    # Construct X_i:j from Y_i:j + Z_j+i:k, shortest spans first
    # for i, j, k in subspans(len(words)):
    #     for X, Y, p in getGrammarSyntaxRules(grammar):
    #         # printV('i:', i, 'j:', j, 'k:', k, '', X, '->', Y, '['+str(p)+']', 
    #         #         'PY =' ,getP(Y, i, j), p, '=', getP(Y, i, j) * getP(Y, j+1, k) * p)
    #         PY = getP(Y, i, j) * getP(Y, j+1, k) * p
    #         if PY > getP(X, i, k):
    #             # printV('     inserting from', i, '-', k, ' ', X, '->', T[Y+'/'+str(i)+'/'+str(j)], T[Y+'/'+str(j+1)+'/'+str(k)],
    #             #             'because', PY, '=', getP(Y, i, j), '*', getP(Z, j+1, k), '*', p, '>', getP(X, i, k), '=',
    #             #             'getP(' + X + ',' + str(i) + ',' + str(k) + ')')
    #             P[X] = PY
    #             # T[X] = Tree.Tree(X, T[Y+'/'+str(i)+'/'+str(j)], T[Y+'/'+str(j+1)+'/'+str(k)])
    # # printV('T:', [str(T[t]) for t in T])
    # printV('P:', P)
    return T, P

# Python uses 0-based indexing, requiring some changes from the book's
# 1-based indexing: i starts at 0 instead of 1
def subspans(N):
    for length in range(2, N+1):
        for i in range(N+1 - length):
            k = i + length - 1
            for j in range(i, k):
                # print(i, j, k)
                yield i, j, k

# These two getXXX functions use yield instead of return so that a single pair can be sent back,
# and since that pair is a tuple, Python permits a friendly 'X, p' syntax
# in the calling routine.
def getGrammarLexicalRules(grammar, word):
    # 'lexicon' : [
    # ['Noun', 'stench', 0.05],
    for rule in grammar['lexicon']:
        if rule[1] == word:
            yield rule[0], rule[2]

def getGrammarSyntaxRules(grammar):
    #tuple
    rule = []
    for rule in grammar['syntax']:
        yield rule[0], rule[1], rule[2]

# 'Grammar' here is used to include both the syntax part and the lexicon part.

# E0 from AIMA, ps. 834.  Note that some syntax rules were added or modified 
# to shoehorn the rules into Chomsky Normal Form. 
def getGrammarE0():
    return {
        'syntax' : [
            ['S', 'NP', 'VP', 0.9 * 0.45 * 0.6],
            ['S', 'Pronoun', 'VP', 0.9 * 0.25 * 0.6],
            ['S', 'Name', 'VP', 0.9 * 0.10 * 0.6],
            ['S', 'Noun', 'VP', 0.9 * 0.10 * 0.6],
            ['S', 'NP', 'Verb', 0.9 * 0.45 * 0.4],
            ['S', 'Pronoun', 'Verb', 0.9 * 0.25 * 0.4],
            ['S', 'Name', 'Verb', 0.9 * 0.10 * 0.4],
            ['S', 'Noun', 'Verb', 0.9 * 0.10 * 0.4],
            ['S', 'S', 'Conj+S', 0.1],
            ['Conj+S', 'Conj', 'S', 1.0],
            ['NP', 'Article', 'Noun', 0.25],
            ['NP', 'Article+Adjs', 'Noun', 0.15],
            ['NP', 'Article+Adjective', 'Noun', 0.05],
            ['NP', 'Digit', 'Digit', 0.15],
            ['NP', 'NP', 'PP', 0.2],
            ['NP', 'NP', 'RelClause', 0.15],
            ['NP', 'NP', 'Conj+NP', 0.05],
            ['Article+Adjs', 'Article', 'Adjs', 1.0],
            ['Article+Adjective', 'Article', 'Adjective', 1.0],
            ['Conj+NP', 'Conj', 'NP', 1.0],
            ['VP', 'VP', 'NP', 0.6 * 0.55],
            ['VP', 'VP', 'Adjective', 0.6 * 0.1],
            ['VP', 'VP', 'PP', 0.6 * 0.2],
            ['VP', 'VP', 'Adverb', 0.6 * 0.15],
            ['VP', 'Verb', 'NP', 0.4 * 0.55],
            ['VP', 'Verb', 'Adjective', 0.4 * 0.1],
            ['VP', 'Verb', 'PP', 0.4 * 0.2],
            ['VP', 'Verb', 'Adverb', 0.4 * 0.15],
            ['Adjs', 'Adjective', 'Adjs', 0.8],
            ['PP', 'Prep', 'NP', 0.65],
            ['PP', 'Prep', 'Pronoun', 0.2],
            ['PP', 'Prep', 'Name', 0.1],
            ['PP', 'Prep', 'Noun', 0.05],
            ['RelClause', 'RelPro', 'VP', 0.6],
            ['RelClause', 'RelPro', 'Verb', 0.4]
        ],
        'lexicon' : [
            ['Noun', 'stench', 0.05],
            ['Noun', 'breeze', 0.05],
            ['Noun', 'wumpus', 0.05],
            ['Noun', 'pits', 0.05],
            ['Noun', 'dungeon', 0.05],
            ['Noun', 'frog', 0.05],
            ['Noun', 'balrog', 0.7],
            ['Verb', 'is', 0.1],
            ['Verb', 'feel', 0.1],
            ['Verb', 'smells', 0.1],
            ['Verb', 'stinks', 0.05],
            ['Verb', 'wanders', 0.65],
            ['Adjective', 'right', 0.1],
            ['Adjective', 'dead', 0.05],
            ['Adjective', 'smelly', 0.02],
            ['Adjective', 'breezy', 0.02],
            ['Adjective', 'green', 0.81],
            ['Adverb', 'here', 0.05],
            ['Adverb', 'ahead', 0.05],
            ['Adverb', 'nearby', 0.02],
            ['Adverb', 'below', 0.88],
            ['Pronoun', 'me', 0.1],
            ['Pronoun', 'you', 0.03],
            ['Pronoun', 'I', 0.1],
            ['Pronoun', 'it', 0.1],
            ['Pronoun', 'she', 0.67],
            ['RelPro', 'that', 0.4],
            ['RelPro', 'which', 0.15],
            ['RelPro', 'who', 0.2],
            ['RelPro', 'whom', 0.02],
            ['RelPro', 'whoever', 0.23],
            ['Name', 'Ali', 0.01],
            ['Name', 'Bo', 0.01],
            ['Name', 'Boston', 0.01],
            ['Name', 'Marios', 0.97],
            ['Article', 'the', 0.4],
            ['Article', 'a', 0.3],
            ['Article', 'an', 0.05],
            ['Article', 'every', 0.05],
            ['Prep', 'to', 0.2],
            ['Prep', 'in', 0.1],
            ['Prep', 'on', 0.05],
            ['Prep', 'near', 0.10],
            ['Prep', 'alongside', 0.55],
            ['Conj', 'and', 0.5],
            ['Conj', 'or', 0.1],
            ['Conj', 'but', 0.2],
            ['Conj', 'yet', 0.2],
            ['Digit', '0', 0.1],
            ['Digit', '1', 0.1],
            ['Digit', '2', 0.1],
            ['Digit', '3', 0.1],
            ['Digit', '4', 0.1],
            ['Digit', '5', 0.1],
            ['Digit', '6', 0.1],
            ['Digit', '7', 0.1],
            ['Digit', '8', 0.1],
            ['Digit', '9', 0.1]
        ]
    }


# Sample sentences:
# Hi, I am Peter. I am Peter. Hi, my name is Peter. My name is Peter.
# What is the temperature in Irvine? What is the temperature in Irvine now? 
# What is the temperature in Irvine tomorrow? 
# 
def getGrammar():
    return {
        'syntax' : [
            ['S', 'Greeting', 0.25],
            ['S', 'NP', 0.25],
            ['S', 'WQuestion', 0.25],
            ['VP', 'Verb', 1],
            ['NP', 'Noun', 0.2],
            ['NP', 'Pronoun', 0.2],
            ['NP', 'Digit', 0.2],
            ['NP', 'RelClause', 0.2],
            ['NP', 'Name', 0.2],
            ['Adj', 'Adjective', 1]
        ],
        'lexicon' : [
            ['Greeting', 'hi', 0.5],
            ['Greeting', 'hello', 0.5],
            ['WQuestion', 'what', 0.5],
            ['WQuestion', 'when', 0.25],
            ['WQuestion', 'which', 0.25],
            ['WQuestion', 'where', 0.25],
            ['HQuestion', 'how', 0.25],
            ['Verb', 'cancel', 0.5],
            ['Verb', 'thank', 0.5],
            ['Verb', 'am', 0.5],
            ['Verb', 'is', 0.5],
            ['Verb', 'will', 0.0],   #recalculate p for will verb
            ['Verb', 'park', 0],
            ['Verb', 'located', 0],
            ['Verb', 'pay', 0],
            ['Verb', 'pay', 0],
            ['Name', 'peter', 0.1],
            ['Name', 'sue', 0.1],
            ['Name', 'bao', 0.1],
            ['Name', 'bebe', 0.01],
            ['Name', 'tammy', 0.01],
            ['Name', 'davis', 0.01],
            # ['Name', '', 0.01],
            ['Pronoun', 'me', 0.1],
            ['Pronoun', 'you', 0.03],
            ['Pronoun', 'I', 0.1],
            ['Pronoun', 'i', 0.1],
            ['Pronoun', "i'm", 0.1],
            ['Pronoun', 'it', 0.1],
            ['Pronoun', 'she', 0.67],
            ['Pronoun', 'he', 0.67],

            # ['AdverbPhrase', 'yesterday', 0], #recalculate p
            # ['AdverbPhrase', 'tomorrow', 0], #recalculate p
            # ['AdverbPhrase', 'weekend', 0], #recalculate p
            # ['AdverbPhrase', 'weekday', 0], #recalculate p
            ['Noun', 'man', 0.2],
            ['Noun', 'thanks', 0.2],
            ['Noun', 'name', 0.2],
            ['Noun', 'pedicure', 0.8],
            ['Noun', 'manicure', 0.8],#recalculate p
            ['Noun', 'pedi', 0.8],
            ['Noun', 'mani', 0.8],#recalculate p
            ['Noun', 'pedicures', 0.8],
            ['Noun', 'manicures', 0.8],#recalculate p
            ['Noun', 'pedis', 0.8],
            ['Noun', 'manis', 0.8],#recalculate p

            ['Noun', 'appointment', 0.8],
            ['Noun', 'arrangement', 0.8],#recalculate p
            ['Noun', 'appointments', 0.8],
            ['Noun', 'arrangements', 0.8],#recalculate p
            ['Noun', 'address', 0],
            ['Noun', 'staff',0],
            ['Noun', 'availability',0],
            ['Noun', 'service',0],
            ['Noun', 'services',0],

            ['Type', 'gel', 0],
            ['Type', 'regular',0],
            ['Type', 'deluxe',0],
            ['Type', 'french',0],
            ['Type', 'paraffin',0],
            ['Article', 'the', 0.7],
            ['Article', 'a', 0.3],
            ['Adjective', 'my', 1.0],
            ['Adjective', 'hotter', 1.0],
            ['Adjective', 'much', 1.0],
            ['Adjective', 'available', 1.0],
            ['Adverb', 'now', 0.4],
            ['Adverb', 'today', 0.3],
            ['Adverb', 'yesterday', 0.4],
            ['Adverb', 'tomorrow', 0.3],
            ['Adverb', 'weekend', 0], #recalculate p
            ['Adverb', 'weekday', 0], #recalculate p

            ['Preposition', 'with', 0.5],
            ['Preposition', 'in', 0.5],
            ['RelPro', 'that', 0.4],
            ['RelPro', 'which', 0.15],
            ['RelPro', 'who', 0.2],
            ['RelPro', 'whom', 0.02],
            ['RelPro', 'whoever', 0.23],
            ['Article', 'the', 0.4],
            ['Article', 'a', 0.3],
            ['Article', 'couple', 0.3],
            ['Article', 'an', 0.05],
            ['Article', 'every', 0.05],
            ['Prep', 'to', 0.2],
            ['Prep', 'in', 0.1],
            ['Prep', 'on', 0.05],
            ['Prep', 'near', 0.10],
            ['Prep', 'alongside', 0.55],
            ['Conj', 'and', 0.5],
            ['Conj', 'or', 0.1],
            ['Conj', 'but', 0.2],
            ['Conj', 'yet', 0.2],
            ['Digit', '0', 0.1],
            ['Digit', '1', 0.1],
            ['Digit', '2', 0.1],
            ['Digit', '3', 0.1],
            ['Digit', '4', 0.1],
            ['Digit', '5', 0.1],
            ['Digit', '6', 0.1],
            ['Digit', '7', 0.1],
            ['Digit', '8', 0.1],
            ['Digit', '9', 0.1],
            ['Digit', 'one', 0.1],
            ['Digit', 'two', 0.1],
            ['Digit', 'three', 0.1],
            ['Digit', 'four', 0.1],
            ['Digit', 'five', 0.1],
            ['Digit', 'six', 0.1],
            ['Digit', 'seven', 0.1],
            ['Digit', 'eight', 0.1],
            ['Digit', 'nine', 0.1],
            ['Digit', 'ten', 0.1],
            ['Hour', '9:00', 0.1],
            ['Hour', '10:00', 0.1],
            ['Hour', '11:00', 0.1],
            ['Hour', '12:00', 0.1],
            ['Hour', '13:00', 0.1],
            ['Hour', '14:00', 0.1],
            ['Hour', '15:00', 0.1],
            ['Hour', '16:00', 0.1],
            ['Hour', '17:00', 0.1],
            ['Hour', '18:00', 0.1],
            ['Date', 'monday', 0.1],
            ['Date', 'tuesday', 0.1],
            ['Date', 'wednesday', 0.1],
            ['Date', 'thursday', 0.1],
            ['Date', 'friday', 0.1],
            ['Date', 'saturday', 0.1],
            ['Date', 'sunday', 0.1]

        ]
    }

# Unit testing code
if __name__ == '__main__':
    verbose = True
    # ['S', 'Greeting', 0.25],
    # ['S', 'NP' : 
    # ['VP', 'Verb', 1], book, like, would, can, help, have, get, sounds, got, upgrade, works, assist, arrive, send, confirm, set
    # ['NP', 'Noun', 0.2],  appointment, reminder, number, coat, nail, buffer, glitter, foot, hand, finger, 
    # ['NP', 'Pronoun', 0.2],
    # ['NP', 'Digit', 0.2],
    # ['NP', 'RelClause', 0.2],
    # ['NP', 'Name', 0.2],
    # ['Adj', 'Adjective', 1] base

    # I would like to book an appointment for a pedicure today please.
    # BookIt: This is BookIt. How can help you today?
    # Customer: Hi, I’m Paula. I would like to book an appointment for a pedicure today please.
    # BookIt: Hi, Paula. We have a few options for a pedicure. Would you like to get a regular, gel, or deep pedicure? ¬¬
    # Customer: A gel pedicure sounds nice. 
    # BookIt: You got it. Would you like to upgrade it to deluxe for an additional $10? 
    # Customer: No, thank you. But actually I would like to book one gel pedicure for my mom as well. 
    # BookIt: Absolutely. What time would be best for you and your mom?
    # Customer: Hmmm… How about 3pm?
    # BookIt: That works. Bebe and Tammy will be available to assist you and your mom when you arrive. Would you like me to send you a reminder 30 minutes prior your appointment?
    # Customer: Yes. Sure. 
    # BookIt: You got it. Can you confirm your phone number for me please? 
    # Customer: 530-753-9999
    # BookIt: Perfect. Paula, you are all set for two gel pedicures at 3pm today. Is there anything else I can assist you with?
    # Customer: No. All sounds good. Thank you. See you guys soon. 
    # BookIt: We are looking forward to seeing you and your mom at 3pm. Thank you and enjoy your day!   

    # CYKParse(['will', 'tomorrow', 'be', 'hotter', 'than', 'today', 'in', 'Pasadena'], getGrammar())


# Hi, I am Peter. I am Peter. Hi, my name is Peter. My name is Peter.
# What is the temperature in Irvine? What is the temperature in Irvine now? 
# What is the temperature in Irvine tomorrow? 