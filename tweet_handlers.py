import pandas as pd


# pullTweetsFromCSV: 
# Take in filenames of CSVs and return a dataframe of Date, Tweet, Keyword, and Spanish Word 
def pullTweetsFromCSV( tweetFileList, returnColumns = None, fileEncoding = 'UTF-8' ):
    # First we're going to use this space to declare the columns we want to keep. 
    # These will be default columns, unless given others
    if returnColumns is None:
        returnColumns = [
            'Date',
            'Tweet',
            'Keyword',
            'Spanish'
        ]

    # Declare the df to append, then return
    tweet_df = pd.DataFrame( columns = returnColumns)

    if type(tweetFileList) == type(''): tweetFileList = [tweetFileList] 

    for aFile in tweetFileList:
        temp_df = pd.read_csv(aFile, encoding=fileEncoding)

        tweet_df = tweet_df.append( temp_df, ignore_index=True )

    return tweet_df


