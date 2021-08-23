import spacy
from textblob import TextBlob
import pandas as pd

# Import functions from other files
from tweet_handlers import pullTweetsFromCSV

### Declare functions to standardize, identify, and analyze input text
# Will ultimately take in a list of tweets and return:
# - Word counts
# - Split of positive / negative aspects
# - Brand identification?

#visualizeText() is a funtion to diagram sentences for help troubleshooting
# Inputs: 
#   - nlp: an NLP object, 
#   - txt = a string containing the sentence to be diagramed, 
#   - writeFilename: a string containing the filename to write the HTML diagram to
# Returns:
#   - writeFilename: the path of the file that contains the HTML diagram
def visualizeText(nlp, txt, writeFilename):
    doc = nlp(txt)
    spacy.displacy.render(doc, style='dep')

    filePath = './' + writeFilename + '.html'

    with open(writeFilename, 'w') as f:
        f.write(txt)
    
    return writeFilename


#extractDescriptors() is a funtion to pull aspects and descriptors from a list of sentences
# Inputs: 
#   - nlp: an NLP object, 
#   - sentenceList = a list of strinsg containing the sentences to be analyzed
# Outputs: 
#   - list of dictionaries containing 'aspect' and 'description' -- not broken by tweet

def extractDescriptors(nlp, sentenceList):
    #We'll ultimately return this aspects list
    aspects = []

    #We will iterate through the sentences
    for aSentence in sentenceList:
        doc = nlp(aSentence)
        descriptive_term = ''
        target = ''
        for token in doc:
            if token.dep_ == 'nsubj' and token.pos_ == 'NOUN':
                target = token.text

            if token.pos_ == 'ADJ':
                prepend = ''
                for child in token.children:
                    if child.pos_ != 'ADV':
                        continue
                    prepend += child.text + ' '
                descriptive_term = prepend + token.text
        aspects.append({
            'aspect': target,
            'description': descriptive_term
        })

    return aspects

# In the main, this is where the tweet files are loaded...
# ...and routed through the analysis functions
if __name__ == "__main__":
    print("In the main")
    nlp = spacy.load("en_core_web_sm")


    tweetFileList = [
        './tweet_data/Fanta-Tweet-DB-08.10.2021.csv',
        './tweet_data/Flavor-Tweet-DB-FULL.csv'
    ]

    tweet_df = pullTweetsFromCSV( tweetFileList )

    sentences = [
        'The food we had yesterday was delicious',
        'My time in Italy was very enjoyable',
        'I found the meal to be tasty',
        'The internet was slow.',
        'Our experience was suboptimal'
    ]