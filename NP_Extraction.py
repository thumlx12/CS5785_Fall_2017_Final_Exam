import nltk
import re
from sets import Set
from nltk import Tree
from nltk.stem import WordNetLemmatizer

patterns = """
    NP: {<JJ>*<NN*>+}
    {<JJ>*<NN*><CC>*<NN*>+}
    """

new_patterns = """
    NP:    {<DT><WP><VBP>*<RB>*<VBN><IN><NN>}
           {<NN|NNS|NNP|NNPS><IN    >*<NN|NNS|NNP|NNPS>+}
           {<JJ>*<NN|NNS|NNP|NNPS><CC>*<NN|NNS|NNP|NNPS>+}
           {<JJ>*<NN|NNS|NNP|NNPS>+}

    """

NPChunker = nltk.RegexpParser(patterns)
de_nonletter = re.compile('[^a-zA-Z]')
wl = WordNetLemmatizer()


def cmpNP(target, origin):
    t_words = target.split(' ')
    o_words = origin.split(' ')
    sameWords = list(set(t_words) & set(o_words))
    return len(sameWords)


def deleteEmpty(list):
    return [item for item in list if len(item) > 0]


def findTypeWord(input, typeList):
    dictionary = Set()
    sentences = nltk.sent_tokenize(input)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    for i in range(len(sentences)):
        for j in range(len(sentences[i])):
            sentences[i][j] = de_nonletter.sub('', sentences[i][j].lower())

    sentences = [deleteEmpty(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent) for sent in sentences]
    for sent in sentences:
        for word in sent:
            if word[1] in typeList:
                dictionary.add(wl.lemmatize(word[0]))
    return dictionary


def prepare_text(input):
    sentences = nltk.sent_tokenize(input)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    for i in range(len(sentences)):
        for j in range(len(sentences[i])):
            sentences[i][j] = de_nonletter.sub('', sentences[i][j].lower())

    sentences = [deleteEmpty(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent) for sent in sentences]
    for sentence in sentences:
        for i in range(len(sentence)):
            if sentence[i][1] == 'NNS':
                tlst = list(sentence[i])
                tlst[0] = wl.lemmatize(tlst[0])
                tlst[1] = 'NN'
                sentence[i] = tuple(tlst)
    sentences = [NPChunker.parse(sent) for sent in sentences]
    return sentences


def parsed_text_to_NP(sentences):
    nps = []
    for sent in sentences:
        tree = NPChunker.parse(sent)
        for subtree in tree.subtrees():
            if subtree.label() == 'NP':
                t = subtree
                t = ' '.join(word for word, tag in t.leaves())
                nps.append(t)
    return nps


if __name__ == "__main__":
    sent = 'A men is driving a colorful car.'
    findTypeWord(sent, ['NN','NNS'])
