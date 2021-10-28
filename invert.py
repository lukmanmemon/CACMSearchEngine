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

# Parse file and separate into individual documents
with open("cacm.all") as file:
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
        for word in line.split():
            stripped_word = word.strip(string.punctuation).lower()
            if stripped_word in check_duplicates:
                continue
            
            check_duplicates.append(stripped_word)
            terms_list.append(stripped_word)
    check_duplicates.clear()

# Remove all occurences of '.W' in list
terms_list[:] = (value for value in terms_list if value != 'W')

# Get stop words and put into list
with open("stopwords.txt", 'r') as file_stopwords:
    for line in file_stopwords:
        stopwords_list.extend(line.split())

# Toggle stopwords and stemming components
stopwords_on = False
stemming_on = False
ps = PorterStemmer()

# Take command line arguments to toggle stopwords/stemming
toggle_stopwords = sys.argv[1]
toggle_stemming = sys.argv[2]

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
write_file_dict = open("dict.txt","w")
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
            title_list[title_index] = line
            prev_line_starts_with = False
        if line.startswith('.T'):
            prev_line_starts_with = True
    title_index = title_index + 1

# Add terms to postings list with ID, TF, positions
postings_list = {}
id = 1
position = 0
position_counter = {}
tf_counter = {}

for document in document_list_posting:
    
    for line in document:
        for word in line.split():
            if word == '.W':
                continue
            stripped_word = word.strip(string.punctuation).lower()

            if stemming_on:
                stripped_word = ps.stem(stripped_word)

            if stripped_word in tf_counter:
                tf_counter[stripped_word] = tf_counter[stripped_word] + 1
            else:
                tf_counter[stripped_word] = 1

            position = position + 1
            if stripped_word in position_counter:
                position_counter[stripped_word].append(position)
            else:
                position_counter[stripped_word] = [position]
            
            if stripped_word not in postings_list:
                postings_list[stripped_word] = {id: [title_list[id], tf_counter[stripped_word], position_counter[stripped_word]]}

            if stripped_word in postings_list and id not in postings_list[stripped_word].keys():
                postings_list[stripped_word][id] = [title_list[id], tf_counter[stripped_word], position_counter[stripped_word]]

            if stripped_word in postings_list and id in postings_list[stripped_word].keys():
                postings_list[stripped_word][id] = [title_list[id], tf_counter[stripped_word], position_counter[stripped_word]]

    id = id + 1
    position = 0
    for key in tf_counter:
        tf_counter[key] = 0

    for key in position_counter:
        position_counter[key] = []

# sorted(postings_list.items(), key=lambda e: e[1][1], reverse=True)

# Open txt file and write postings list to it
write_file_postings = open("postings.txt","w")
write_file_postings.write( str(postings_list) )
write_file_postings.close()