import json
import nltk
import IntentionDetection
from language import Passage, Sentence, Word
# -*- coding: utf-8 -*-


class inquiry(object):
    "Understands an intention prompt and user response pair"
    def __init__(self, question):
        tally = 1
        for eachSentence in sentenceTokens:
            if tally in selectedSentences:
                print "  * " + str(tally) + ":  " + eachSentence
            else:
                print "    " + str(tally) + ":  " + eachSentence
            tally += 1
        userInput = raw_input('''\n\nAny intentional sentences?
            Enter line number
            0 to save and quit
            or hit return to move on:''')
        if userInput == '':
            print "okay, none\n\n---\n"
            break
        elif int(userInput) == 0:
            resp = raw_input('save and quit? y/n\n: ')
            if resp == "y":
                return my_output
        elif int(userInput) == 0:
            print "undefined"
        elif int(userInput) > 0 and int(userInput) <= tally and not int(userInput) in selectedSentences:
            selectedSentences.append(int(userInput))
        else:
            print "be nice.."
        print "\n\n"


def prompt_setences_and_ask_intention(targetText):
    #########################
    ## Cycle through lines ##
    #########################
    # my_output = []
    # for eachParagraph in targetText:
    selectedSentences = []
    if targetText == '\n':
        return None
    # sentenceTokens = sent_detector.tokenize(eachParagraph.strip())
    # for i in 3 * range(len(targetText)):  # user gets 3*number of sentences
    inquiry()
    i = 1  # user input is 1-indexed, so this is as well
    for eachSentence in sentenceTokens:
        if i in selectedSentences:
            my_output = my_output + [eachSentence, 1]
        if i not in selectedSentences:
            my_output = my_output + [eachSentence, 0]
        i += 1


class Project(object):
    'Understands user-file interactions'
    def __init__(self):
        fileName = raw_input('File Name: ')
        if fileName == "":
            print "no filename given, using exampleText.txt as default"
            self.fileName = 'exampleText'
            self.fileType = 'txt'
        else:
            self.fileType = self.determine_file_type(self.fileName)
        self.fileAsLists = self.load_file(self.fileName, self.fileType)
        self.rawText = " ".join(self.fileAsLists)
        # self.targetText = Passage(self.rawText)
        if self.fileType:
            self.start_txt_session()

    def start_txt_session(self):
        print "And what would you like to do with this file?"
        print "1: Print all intentional sentences"
        print "2: Give the number of sentences in the entire document"
        print "3: Print report on density of intentional statements in text"
        print "4: Manually enter intention data and save as .intention file"
        print "0: Unit tests"
        selectedFunction = input("\n: ")
        if selectedFunction == 1:
            ## 1: Print all intentional sentences
            sentences = Passage(self.rawText).all_intentional_sentences()
            print [each.text for each in sentences]
        elif selectedFunction == 2:
            ## 2: Total number of sentences in the entire document
            print Passage(self.rawText).count_sentences()
        elif selectedFunction == 3:
            ## 3: Print report on density of intentional statements in text
            print Passage(self.rawText).intentional_sentences_density()
        elif selectedFunction == 4:
            ## 4: User inputs to determine which sentences are intentional
            print "Okay, let's begin...\n-----\n\n"
            myOutput = [prompt_setences_and_ask_intention(Passage(each)) for each in self.fileAsLists]
            self.save_and_quit(myOutput, self.fileName)
        elif selectedFunction == 0:
            ## 0: Perform unit tests
            import unittest
            from unitTests import *
            unittest.main()
        else:
            print "Invalid entry"

    def start_intention_entry(self):
        print "And what would you like to do with this file?"
        print "1: Print this .intention file"
        print "2: Pick up prompting where you last left off"
        print "0: Unit tests"
        selectedFunction = input("\n: ")
        if selectedFunction == 1:
            print self.rawText
        elif selectedFunction == 2:
            restart_prompting(self.rawText)
        elif selectedFunction == 0:
            ## 0: Perform unit tests
            import unittest
            from unitTests import *
            unittest.main()
        else:
            print "Invalid entry"

    def save_and_quit(my_output, fileName):
        outputFileName = raw_input('what would you like to call the new file?\n: ')
        if outputFileName == '':
            print "assuming it is the same as input, but with '.intention' appended"
            outputFileName = fileName
        elif '.intention' not in outputFileName:
            outputFileName = outputFileName + '.intention'
        output_file = open(outputFileName, 'w')
        json.dump(my_output, output_file)
        print "\nSuccess!\n\nfile saved as ", outputFileName
        quit('saved and quitting')

    def load_file(fileName, fileTYPE):
        import os
        import codecs
        print "Loading..."
        try:
            textFile = codecs.open(fileName, "rb", encoding="utf-8")
        except:
            try:
                print "Looking also in /TextExamples folder"
                myCWD = os.getcwd()
                fileName = myCWD + "/TextExamples/" + fileName + '.' + fileTYPE
                textFile = codecs.open(fileName, "rb", encoding="utf-8")
            except:
                quit("ERROR FINDING FILE")
        if fileTYPE == "intention":
            rawText = json.load(textFile)
        elif fileTYPE == "txt":
            rawText = textFile.readlines()
        else:
            raise Exception("unrecognized file type")
        textFile.close()
        print "done \n"
        return rawText

    def determine_file_type(fileName):
        if fileName[-10:] == ".intention":
            fileTYPE = "intention"
        elif fileName[-4:] == ".txt":
            fileTYPE = "txt"
        else:
            if fileName[len(str(fileName))-4] == ".":
                quit("unrecognized filetype")
            print "No file extension, assuming it's a .txt file"
            fileTYPE = 'txt'
        return fileTYPE


if __name__ == "__main__":
    Project()
