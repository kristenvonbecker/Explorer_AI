import inflect
p = inflect.engine()


# get the grammatical number of a noun or verb (i.e. singular, plural)

def is_plural(word):

    if word[1] in ['NNS', 'NNPS', 'VBP']:
        return True
    elif word[1] in ['NN', 'NNP', 'VBZ']:
        return False
    else:
        print('Word must be noun or verb')
        raise ValueError


def is_singular(word):
    if word[1] in ['NN', 'NNP', 'VBZ']:
        return True
    elif word[1] in ['NNS', 'NNPS', 'VBP']:
        return False
    else:
        print('Word must be noun or verb')
        raise ValueError


# change a singular noun or verb to its plural form
# returns any other word unchanged

def get_singular(word):
    if is_plural(word):
        text = p.plural(word[0])
        label = ['NN', 'NNP', 'VBZ'][['NNS', 'NNPS', 'VBP'].index(word[1])]
        return text, label
    else:
        return word


# change a plural noun or verb to its singular form
# returns any other word unchanged

def get_plural(word):
    if is_singular(word):
        text = p.plural(word[0])
        label = ['NNS', 'NNPS', 'VBP'][['NN', 'NNP', 'VBZ'].index(word[1])]
        return text, label
    else:
        return word


# define functions to extract words/phrases of specified pos tag sequences

adj_labels = ['JJ', 'JJR', 'JJS']
noun_labels = ['NN', 'NNS', 'NNP', 'NNPS']
verb_labels = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
adv_labels = ['RB', 'RBR', 'RBS']


def is_noun(word):
    label = word[1]
    return label in noun_labels


def get_nouns(words):
    nouns = []
    nouns += [[get_singular(word)] for word in words if word[1] in noun_labels]
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
            if words[i][1] in verb_labels and words[i + 1][1] in noun_labels:
                vb_nouns.append([words[i], get_singular(words[i + 1])])
            if i < len(words) - 2:
                if words[i][1] in verb_labels and words[i + 1][1] in adj_labels and words[i + 2][1] in noun_labels:
                    vb_nouns.append([words[i], get_singular(words[i + 2])])
    return vb_nouns


def get_adj_verbs(words):
    adj_verbs = []
    if len(words) > 2:
        for i in range(len(words) - 1):
            if words[i][1] in adj_labels and words[i + 1][1] in verb_labels:
                adj_verbs.append([words[i], words[i + 1]])
    return adj_verbs


def get_adj_nouns(words):
    adj_nouns = []
    if len(words) > 2:
        for i in range(len(words) - 1):
            if words[i][1] in adj_labels and words[i + 1][1] in noun_labels:
                adj_nouns.append([words[i], get_singular(words[i + 1])])
            if i < len(words) - 2:
                if words[i][1] in adj_labels and words[i + 1][1] in noun_labels and words[i + 2][1] in noun_labels:
                    adj_nouns.append([words[i], get_singular(words[i + 2])])
    if len(words) > 3:
        for i in range(len(words) - 3):
            if words[i][1] in adj_labels and words[i + 1][1] in noun_labels and words[i + 2][0] in ['of', 'and'] \
                    and words[i + 3][1] in noun_labels:
                adj_nouns.append([words[i], get_singular(words[i + 3])])
    return adj_nouns


def get_noun_noun(words):
    noun_nouns = []
    if len(words) > 2:
        for i in range(len(words) - 1):
            if words[i][1] in noun_labels and words[i + 1][1] in noun_labels:
                noun_nouns.append([get_singular(words[i]), get_singular(words[i + 1])])
            if i < len(words) - 2:
                if words[i][1] in noun_labels and words[i + 1][1] in adj_labels and words[i + 2][1] in noun_labels:
                    noun_nouns.append([get_singular(words[i]), get_singular(words[i + 2])])
        try:
            for i in range(len(words) - 2):
                if words[i][1] in noun_labels and words[i + 1][1] == 'IN' and words[i + 2][1] in noun_labels:
                    noun_nouns.append([get_singular(words[i + 2]), get_singular(words[i])])
        except IndexError:
            pass
    if len(words) > 3:
        for i in range(len(words) - 3):
            if words[i][1] in noun_labels and words[i + 1][1] in noun_labels and words[i + 2][0] == 'and' \
                    and words[i + 3][1] in noun_labels:
                noun_nouns.append([get_singular(words[i]), get_singular(words[i + 3])])
            if words[i][1] in noun_labels and words[i + 1][0] == 'of' and words[i + 2][1] in adj_labels \
                    and words[i + 3][1] in noun_labels:
                noun_nouns.append([words[i], words[i + 1], words[i + 3]])
    return noun_nouns

