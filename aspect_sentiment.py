import spacy
from textblob import TextBlob
import pandas as pd

# Import functions from other files
from tweet_handlers import pullTweetsFromCSV, tweetPulls

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
    html = spacy.displacy.render(doc, style='dep')

    filePath = './' + writeFilename + '.html'

    with open(filePath, 'w') as f:
        f.write(html)
    
    return filePath


#extractDescriptors() is a funtion to pull aspects and descriptors from a list of sentences
# Inputs: 
#   - nlp: an NLP object, 
#   - sentenceList: a list of strinsg containing the sentences to be analyzed
# Outputs: 
#   - list of dictionaries containing 'aspect' and 'description' -- not broken by tweet

def extractDescriptors(nlp, sentenceList):
    #We'll ultimately return this aspects list
    aspects = []
    aspects_lemma = []
    attributes = []
    attributes_lemma = []


    #We will iterate through the sentences
    for i, aSentence in enumerate( sentenceList ):
        if i % 100 == 0: print("Tweet# ", str(i))
        doc = nlp(aSentence)
        
        for token in doc:

            ###TODO: 
            # Currently there's no standardization that makes it a 1:1 Noun + Adjective, so that needs to be fixed
            # Also need to add in a case that checks for pronoun resolution and sees what we can do about that

            # We need to identify each noun, and find its descendants that are (pos_ == 'ADJ' or pos_ == 'VERB') and (dep_ == 'amod' or dep_ == 'acl')

            # Modifying rule to examine ALL nouns, not just the subject of the sentence
            #if token.dep_ == 'nsubj' and token.pos_ == 'NOUN':
            if (token.pos_ == 'ADJ' or token.pos_ == 'VERB') and (token.dep_ == 'amod' or token.dep_ == 'acl'):

                #Now append the things
                aspects.append (token.head.text)
                aspects_lemma.append(token.head.lemma_)

                attributes.append( token.text )
                attributes_lemma.append( token.lemma_ )


    return ( aspects , attributes, aspects_lemma, attributes_lemma ) 

# Need a function that pulls attributes for each keyword in the tweet DF, since we need them to be kept separate
# extractTweetAttributes: 
# Takes a DF of tweets, keywords, etc. and pulls out adjectives for each
# Inputs:
#   - nlp: an NLP object,
#   - tweet_df: pandas dataframe containing colums:
#       - Tweet 
#       - Keyword
#       - Spanish
#       - Date
# Returns:
#   - attribute_df: dataframe containing the list of...
#       ...aspects & attributes for each keyword / spanish pair
def extractTweetAttributes(nlp, tweet_df):
    #define return df
    attribute_df = pd.DataFrame( columns = [
        'Keyword',
        'Spanish',
        'aspect',
        'attribute',
        'aspect_lemma',
        'attribute_lemma'
    ])

    # Now create a set for the different keywords and spanish words
    keySet = set( tweet_df['Keyword'] )
    
    for aKey in keySet:
        print("Extracting ", aKey)
        spanishWord = tweet_df.loc[ tweet_df['Keyword'] == aKey ]['Spanish'].iloc[0]

        # And this is where we actually add the various analyses
        ( aspectList , attributeList, aspectList_lemma, attributeList_lemma ) = extractDescriptors( nlp, tweet_df[ tweet_df['Keyword'] == aKey ]['tweet'] )    


        # Now that we've got the data, create lookup lists for the Keyword & Spanish words
        keyList = [aKey] * len(aspectList)
        spanishList = [spanishWord] * len(aspectList)

        temp_df = pd.DataFrame({
            'Keyword': keyList,
            'Spanish': spanishList,
            'aspect': aspectList,
            'attribute': attributeList,
            'aspect_lemma': aspectList_lemma,
            'attribute_lemma': attributeList_lemma
        })

        # Finally, append the data for this keyword to the attribute dataframe
        attribute_df = attribute_df.append( temp_df )
    
    return attribute_df

def countAttributes( aspect_df ):

    temp_df = pd.DataFrame({
        'Keyword': aspect_df['Keyword'],
        'Spanish': aspect_df['Spanish'],
        'aspect': aspect_df['aspect_lemma'],
        'attribute': aspect_df['attribute_lemma']
    })

    return  temp_df.value_counts()

# In the main, this is where the tweet files are loaded...
# ...and routed through the analysis functions
if __name__ == "__main__":
    print("In the main")
    
    # Create the NLP object that will be used for all the text processing
    #nlp = spacy.load("en_core_web_sm")
    # We're actually using a spanish NLP object instead of an English one
    nlp = spacy.load("es_core_news_sm")

    # Pull in CSV files that hold all the tweets
    tweetFileList = [
        './tweet_data/tweet_db_08.27.2021.csv'
    ]

    # Create the DF of tweets from the CSV File
    tweet_df = pullTweetsFromCSV( tweetFileList )#, fileEncoding='ANSI' )

    # Instead of pulling tweets from a file, we're going to get new tweets
    # First we need to designate a list of english + spanish keywords to search for
    keyword_df = pd.read_csv('./keyword_list.csv')

    #tweet_df = tweetPulls( keyword_df )

    #Save the tweet-df because of errors
    #tweet_df.to_csv('./tweet_data/tweet_db_08.27.2021.csv')#, encoding='ANSI')

    # Run the tweets through the attribute extractor
    aspect_df = extractTweetAttributes ( nlp, tweet_df)

    
    # Run the aspects & attributes through a modified version of the wordcount function
    count_df = countAttributes( aspect_df )
    #   - Not to mention run some sort of pronoun resolution
    
    count_df.to_csv('./tweet_data/aspect_count_08.27.2021.csv')