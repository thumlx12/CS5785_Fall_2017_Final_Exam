import nltk
import re
import pprint
from nltk import Tree
from nltk.stem.porter import PorterStemmer
from sets import Set
from pattern.text.en import singularize

patterns = """
    NP: {<JJ>*<NN*>+}
    {<JJ>*<NN*><CC>*<NN*>+}
    """

new_patterns = """
    NP:    {<DT><WP><VBP>*<RB>*<VBN><IN><NN>}
           {<NN|NNS|NNP|NNPS><IN>*<NN|NNS|NNP|NNPS>+}
           {<JJ>*<NN|NNS|NNP|NNPS><CC>*<NN|NNS|NNP|NNPS>+}
           {<JJ>*<NN|NNS|NNP|NNPS>+}

    """

NPChunker = nltk.RegexpParser(patterns)
de_nonletter = re.compile('[^a-zA-Z]')
ps = PorterStemmer()


def cmpNP(target, origin):
    t_words = target.split(' ')
    o_words = origin.split(' ')
    sameWords = list(set(t_words) & set(o_words))
    # if sameWords.__len__() > 0:
    #     print(sameWords, target, float(len(sameWords)) / len(t_words))
    return float(len(sameWords)) / len(t_words)


def deleteEmpty(list):
    return [item for item in list if len(item) > 0]


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
                tlst[0] = singularize(tlst[0])
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


def find_nps(text):
    prepared = prepare_text(text)
    return parsed_text_to_NP(prepared)


if __name__ == "__main__":
    sample_text = """Good behaviors upon the street, or public promenade, marks the gentleman
most effectually; rudeness, incivility, disregard of "what the world
says," marks the person of low breeding. We always know, in walking a
square with a man, if he is a gentleman or not. A real gentility never
does the following things on the street, in presence of observers:--

Never picks the teeth, nor scratches the head.

Never swears or talks uproariously.

Never picks the nose with the finger.

Never smokes, or spits upon the walk, to the exceeding annoyance of
those who are always disgusted with tobacco in any shape.

Never stares at any one, man or woman, in a marked manner.

Never scans a lady's dress impertinently, and makes no rude remarks
about her.

Never crowds before promenaders in a rough or hurried way.

Never jostles a lady or gentleman without an "excuse me."

Never treads upon a lady's dress without begging pardon.

Never loses temper, nor attracts attention by excited conversation.

Never dresses in an odd or singular manner, so as to create remark.

Never fails to raise his hat politely to a lady acquaintance; nor to
a male friend who may be walking with a lady--it is a courtesy to the
lady.
"""
    print(Set(find_nps(sample_text)))
