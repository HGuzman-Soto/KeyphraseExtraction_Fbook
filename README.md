# Fbook_KeyphraseExtraction

Repository contains code for data collection and preliminary experiments for my research with Dr. Yudong Liu at WWU 
in the natural language processing lab. 

# Summary

Our research goal is to build NLP models that can identify complex word for non-native english speakers. 
We want to use these models to build language learning applications that are integrated in the user's 
browser to create contextual learning. 

Originally, we pursued keyphrase extraction as a potential direction for our project. The data indicated
that this is a good direction to pursue and so we've shifted towards complex word identification instead.

# Key highlights

* Scrapers that collect all the comments of a Facebook post and automatically scrolls down a user's feed
* Scripts that organize the data and filters to relevant information
* Implemented a keyphrase extraction model (TextRank) from scratch and experimented with changing the grammar 
used.  For example, TextRank only uses noun phrases as grammar, I played around with adding verb phrases.

