# import nlok
import spacy


# I haven't yet decided if I am going "all in" on using spacy instead of NLTK, 
# so in the meantime there will be code duplication
def load_spacy():
    if 'nlp' not in globals():
        from time import time
        print("Loading Spacy parser...")
        t1 = time()
        global nlp
        nlp = spacy.load('en')
        t2 = time()
        print("Done in " + str(t2-t1) + " seconds")
    return nlp


def make_span(text):
    nlp = load_spacy()
    if type(text) is spacy.tokens.doc.Doc:
        text = text.sents.next()
    elif type(text) is str:
        text = next(nlp(text).sents)
    return text


def tense(text):
    text = make_span(text)
    tag = text.root.tag_
    if tag == 'VBD' or tag == 'VBN':
        tense = 'past'
    elif tag == 'VBP' or tag == 'VBZ' or tag == 'VBG':
        tense = 'present'
    else:
        aux = [t for t in text if t.tag_ == 'MD']
        if True in [text.root.is_ancestor(t) for t in aux]:
            tense = 'future'
    return tense


def determine_frame(text):
    from nltk.corpus import verbnet as vn
    from pattern.en import conjugate, INFINITIVE
    text = make_span(text)
    root = conjugate(text.root.text.lower(), tense=INFINITIVE)
    vnclasses = vn.classids(lemma=root)
    if len(vnclasses) == 1:
        return vnclasses[0]
    else:
        print(vnclasses)
        return False


if __name__ == '__main__':
    import unittest
    from unitTests import test_language_objects
    suite = unittest.TestLoader().loadTestsFromTestCase(test_language_objects)
    unittest.TextTestRunner(verbosity=2).run(suite)
