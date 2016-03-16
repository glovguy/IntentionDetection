import json
import nltk
from language import Sentence, Word, Tag
# -*- coding: utf-8 -*-
# from nltk.chunk import *


# def GrabSentence(word, capitalize=True, taggedVersion=False):
#         ## Find where the sentence starts
#         startDisp = 0
#         '''print "\n\n\n"
#         print word
#         print originalTaggedText[word[2]+startDisp][0][0]
#         print "\n\n\n"'''
#         while originalTaggedText[word[2]+startDisp][0][0] != "." and originalTaggedText[word[2]+startDisp][0][0] != ";" and (originalTaggedText[word[2]+startDisp][0][0] != "!" or originalTaggedText[word[2]+startDisp+1][0][0] != '"') and originalTaggedText[word[2]+startDisp][0][0] != "?":
#             startDisp -= 1
#             if word[2]+startDisp < 0: break
#         try:
#             if not (originalTaggedText[word[2]+endDisp][0][0] == "!" and originalTaggedText[word[2]+endDisp+1][0][0] != '"'):
#                 print "COMBINED EXCLAMATION AND QUOTE"
#                 print originalTaggedText[word[2]+endDisp][1][0]
#                 print originalTaggedText[word[2]+endDisp+1][1][0]
#         except:
#             startDisp += 1
#         ## Find where the sentence ends
#         endDisp = 0
#         while originalTaggedText[word[2]+endDisp][0][0] != "." and originalTaggedText[word[2]+endDisp][0][0] != ";" and (originalTaggedText[word[2]+endDisp][0][0] != "!" or originalTaggedText[word[2]+endDisp+1][0][0] != '"') and originalTaggedText[word[2]+endDisp][0][0] != "?":
#             endDisp += 1
#             try:
#                 originalTaggedText[word[2]+endDisp][0][0] != "."
#             except:
#                 endDisp -= 1
#                 break
#         endDisp += 1
#         try:  # I want to remove these
#             if (originalTaggedText[word[2]+endDisp][1][0] == "!" and originalTaggedText[word[2]+endDisp+1][1][0] != '"'):
#                 print "COMBINED EXCLAMATION AND QUOTE"
#                 print originalTaggedText[word[2]+endDisp][0][0]
#                 print originalTaggedText[word[2]+endDisp+1][0][0]
#         except:
#             "don't fix what ain't broke I guess"
#         ## Smash the sentence together into a human-readable string or isolated tagged sentence
#         sentence = []
#         if taggedVersion is False:
#             for i in range(endDisp - startDisp):
#                 if startDisp == -i and capitalize is True:
#                     sentence.append(str.upper(str(originalTaggedText[word[2]+startDisp+i][0])))  # Capitalize the word passed to the function
#                 else:
#                     sentence.append(originalTaggedText[word[2]+startDisp+i][0])
#             sentence = ' '.join(sentence)
#             ## The above process adds unnecessary spaces before punctuation,
#             ## which we remove below.
#             sentence = sentence.replace(" .", ".")
#             sentence = sentence.replace(" ,", ",")
#             sentence = sentence.replace(" !", "!")
#             sentence = sentence.replace(" ;", ";")
#             sentence = sentence.replace(" :", ":")
#             sentence = sentence.replace(" ?", "?")
#             sentence = sentence.replace(" 's", "'s")
#             sentence = sentence.replace(" 'd", "'d")
#             sentence = sentence.replace(" 've", "'ve")
#             sentence = sentence.replace(" n't", "n't")
#             sentence = sentence.replace(" '", "'")
#             sentence = sentence.replace("''", '"')
#             sentence = sentence.replace("`` ", '"')
#         elif taggedVersion is True:
#             for i in range(endDisp - startDisp):
#                 if startDisp == -i and capitalize is True:
#                     # Capitalize the word passed to the function
#                     appendThis = [str.upper(originalTaggedText[word[2]+startDisp+i][0]), originalTaggedText[word[2]+startDisp+i][1]]
#                     sentence.append(appendThis)
#                 else:
#                     sentence.append(originalTaggedText[word[2]+startDisp+i])
#         return sentence


