import inflect
p = inflect.engine()

# get the grammatical number of a noun (i.e. singular, plural)

def is_plural(noun):
    if noun[1] in ['NNS','NNPS']:
        return True
    elif noun[1] in ['NN', 'NNP']:
        return False
    else:
        raise ValueError

def is_singular(noun):
    if noun[1] in ['NN','NNP']:
        return True
    elif noun[1] in ['NNS', 'NNPS']:
        return False
    else:
        raise ValueError

# change a singular noun to its plural form
# returns any other word unchanged

def get_singular(noun):
    if noun[1] in ['NNS', 'NNPS']:
        return p.plural(noun[0])
    else:
        return noun[0]

# change a plural noun to its singular form
# returns any other word unchanged

def get_plural(noun):
    if noun[1] in ['NN', 'NNP']:
        return p.plural(noun[0])
    else:
        return noun[0]

# define functions to extract words/phrases of specified pos tag sequences

adj_labels = ['JJ', 'JJR', 'JJS']
noun_labels = ['NN', 'NNS', 'NNP', 'NNPS']
verb_labels = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
adv_labels = ['RB', 'RBR', 'RBS']

def get_nouns(words):
    nouns = []
    if len(words) > 1:
        nouns += [[word] for word in words if word[1] in noun_labels]
    return nouns

def get_verbs(words):
    verbs = []
    if len(words) > 1:
        verbs += [[word] for word in words if word[1] in verb_labels]
    return verbs

def get_adjectives(words):
    adj = []
    if len(words) > 1:
        adj += [[word] for word in words if word[1] in adj_labels]
    return adj

def get_vb_nouns(words):
    vb_nouns = []
    if len(words) > 2:
        for i in range(len(words) - 1):
            if words[i][1] in verb_labels and words[i+1][1] in noun_labels:
                vb_nouns.append([words[i], words[i+1]])
    return vb_nouns

def get_adj_verbs(words):
    adj_verbs = []
    if len(words) > 2:
        for i in range(len(words) - 1):
            if words[i][1] in adj_labels and words[i+1][1] in verb_labels:
                adj_verbs.append([words[i], words[i+1]])
    return adj_verbs

def get_adj_nouns(words):
    adj_nouns = []
    if len(words) > 2:
        for i in range(len(words) - 1):
            if words[i][1] in adj_labels and words[i+1][1] in noun_labels:
                adj_nouns.append([words[i], words[i+1]])
    if len(words) > 3:
        for i in range(len(words) - 3):
            if words[i][1] in adj_labels and words[i+1][1] in noun_labels and words[i+2][1] == 'CC' and words[i+3][1] in noun_labels:
                adj_nouns.append([words[i], words[i+3]])
    return adj_nouns

def get_noun_noun(words):
    noun_nouns = []
    if len(words) > 2:
        for i in range(len(words) - 1):
            if words[i][1] in noun_labels and words[i+1][1] in noun_labels:
                noun_nouns.append([words[i], words[i+1]])
        try:
            for i in range(len(words) - 2):
                if words[i][1] in noun_labels and words[i+1][1] == 'IN' and words[i+2][1] in noun_labels:
                    noun_nouns.append([words[i+2], words[i]])
        except IndexError:
            pass
    if len(words) > 3:
        for i in range(len(words) - 3):
            if words[i][1] in noun_labels and words[i+1][1] in noun_labels and words[i+2][1] == 'CC' and words[i+3][1] in noun_labels:
                noun_nouns.append([words[i], words[i+3]])
    return noun_nouns