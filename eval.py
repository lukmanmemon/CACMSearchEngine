from nltk.tokenize import word_tokenize

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


file_query.close()