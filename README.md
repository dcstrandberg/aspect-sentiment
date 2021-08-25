Project for the purpose of learning aspect based sentiment analysis -- eventually to be used in analyzying tweet data. 

Link for spaCy module & documentation:
https://spacy.io/usage/linguistic-features

Note: In order to run these programs, you'll need to download the english & spanish language models that are used by spaCy, using the following commands:

English:
python -m spacy download en_core_web_sm

Spanish:
python -m spacy download es_core_news_sm


----

# TODOs:
 
**./aspect-sentiment.py**
- Pipe in list of tweets
- Pull out aspects & descriptions
   - Need to modify algo to inclue "not"s and whatnot
- Add sentiment to each of the words
- Potentially add Named Entities, to identify things like competitors, etc. 
   - Look into whether there are pre-existing lists of Named Entities

- Run all the words through frequency & see if that's more interesting
   - Probably still need to finish Freq Count file, to include "Words of Interest" list
   - Probably need to add in Lemma-tization, before grouping words?
   - This would also be where to add in Pronoun Resolution


**What are the other things that need to be done?**