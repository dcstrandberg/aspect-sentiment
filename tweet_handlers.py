from datetime import date
from numpy.lib.npyio import save
import pandas as pd
import twint
from multiprocessing import Process, Queue, Pool, Manager, Lock


# tweetPulls:
# Runs tweet pulling function in multiprocess and returns a simplified tweet_df
def tweetPulls( key_spanish_df ):
    
    m = Manager()
    q = m.Queue() 
    
    p = {}
    qcount = 0

    tweet_df=pd.DataFrame( columns = [
        'Keyword',
        'Spanish',
        'Date',
        'Tweet'
    ])

    for i, aKeyword in enumerate(key_spanish_df['keyword']):            
        print("starting process: ", aKeyword)
        p[i] = Process(target=get_tweets, args=(aKeyword, key_spanish_df['english'][i], q))
        p[i].start()

    
        # join should be done in seperate for loop 
        # reason being that once we join within previous for loop, join for p1 will start working
        # and hence will not allow the code to run after one iteration till that join is complete, ie.
        # the thread which is started as p1 is completed, so it essentially becomes a serial work instead of 
        # parallel
    for i in range(len(key_spanish_df['keyword'])):
        p[i].join()
        print("#" + str(i) + " joined")
    while q.empty() is not True:
        qcount = qcount+1
        queue_top = q.get()

        tweet_df = tweet_df.append(queue_top[0])
        
        print("Q Count " + str(qcount) + " pulled")
                
    #print(q.get())
    
    return tweet_df


# get_tweets:
# Takes a keyword (and english version of that word), a queue object and pipes all the tweet DFs back through that queue
# filterTweets: An optional agrument that potentially filters the returned DF with only tweets that contain the keyword
def get_tweets(keyword, englishWord, q, filterTweets = None):
    all = []
    
    #Create the TWINT config object
    c = twint.Config()
    
    c.Pandas = True
    c.Popular_tweets = True


    c.Hide_output = True
    c.Search = keyword
    c.Limit = 100000
    c.Since = '2019-01-01'

    twint.run.Search(c)

    #Get the tweets
    temp_df = twint.storage.panda.Tweets_df
    
    #If filter parameter == True, remove any entries that don't hvae the actual keyword in the text
    if filterTweets is not None:
        temp_df = temp_df.loc[ temp_df['tweet'].str.contains(filterTweets, case=False) ]
        temp_df = temp_df.reset_index()

    #append on the keyword column
    tempKeywordColumn = [ keyword ] * len( temp_df['tweet'] )
    tempEnglishColumn = [ englishWord ] * len( temp_df['tweet'] )

    temp_df['Keyword'] = tempEnglishColumn
    temp_df['Spanish'] = tempKeywordColumn

    print(keyword, " is length ", str(len(temp_df['tweet'])))


    all.append( temp_df )

    q.put(all)
    print("Put ", keyword)
    
    return 



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


