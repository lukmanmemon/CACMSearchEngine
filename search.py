import ast
import math
import numpy as np
import collections
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from invert import *

def search(query_input):

    with open('dict.txt') as dict_file:
        dict_data = dict_file.read()

    with open('postings.txt') as postings_file:
        postings_data = postings_file.read()

    # Convert from string to dictionary
    dictionary = ast.literal_eval(dict_data)

    # Convert postings list from string to dictionary
    postings_list = ast.literal_eval(postings_data)

    # Split input query into tokens
    query_tokens = word_tokenize(query_input)

    stemming_on = False
    ps = PorterStemmer()
    toggle_stemming = sys.argv[2]

    if toggle_stemming == 'ON':
        stemming_on = True
        
    # Filter list and apply stemming if needed
    query_terms = []
    for word in query_tokens:
        if stemming_on == True:
            word = ps.stem(word)
        
        if word in dictionary:
            query_terms.append(word)

    sorted_query_terms = sorted(query_terms)
    final_query_terms = []
    [final_query_terms.append(word) for word in sorted_query_terms if word not in final_query_terms]

    # Get query term frequencies
    query_terms_frequencies = {}
    for word in sorted_query_terms:
        if word in query_terms_frequencies:
            query_terms_frequencies[word] = query_terms_frequencies[word] + 1
        else:
            query_terms_frequencies[word] = 1

    # Add idf of query terms to dictionary
    terms_idf = {}
    for word in final_query_terms:
        df = dictionary[word]
        idf = math.log(1 + (3204 / df), 10)
        terms_idf[word] = idf

    # Get vectors for each document and store in dictionary
    document_vectors_dict = {}
    for id in range(1, 3205):
        document_vector = np.zeros((len(final_query_terms)), dtype=float)
        index = 0
        for term in final_query_terms:
            # Get weight by idf * tf
            try:
                document_vector[index] = terms_idf[term] * (1 + math.log(postings_list[term][id][1], 10))
            except KeyError:
                document_vector[index] = 0
            index = index + 1

        document_vectors_dict[id] = document_vector

    # Calculate document vector lengths and store in dictionary
    document_vector_lengths = {}
    for id, vector in document_vectors_dict.items():
        sum = 0
        length = 0
        for weight in vector:
            sum = sum + weight ** 2
            
        length = math.sqrt(sum)
        document_vector_lengths[id] = length

    # Get query vector
    query_vector = np.zeros((len(final_query_terms)), dtype=float)
    q_index = 0
    for term in final_query_terms:
        # Get weight by idf * tf
        query_vector[q_index] = terms_idf[term] * (1 + math.log(query_terms_frequencies[term], 10))
        q_index = q_index + 1

    # Calculate query vector length
    qvector_sum = 0
    for weight in query_vector:
        qvector_sum = qvector_sum + weight ** 2

    qvector_length = math.sqrt(qvector_sum)

    # Calculate cosine similarity
    cosine_similarity = {}
    for id in range(1, 3205):
        similarity_score = 0
        if document_vector_lengths[id] == 0:
            similarity_score = 0
        else :
            similarity_score = (document_vectors_dict[id].dot(query_vector)) / (document_vector_lengths[id] * qvector_length)
        if math.isnan(similarity_score):
            similarity_score = 0

        cosine_similarity[id] = similarity_score

    cosine_similarity_collection = collections.Counter(cosine_similarity)
    # Sort collection of scores in descending order
    sorted_cosine_similarity = cosine_similarity_collection.most_common()
    # Get top K relevant documents
    topK_rel_documents = cosine_similarity_collection.most_common(20)
    rank = 1
    top_ret_documents = []
    for key, value in topK_rel_documents:
        top_ret_documents.append(key)
        rank = rank + 1
    return top_ret_documents
