#!/usr/bin/env python3

import argparse
import linecache
import string
from enum import Enum

### Pig Latin Translator
### This program asks for input and output files and translates the input file to pig latin
### Input is required and output is optional. If no output file is given, the program will write to output.txt
### The program will read the input file line by line and write the translated lines to the output file
### The program will also preserve capitalization and punctuation in the input file


# Enum to represent different rules for translating words to pig latin
class WordType(Enum):
    UNKNOWN = -1 # Word type did not match any checks
    CONSONANT_VOWEL = 1
    CONSONANT_CONSONANT = 2
    VOWEL = 3
    

# Setup the command line arguments
def setupArgs():
    parser = argparse.ArgumentParser(description="Pig Latin Translator")
    parser.add_argument("--input", type=str, help="Input file to translate", required=True)
    parser.add_argument("--output", type=str, help="Output file to write to", required=False)
    return parser.parse_args()


# Get the words from a specific line in a file and return them as a list
def getWordsFromLine(file, line):
    line = linecache.getline(file, line)
    return line.split()


# Check the type of word according to pig latin rules
# Might have to think about order of checks later but it works for now
def checkWordType(word):
    if not word:
        return WordType.UNKNOWN
    if word[0].lower() in "aeiou":
        return WordType.VOWEL
    elif len(word) > 1 and word[1].lower() in "aeiou":
        return WordType.CONSONANT_VOWEL
    elif len(word) > 2 and word[2].lower() in "aeiou":
        return WordType.CONSONANT_CONSONANT
    else:
        return WordType.UNKNOWN


# Transfer the capitalization of the from word to the to word
def transferCapitals(fromWord, toWord):
    returnWord = ""
    for i in range(min(len(fromWord), len(toWord))):
        if fromWord[i].isupper():
            returnWord += toWord[i].upper()
        elif fromWord[i].islower():
            returnWord += toWord[i].lower()
        else:
            returnWord += toWord[i]
    # If the toWord is shorter than the fromWord, then the rest of the word is lowercase
    returnWord += toWord[len(fromWord):].lower()
    return returnWord


# Translate a single word to pig latin
# This is kinda long but refactoring into smaller functions is not worth it
def translateWord(word):
    prefix = "" 
    suffix = " " # Space between words added here because why not. (kinda dumb)

    # Strip any non-alphabetic characters from the front of the word and store them in prefix
    while len(word) > 0 and not word[0].isalpha():
        prefix += word[0]
        word = word[1:]
    # And for suffix
    while len(word) > 0 and not word[-1].isalpha():
        suffix = word[-1] + suffix
        word = word[:-1]

    # Check if the word is empty after stripping non-alphabetic characters
    if not word:
        return prefix + suffix
    
    # Match the word to a rule and store the translation in word
    wordType = checkWordType(word)
    if wordType == WordType.VOWEL:
        word = translateVowel(word)
    elif wordType == WordType.CONSONANT_VOWEL:
        word = translateConsonantVowel(word)
    elif wordType == WordType.CONSONANT_CONSONANT:
        word = translateConsonantConsonant(word)
    else:
        return prefix + word + suffix

    # Add the prefix and suffix back to the word and return it
    return prefix + word + suffix

    
# These three functions just apply the pig latin rules to the word and return it
def translateConsonantVowel(word):
    returnWord = word[1:] + word[0] + "ay"
    return transferCapitals(word, returnWord)
def translateConsonantConsonant(word):
    returnWord = word[2:] + word[0:2] + "ay"
    return transferCapitals(word, returnWord)
def translateVowel(word):
    returnWord = word + "way"
    return transferCapitals(word, returnWord)


# Translate a line of text to pig latin
def translateLine(line):
    words = line.split()
    translatedLine = ""
    for word in words:
        translatedLine += translateWord(word)
    return translatedLine.strip()


# Translate a file to pig latin
def translateFile(inputFile, outputFile):
    with open(inputFile, "r") as file:
        lines = file.readlines()
        with open(outputFile, "w") as outFile:
            for line in lines:
                outFile.write(translateLine(line) + "\n")

# Python boilerplate
def main():
    args = setupArgs()
    print(args.input)
    
    inputFile = args.input

    if args.output:
        outputFile = args.output
    else:
        outputFile = "output.txt"

    translateFile(inputFile, outputFile)

if __name__ == "__main__":
    main()
