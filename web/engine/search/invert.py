import time
import json
import string
import sys
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

start = time.time()

dictionary = {}
document_list = []
terms_list = []
stopwords_list = []


def invert(toggle_stopwords, toggle_stemming):




    # Parse file and separate into individual documents
    with open("search/cacm.all") as file:
        for line in file:
            if line.startswith('.I'):
                tmp = []
                tmp.append(line.strip())
                for line in file:
                    if line.startswith('.N'):
                        document_list.append(tmp)
                        break
                    tmp.append(line.strip())

    # Get non-duplicate terms from each document's title/abstract sections
    for document in document_list:        
        start = document.index('.T')
        stop = document.index('.B')
        shortened_document = document[start+1:stop]

        check_duplicates = []

        for line in shortened_document:
            for word in word_tokenize(line):
                lowercase_word = word.lower()
                if lowercase_word in check_duplicates:
                    continue
                
                check_duplicates.append(lowercase_word)
                terms_list.append(lowercase_word)
        check_duplicates.clear()

    # Remove all occurences of '.W' in list
    terms_list[:] = (value for value in terms_list if value != 'W')

    # Get stop words and put into list
    with open("search/stopwords.txt", 'r') as file_stopwords:
        for line in file_stopwords:
            stopwords_list.extend(line.split())

    # Toggle stopwords and stemming components
    stopwords_on = False
    stemming_on = False
    ps = PorterStemmer()


    if toggle_stopwords == 'ON':
        stopwords_on = True
    if toggle_stopwords == 'OFF':
        stopwords_on = False
    if toggle_stemming == 'ON':
        stemming_on = True
    if toggle_stemming == 'OFF':
        stemming_on = False

    # Put terms into dictionary
    for term in terms_list:
        # Enable stop word removal
        if term in stopwords_list and stopwords_on:
            continue

        # Enable Porter Stemming
        if stemming_on:
            term = ps.stem(term)
            
        if term in dictionary:
            dictionary[term] += 1
        else:
            dictionary[term] = 1

    # Sort dictionary items
    dictionary_items = dictionary.items()
    sorted_items = sorted(dictionary_items)

    # List of tuples to dictionary 
    sorted_dictionary = {k:v for k,v in sorted_items}

    # Open txt file and write dictionary to it
    write_file_dict = open("search/dict.txt","w")
    write_file_dict.write( str(sorted_dictionary) )

    file_stopwords.close()
    write_file_dict.close()
    file.close()

    # Get ID, title, abstract sections for postings list
    document_list_posting = []
    for document in document_list:
        start = document.index('.T')        
        stop = document.index('.B')
        document_list_posting.append(document[start+1:stop])

    # Get title from documents
    prev_line_starts_with = False
    title_list = {}
    title_index = 1
    for document in document_list:
        for line in document:
            if prev_line_starts_with == True:
                if line == '.W':
                    title_list[title_index] = "No title"
                else:
                    title_list[title_index] = line
                prev_line_starts_with = False
            if line.startswith('.T'):
                prev_line_starts_with = True
        title_index = title_index + 1

    # Get authors from documents
    author_list = {}
    author_index = 0
    for document in document_list:
        author_index = author_index + 1
        if '.A' not in document:
            author_list[author_index] = "No author(s)"
            continue

        shortened_document = []
        start = document.index('.A')
        if '.K' in document:
            stop = document.index('.K')
            shortened_document = document[start+1:stop]
        elif '.C' in document:
            stop = document.index('.C')
            shortened_document = document[start+1:stop]
        elif '.X' in document: 
            stop = document.index('.X')
            shortened_document = document[start+1:stop]
        else:
            shortened_document = document[start+1:]
        
        for line in shortened_document:
            if author_index in author_list:
                author_list[author_index] = author_list[author_index] + " " + line
            else: 
                author_list[author_index] = line

    # Add terms to postings list with ID, TF, positions
    postings_list = {}
    id = 1
    position = 0
    position_counter = {}
    tf_counter = {}

    for document in document_list_posting:
        
        for line in document:
            
            for word in word_tokenize(line):
                if word == '.W' or word in string.punctuation:
                    continue
                lowercase_word = word.lower()

                if stemming_on:
                    lowercase_word = ps.stem(lowercase_word)

                if lowercase_word in tf_counter:
                    tf_counter[lowercase_word] = tf_counter[lowercase_word] + 1
                else:
                    tf_counter[lowercase_word] = 1

                position = position + 1
                if lowercase_word in position_counter:
                    position_counter[lowercase_word].append(position)
                else:
                    position_counter[lowercase_word] = [position]
                
                if lowercase_word not in postings_list:
                    postings_list[lowercase_word] = {id: [title_list[id], tf_counter[lowercase_word], position_counter[lowercase_word]]}

                if lowercase_word in postings_list and id not in postings_list[lowercase_word].keys():
                    postings_list[lowercase_word][id] = [title_list[id], tf_counter[lowercase_word], position_counter[lowercase_word]]

                if lowercase_word in postings_list and id in postings_list[lowercase_word].keys():
                    postings_list[lowercase_word][id] = [title_list[id], tf_counter[lowercase_word], position_counter[lowercase_word]]

        id = id + 1
        position = 0
        for key in tf_counter:
            tf_counter[key] = 0

        for key in position_counter:
            position_counter[key] = []

    # Open txt file and write postings list to it
    write_file_postings = open("search/postings.txt","w")
    write_file_postings.write( str(postings_list) )
    write_file_postings.close()
    return (title_list, author_list)