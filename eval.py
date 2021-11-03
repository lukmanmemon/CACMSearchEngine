from nltk.tokenize import word_tokenize
from search import *

query_list = []
with open("query.text") as file_query:
    for line in file_query:
        if line.startswith('.I'):
            tmp = []
            tmp.append(line.strip())
            for line in file_query:
                if line.startswith('.A') or line.startswith('.N'):
                    query_list.append(tmp)
                    break
                tmp.append(line.strip())

# Get indidiual queries from list and store in dictionary
query_number = 1
query_dictionary = {}
for query in query_list:
    start = query.index('.W')
    query_section = query[start+1:]
    joined_query = ' '.join(query_section)
    query_dictionary[query_number] = joined_query
    query_number = query_number + 1

# Store rel documents for each query in dictionary
qrels_dictionary = {}
with open("qrels.text") as file_rel:
    for line in file_rel:

        # Get query number 
        query_id = line.split(' ', 1)[0]
        if query_id.startswith('0'):
            query_id = query_id[1:]

        # Get document id
        document_id = line.split(' ')[1]
        if document_id.startswith('0'):
            document_id = document_id[1:]

        query_id = int(query_id)
        document_id = int(document_id)
        qrels_dictionary[query_id] = qrels_dictionary.get(query_id, []) + [document_id]

# Get MAP/R-Precision values average over all queries
map_values_list = []
rprecision_value_list = []
for id, query in query_dictionary.items():
    retrieved_documents = search(query)
    try:
        relevant_documents = qrels_dictionary[id]
    except KeyError:
        relevant_documents = []

    relevant_counter = 0
    precision_list = []
    index = 1

    # Calculate precision values and store in list
    for document in retrieved_documents:    
        if document in relevant_documents:
            relevant_counter = relevant_counter + 1
            precision_value = relevant_counter / index
            precision_list.append(precision_value)
        index = index + 1

    if len(relevant_documents) == 0:
        map_value = 0
    else:
        map_value = sum(precision_list) / len(relevant_documents)
    map_values_list.append(map_value)

    if len(relevant_documents) == 0:
        rprecision_value = 0
    else:
        rprecision_value = relevant_counter / len(relevant_documents)
    rprecision_value_list.append(rprecision_value)

final_map_average = sum(map_values_list) / len(query_list)
final_rprecision_average = sum(rprecision_value_list) / len(query_list)
            
print("\nAverage MAP: ", final_map_average)
print("Average R-Precision: ", final_rprecision_average)

file_query.close()
file_rel.close()