import time
import json
import ast
import sys
from nltk.stem import PorterStemmer

with open('dict.txt') as dict_file:
    dict_data = dict_file.read()

with open('postings.txt') as postings_file:
    postings_data = postings_file.read()

# Convert from string to dictionary
dictionary = ast.literal_eval(dict_data)

# Convert postings list from string to dictionary
postings_list = ast.literal_eval(postings_data)
    
total_time_elapsed = 0
counter = 0
term_input = ""

stemming_on = False
ps = PorterStemmer()
toggle_stemming = sys.argv[1]

if toggle_stemming == 'ON':
    stemming_on = True

while term_input != 'ZZEND':
    term_input = input("Enter a term: ")
    if term_input == 'ZZEND':
        break

    # Stem search keyword
    if stemming_on == True:
        term_input = ps.stem(term_input)

    if term_input not in dictionary:
        print("\n--- Please enter a valid term ---\n")
        continue

    # Print term information
    start = time.time()
    print("\nDocument frequency: " + str(dictionary[term_input]))
    print("Postings list: \n" + str(postings_list[term_input]))
    
    end = time.time()

    # Calculate and print time for each output
    time_elapsed = end - start
    total_time_elapsed = total_time_elapsed + time_elapsed
    counter = counter + 1

    print("\nTime to output the result: " + str(time_elapsed) + " seconds\n")

# Calculate and print average time elapsed
if counter > 0:
    average_time_elapsed = total_time_elapsed / counter
    print("\nAverage time per output: " + str(average_time_elapsed) + " seconds")


dict_file.close()
postings_file.close()