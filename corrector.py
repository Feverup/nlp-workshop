import re
import collections

ALPHABET = 'qwertyuiopasdfghjklzxcvbnm'


def words(text):
    return re.findall('[a-z]+', text.lower())


def train(words):
    model = collections.defaultdict(lambda: 1)
    for word in words:
        model[word] += 1
    return model

NWORDS = train(words(open('data/anna_karenina.txt', 'r').read()))


def edits_1(word):

    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [a + b[1:] for a, b in splits if b]
    transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b) > 1]
    replaces = [a + c + b[1:] for a, b in splits for c in ALPHABET if b]
    inserts = [a + c + b for a, b in splits for c in ALPHABET]

    return set(deletes + transposes + replaces + inserts)


def known_edits_2(word):
    return set(e2 for e1 in edits_1(word) for e2 in edits_1(e1) if e2 in NWORDS)


def known(words):
    return set(w for w in words if w in NWORDS)


def correct(word):
    corrections = known([word]) or known(edits_1(word)) or known_edits_2(word) or [word]
    return max(corrections, key=NWORDS.get)

print correct('kanenina')
