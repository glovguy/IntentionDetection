import unittest
from IntentionDetection import *
from IntentionPrompts import *
from language import *
from spacylang import *
from illocutionary import *


class test_statements(unittest.TestCase):
    def test_comparisons(self):
        self.assertEqual(Statement("He operated the pump"), Statement("He operated the pump"))
        self.assertNotEqual(Statement("I operated the pump"), Statement("He operated the pump"))

    def test_statement_tense(self):
        act1 = Statement("He operated the pump")
        act2 = Statement("He will operate the pump")
        act3 = Statement("He operates the pump")
        act4 = Statement("He is operating the pump")
        self.assertEqual(act1.tense, 'past')
        self.assertEqual(act2.tense, 'future')
        self.assertEqual(act3.tense, 'present')
        self.assertEqual(act4.tense, 'present')

    def test_statement_subject(self):
        act1 = Statement("He operated the pump")
        act2 = Statement("The mayor operated the pump")
        self.assertEqual(act1.subject.text, "He")
        self.assertEqual(act2.subject.text, "The mayor")

    def test_assign_predicate(self):
        act1 = Statement("He operated the pump")
        act2 = Statement("The mayor operated the pump")
        self.assertEqual(act1.predicate.text, "operated the pump")
        self.assertEqual(act1.predicate.text, act2.predicate.text)

    def test_aux_in_predicate(self):
        act3 = Statement("He is replacing the water")
        self.assertEqual(act3.predicate.text, "is replacing the water")

    def test_adverb_in_predicate(self):
        act4 = Statement("Sam smoked habitually")
        self.assertEqual(act4.predicate.text, "smoked habitually")

    def test_clausal_complement_in_predicate(self):
        act5 = Statement("Roger told me to bake him a cake tomorrow")
        self.assertEqual(act5.predicate.text, "told me to bake him a cake tomorrow")

    def test_nounphrase_adverb_modifier_in_predicate(self):
        act6 = Statement("Tomorrow afternoon, my family will give me a call.")
        self.assertEqual(act6.predicate.text, "will give me a call tomorrow afternoon")


class test_functions_in_IntentionPrompts(unittest.TestCase):
    def test_determine_file_type(self):
        self.assertEqual(determine_file_type("jldsnfkjds.json"), 'json')
        self.assertEqual(determine_file_type("intent.n.json"), 'json')
        self.assertEqual(determine_file_type("exampleText.txt"), "txt")


class test_language_spacy_mixins(unittest.TestCase):
    def test_determine_frame(self):
        self.assertEqual('substance_emission-43.4', determine_frame("I shed those tears in vain"))

    def test_tense(self):
        self.assertEqual('present', tense("I am eating."))
        self.assertEqual('past', tense("I ran earlier today."))
        self.assertEqual('future', tense("I will eat later after 7pm."))


class test_detection_functions(unittest.TestCase):
    def test_detect_nonverb_beliefs_and_attitudes(self):
        s1 = Sentence('My belief is that this coffee is the best in Manhattan.')
        s2 = Sentence('My dog is very obedient.')
        s3 = Sentence('My desire is to become a Samana.')
        self.assertEqual(True, detect_nonverb_beliefs(s1))
        self.assertEqual(False, detect_nonverb_attitudes(s1))
        self.assertEqual(False, detect_nonverb_beliefs(s2))
        self.assertEqual(True, detect_nonverb_attitudes(s3))
        self.assertEqual(False, detect_nonverb_beliefs(s3))

    def test_detect_intention_using_that_clauses(self):
        s4 = Sentence('He started to feel that that was enough coffee for today.')
        s5 = Sentence('I think that you are mistaken.')
        self.assertEqual(True, detect_intention_using_that_clauses(s4))
        self.assertEqual(True, detect_intention_using_that_clauses(s5))

    def test_is_sentence_intentional(self):
        s1 = Sentence('"How deaf and stupid have I been!" he thought, walking swiftly along.')
        s2 = Sentence("This is a sentence that doesn't express intention.")
        s3 = Sentence('I want this sentence to express intention..')
        s4 = Sentence('He started to feel that that was enough coffee for today.')
        s5 = Sentence('I want this sentence to express intention..')
        self.assertEqual(False, is_sentence_intentional(s1))
        self.assertEqual(False, is_sentence_intentional(s2))
        self.assertEqual(True, is_sentence_intentional(s3))
        self.assertEqual(True, is_sentence_intentional(s4))
        self.assertEqual(True, is_sentence_intentional(s5))
        self.assertEqual(True, is_sentence_intentional(str('I want this.')))
        self.assertEqual(True, is_sentence_intentional('I want this.'))

    def test_all_intentional_sentences(self):
        p1 = Passage('''
"How deaf and stupid have I been!" he thought, walking swiftly along. "When someone reads a text,\
wants to discover its meaning, he will not scorn the symbols and letters and call them deceptions,\
coincidence, and worthless hull, but he will read them, he will study and love them, letter by\
letter. But I, who wanted to read the book of the world and the book of my own being, I have,\
for the sake of a meaning I had anticipated before I read, scorned the symbols and letters, I\
called the visible world a deception, called my eyes and my tongue coincidental and worthless forms\
without substance. No, this is over, I have awakened, I have indeed awakened and have not been born\
before this very day."
This is a sentence that doesn't express intention. I want this sentence to express intention..
He started to feel that that was enough coffee for today.
        ''')
        s1 = Sentence("I want this sentence to express intention..")
        s2 = Sentence("He started to feel that that was enough coffee for today.")
        s3 = Sentence('''"When someone reads a text,\
wants to discover its meaning, he will not scorn the symbols and letters and call them deceptions,\
coincidence, and worthless hull, but he will read them, he will study and love them, letter by\
letter.''')
        self.assertTrue(s1 in p1.all_sentences_of_type(is_sentence_intentional))
        self.assertTrue(s2 in p1.all_sentences_of_type(is_sentence_intentional))
        self.assertTrue(s3 in p1.all_sentences_of_type(is_sentence_intentional))

    def test_detect_desire(self):
        s1 = Sentence('"How deaf and stupid have I been!" he thought, walking swiftly along.')
        s2 = Sentence("This is a sentence that doesn't express intention.")
        s3 = Sentence('I want this sentence to express intention..')
        s4 = Sentence('He started to feel that that was enough coffee for today.')
        s5 = Sentence('I want this sentence to express intention..')
        self.assertEqual(False, sentence_indicates_desire(s1))
        self.assertEqual(False, sentence_indicates_desire(s2))
        self.assertEqual(True, sentence_indicates_desire(s3))
        self.assertEqual(True, sentence_indicates_desire(s4))
        self.assertEqual(True, sentence_indicates_desire(s5))
    
    def test_intentional_sentences_density(self):
        p1 = Passage("""But I, who wanted to read the book of the world and the book of my own being, I have,\
         for the sake of a meaning I had anticipated before I read, scorned the symbols and letters, I
         called the visible world a deception, called my eyes and my tongue coincidental and worthless forms
         without substance. No, this is over, I have awakened, I have indeed awakened and have not been born
         before this very day."
        This is a sentence that doesn't express intention. I want this sentence to express intention..
        He started to feel that that was enough coffee for today.""")
        self.assertEqual(p1.sentence_density_of_type(is_sentence_intentional), [True, False, False, True, True])



if __name__ == '__main__':
    unittest.main(verbosity=1)
