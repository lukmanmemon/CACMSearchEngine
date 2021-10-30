import ast
import math
import numpy as np
import nltk
nltk.download('punkt')

with open('dict.txt') as dict_file:
    dict_data = dict_file.read()

with open('postings.txt') as postings_file:
    postings_data = postings_file.read()

# Convert from string to dictionary
dictionary = ast.literal_eval(dict_data)

# Convert postings list from string to dictionary
postings_list = ast.literal_eval(postings_data)

# Get user input
query_input = input("\nEnter a query: ").lower()

# Split input query into tokens
query_tokens = nltk.word_tokenize(query_input)

# Filter list to keep terms that are in dictionary
query_terms = [word for word in query_tokens if word in dictionary]
sorted_query_terms = sorted(query_terms)

# Add idf of query terms to dictionary
terms_idf = {}
for word in sorted_query_terms:
    df = dictionary[word]
    idf = math.log(3204 / df, 10)
    terms_idf[word] = idf