def detect_verb_beliefs_and_attitudes(POStaggedSentence):
    outputWordList = []  # This will contain all of the words we find that signal a belief/attitude is present
    ## Grab all verbs and put them in a list
    # spot = 0
    verbList = []
    for eachWord in POStaggedSentence:
        if eachWord.POStag.is_verb:
            verb = eachWord
            verbList.append(verb)
        spot += 1
    ## Find any belief verbs
    beliefVerbs = [
        "believe", "believes", "believed", "believing",
        "know", "knows", "knew", "knowing", "perceive",
        "perceives", "perceive", "perceiving", "notice",
        "notices", "noticed", "noticing", "remember",
        "remembers", "remembered", "remembering",
        "imagine", "imagines", "imagined", "imagining",
        "suspect", "suspects", "suppose", "suspecting",
        "assume", "presume", "surmise", "conclude",
        "deduce", "understand", "understands",
        "understood", "understanding", "judge", "doubt",
        "thought"
    ]
    eachVerb = []
    for eachVerb in verbList:
        if str.lower(eachVerb.word) in beliefVerbs:
            outputWordList.append(eachVerb)
    ## Find any attitude verbs
    attitudeVerbs = [
        "want", "wanted", "wants", "wish",
        "wishes", "wished", "consider", "considers",
        "considered", "desire", "desires", "desired", "hope",
        "hoped", "hopes", "aspire", "aspired", "aspires",
        "fancy", "fancied", "fancies", "care", "cares",
        "cared", "like", "likes", "liked"
    ]
    eachVerb = []
    for eachVerb in verbList:
        if str.lower(eachVerb[0]) in attitudeVerbs:
            outputWordList.append(eachVerb)
    return outputWordList


def detect_nonverb_beliefs_and_attitudes(originalTaggedText):
    ## Find 'is' verbs
    isWords = ["is", "was", "were", "are"]
    isVerbsFound = []
    for eachVerb in verbList:
        for testVerb in isWords:
            if str.lower(eachVerb[0]) == testVerb:
                isVerbsFound.append(eachVerb)
    beliefNonVerbs = [
        "belief", "beliefs", "knowledge",
        "perception", "perceptions", "memory", "memories",
        "suspicion", "suspicions", "assumption", "assumptions",
        "presupposition", "presuppositions", "suppositions",
        "supposition", "conclusion", "conclusions",
        "understanding", "judgment", "doubt", "doubts"
    ]
    attitudeNonVerbs = [
        "desire", "desires", "wants", "want", "wish", "wishes",
        "hope", "hopes", "aspirations", "aspiration", "fancy",
        "fancies", "care", "cares", "longing"
    ]
    ## "(PRP) (belief/attitude) is..."
    for isVerb in isVerbsFound:
        ## First, apply a grammar
        grammar = r"""
          NP: {<DT|PRP\$|NNP>?<JJ>*<NN><VB.|VB>}
        """
        cp = nltk.RegexpParser(grammar)
        result = cp.parse(GrabSentence(isVerb, taggedVersion=True, capitalize=False))
        ## Then, extract the chunks found by the grammar
        foundChunks = []
        for eachResult in result:
            if str(eachResult).count('/') > 0:
                foundChunks.append(eachResult)
        ## Check if the subject is a belief/attitude word
        for eachChunk in foundChunks:
            for eachWord in eachChunk:
                if eachWord[1] == "NN":
                    for eachBeliefNonverb in beliefNonVerbs:
                        if str.lower(eachWord[0]) == eachBeliefNonverb:
                            verb = [isVerb[0], isVerb[1], isVerb[2]]
                            outputWordList.append(verb)
                    for eachAttitudeNonverb in attitudeNonVerbs:
                        if str.lower(eachWord[0]) == eachAttitudeNonverb:
                            verb = [isVerb[0], isVerb[1], isVerb[2]]
                            outputWordList.append(verb)
    return outputWordList


def find_all_that_words(POSTaggedSentence):
    index = 0
    THATWordsFound = []
    for eachTaggedWord in originalTaggedText:
        if str.lower(eachTaggedWord[0]) == "that":
            word = wordPickedFromPOStaggedSentence(eachTaggedWord[0], eachTaggedWord[1], index)
            THATWordsFound.append(word)
        index += 1
    return THATWordsFound


