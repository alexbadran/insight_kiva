from bs4 import BeautifulSoup   
import re
from nltk.corpus import stopwords # Import the stop word list
from sklearn.feature_extraction.text import CountVectorizer as cv
from sklearn.feature_extraction.text import TfidfVectorizer as tfidf

import pandas as pd
import numpy as np
import ast

# no need to normalize, since Vectorizer will return normalized tf-idf
from scipy.spatial.distance import cosine

def fSearch(dfLoans,search):
	

	# If there is a search term, obtain the clean words from the search description.
	if search:
		dfSearch = dfLoans
		descriptions = [str(e) for e in dfSearch['descriptions_clean']]
		descriptions.append(search)
		
		# Vectorise the descriptions using bag of words.
		vect_words =bag_of_words(descriptions)
		del descriptions[-1]

		vect_words_list = [vect_words[x,:] for x in range(vect_words.shape[0]-1)]

		#vect_words_list
		dfSearch['vect_words'] = vect_words_list

		# Obtain a score taking the log transform of the cosine similarity for each word.
		score = []
		score = [-np.log(cosine(vect_words[x],vect_words[vect_words.shape[0]-1])) for x in range(vect_words.shape[0]-1)]
		dfSearch['search_score'] = score
		
		# Remove NAs (cosequence of log) and return the sorted search.
		dfSearch = dfSearch[~dfSearch['search_score'].isnull()]
		dfSearch = dfSearch.sort(['search_score'],ascending=[0])
	else:
		dfSearch = dfLoans
		dfSearch['search_score'] = 0

	return dfSearch


def review_to_words( raw_review ):
    # Function to convert a raw review to a string of words
    # The input is a single string (a raw movie review), and 
    # the output is a single string (a preprocessed movie review)
    #
    # 1. Remove HTML
    review_text = BeautifulSoup(raw_review).get_text() 
    #
    # 2. Remove non-letters        
    letters_only = re.sub("[^a-zA-Z]", " ", review_text) 
    #
    # 3. Convert to lower case, split into individual words
    words = letters_only.lower().split()                             
    #
    # 4. In Python, searching a set is much faster than searching
    #   a list, so convert the stop words to a set
    stops = set(stopwords.words("english"))                  
    # 
    # 5. Remove stop words
    meaningful_words = [w for w in words if not w in stops]   
    #
    # 6. Join the words back into one string separated by space, 
    # and return the result.
    return( " ".join( meaningful_words )) 

def bag_of_words( clean_train_reviews ):
    # Initialize the "CountVectorizer" object, which is scikit-learn's
    # bag of words tool.  
    vectorizer = tfidf(analyzer = "word",   \
                                 tokenizer = None,    \
                                 preprocessor = None, \
                                 stop_words = None,   \
                                 max_features = 5000) 

    # fit_transform() does two functions: First, it fits the model
    # and learns the vocabulary; second, it transforms our training data
    # into feature vectors. The input to fit_transform should be a list of 
    # strings.
    train_data_features = vectorizer.fit_transform(clean_train_reviews)

    # Numpy arrays are easy to work with, so convert the result to an 
    # array
    train_data_features = train_data_features.toarray()
    
    # Take a look at the words in the vocabulary
    vocab = vectorizer.get_feature_names()

    # Sum up the counts of each vocabulary word
    dist = np.sum(train_data_features, axis=0)

    # For each, print the vocabulary word and the number of times it 
    # appears in the training set
#    for tag, count in zip(vocab, dist):
#        print count, tag
        
    return train_data_features