def detect_intention_using_that_clauses(POSTaggedSentence):
    THATWordsFound = find_all_that_words(POSTaggedSentence)
    if THATWordsFound is []:
        return []
    phenomenalVerbs = [
        "feel", "feels", "thought", "think"
    ]
    ## "(VB) that ..."
    for thatWord in THATWordsFound:
        ## First, apply a grammar
        grammar = r"""
          NP: {<VB.|VB><IN>}
        """
        myParser = nltk.RegexpParser(grammar)
        result = myParser.parse(GrabSentence(thatWord, taggedVersion=True, capitalize=False))
        ## Then, extract the chunks found by the grammar
        foundChunks = []
        for eachResult in result:
            if str(eachResult).count('/') > 0:
                foundChunks.append(eachResult)
        ## Check if the subject is a belief/attitude word
        for eachChunk in foundChunks:
            for eachWord in eachChunk:
                if eachWord[1] == "VB":
                    for eachPhenomenalVerb in phenomenalVerbs:
                        if str.lower(eachWord[0]) == eachPhenomenalVerb:
                            verb = [thatWord[0], thatWord[1], thatWord[2]]
                            outputWordList.append(verb)
    return True


def is_sentence_intentional(POSTaggedSentence):
    ############################################################
    ## Returns a sentence when given a word with its location ##
    ############################################################
    if detect_verb_beliefs_and_attitudes(POSTaggedSentence) is not False:
        return True
    outputWordList.append(detect_nonverb_beliefs_and_attitudes(POSTaggedSentence))
    outputWordList.append(detect_intention_using_that_clauses(POSTaggedSentence))
    functionOutput = []
    for word in outputWordList:
        functionOutput.append(GrabSentence(word))
    functionOutput = '\n'.join(functionOutput)
    return functionOutput


def print_all_intentional_sentences(raw_text):
    tokens = IntentionDetection.tokenize_each_sentence(raw_text)
    pos_tagged_paragraphs = IntentionDetection.pos_tag_each_tokenized_sentence(tokens)
    for eachParagraph in pos_tagged_paragraphs:
        print eachParagraph
        paragraphIntentions = IntentionDetection.DetectIntentions(eachParagraph)
        if paragraphIntentions != "":
            print "Intentional Sentences:"
            print paragraphIntentions
    print "\n"


def total_number_of_intentional_sentences(raw_text):
    print "\n\n"
    mySum = 0
    # Use this sentence separator from nltk instead of whatever stupid method I was using.
    '''sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    print('\n-----\n'.join(sent_detector.tokenize(text.strip())))'''
    # outline:
    # cut text into sentences
    # cycle through each sentence
    #     ask if each sentence is intentional or not
    #     keep a running total
    # return total
    for eachParagraph in raw_text:
        mySum += countSentences(eachParagraph)
    print "Number of sentences: " + str(mySum)


def countSentences(tokens, returnMarkers=False):
    #if text == "\n": return 0
    ## Tokenize
    #tokens = nltk.word_tokenize(text)
    ## Find where sentences start
    markers = []
    findDisp = 0
    for eachToken in tokens:
        if eachToken == "." or eachToken == ";" or eachToken == "!" or eachToken == "?":
            markers.append(findDisp)
        findDisp += 1
    if markers == []:
        markers.append(len(tokens))
    elif markers[len(markers)-1] != len(tokens)-1:
        markers.append(len(tokens))
    if returnMarkers is False:
        return len(markers)
    else:
        return markers


def report_density_of_intentional_sentences(raw_text):
    tokens = tokenize_each_sentence(raw_text)
    pos_tagged_paragraphs = pos_tag_each_tokenized_sentence(tokens)
    density = []
    for eachParagraph in pos_tagged_paragraphs:
        print "eachParagraph"
        print eachParagraph
        print "\n"
        sentenceMarkers = countSentences(eachParagraph, returnMarkers=True)
        wordlist = DetectIntentions(eachParagraph)
        print "sentenceMarkers:"
        print sentenceMarkers
        print "wordlist:"
        print wordlist
        print "\n"
        for eachSentence in range(len(sentenceMarkers)):
            thisDensity = 0
            for eachWord in wordlist:
                if (eachWord[2] > sentenceMarkers[eachSentence-1] or eachSentence == 0) and eachWord[2] < sentenceMarkers[eachSentence]:
                    thisDensity += 1
            density.append(thisDensity)
    print "density"
    print density
    myfile = open('outputDensity.intention', 'r+')
    json.dump(density, myfile)


def tokenize_each_sentence(paragraphs):
        tokens = []
        for eachParagraph in paragraphs:
            if len(eachParagraph) > 0 and eachParagraph != "\n":
                eachToken = nltk.word_tokenize(eachParagraph)
                tokens.append(eachToken)
        return tokens


def pos_tag_each_tokenized_sentence(tokens):
        pos_tagged_paragraphs = []
        for eachToken in tokens:
            eachTaggedSentence = nltk.pos_tag(tokens)
            pos_tagged_paragraphs.append(eachTaggedSentence)
        return pos_tagged_paragraphs
