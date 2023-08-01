# Imports
import math
import chardet

# --------------------------------------------------------------------------------------------------------------
# Function for finding encoding of a file
def find_encoding(fname):
    # Read the file in binary mode
    r_file = open(fname, 'rb').read()
    # Detect the file's character encoding
    result = chardet.detect(r_file)
    charenc = result['encoding']
    return charenc

def load_vocab():
    vocab = {}
    with open('tf-idf/vocab.txt', 'r') as f:
        vocab_terms = f.readlines()
    with open('tf-idf/idf-values.txt', 'r') as  f:
        idf_values = f.readlines()
    
    for (term,idf_value) in zip(vocab_terms, idf_values):
        vocab[term.strip()] = int(idf_value.strip())
    return vocab

def load_documents():
    documents = []
    with open('tf-idf/documents.txt', 'r') as f:
        documents = f.readlines()
    documents = [document.strip().split() for document in documents]

    print('Number of documents: ', len(documents))
    print('Sample document: ', documents[0])
    return documents

def load_inverted_index():
    inverted_index = {}
    with open('tf-idf/inverted-index.txt', 'r') as f:
        inverted_index_terms = f.readlines()

    for row_num in range(0,len(inverted_index_terms),2):
        term = inverted_index_terms[row_num].strip()
        documents = inverted_index_terms[row_num+1].strip().split()
        inverted_index[term] = documents
    
    print('Size of inverted index: ', len(inverted_index))
    return inverted_index

# function to load index( question names)
def load_index():
    index = []
    with open('./qData/index.txt', 'r') as f:
        index = f.readlines()
    return index    

# funciton to load links 
def load_links():
    links = []
    with open('./qData/Qlink.txt', 'r') as f:
        links = f.readlines()
    print('number of links: ', len(links)) 
    return links
# ----------------------------------------------------------------------------------------------------------

# Load vocabulary and IDF values
vocab_idf_values = load_vocab()

# Load documents
documents = load_documents()

# Load inverted index
inverted_index = load_inverted_index()

# Load links
links = load_links()

# Load index
index = load_index()

# -------------------------------------------------------------------------------------------------------------

# Function to get the term frequency (TF) dictionary for a given term
def get_tf_dictionary(term):
    tf_values = {}
    if term in inverted_index:
        # Calculate the TF for each document containing the term
        for document in inverted_index[term]:
            if document not in tf_values:
                tf_values[document] = 1
            else:
                tf_values[document] += 1
        
        # Normalize the TF values by dividing by the total number of words in each document

        for document in tf_values:
            tf_values[document] /= len(documents[int(document)])

    return tf_values

# Function to get the IDF value for a given term
def get_idf_value(term):
    return math.log(len(documents) / vocab_idf_values[term])

# ---------------------------------------------------------------------------------------------------------------------------------

# Function to calculate and print the sorted order of documents based on TF-IDF scores
def calculate_sorted_order_of_documents(query_terms):
    potential_documents = {}
    for term in query_terms:
        try:
            # Check if the term is present in the vocabulary
            if vocab_idf_values[term] == 0:
                # Skip if IDF is 0 (i.e., the term doesn't exist in the vocabulary)
                continue
        except:
            # Error: The term is not found in the vocabulary
            print('Term not found in vocab: ', term)

        # Calculate the TF-IDF score for each document containing the term
        tf_values_by_document = get_tf_dictionary(term)
        idf_value = get_idf_value(term)
        # print(term, tf_values_by_document, idf_value)
        
        for document in tf_values_by_document:
            if document not in potential_documents:
                # Initialize the TF-IDF score for the document
                potential_documents[document] = tf_values_by_document[document] * idf_value
            else:
                # Accumulate the TF-IDF scores for documents with multiple query terms
                potential_documents[document] += tf_values_by_document[document] * idf_value


    # Divide the accumulated TF-IDF scores by the number of query terms to get the average score
    for document in potential_documents:
        potential_documents[document] /= len(query_terms)  

    # Sort the potential_documents dictionary based on the TF-IDF scores in descending order
    potential_documents = dict(sorted(potential_documents.items(), key=lambda item: item[1], reverse=True))
    print(potential_documents)

    # printing index(question names) and  links  of potential_documents
    i=0
    question_list={}
    for document in potential_documents:
        print(index[int(document)],". link: ",links[int(document)])
        question_list[index[int(document)]]=links[int(document)]
        i+=1
        if(i==20):
            break
    return question_list    
        
        

# Get the query from the user and tokenize it
query_string = input('Enter your query: ')
query_terms = [term.lower() for term in query_string.strip().split()]

# Print the query terms
print(query_terms)

# Call the function to calculate and print the sorted order of documents based on TF-IDF scores
calculate_sorted_order_of_documents(query_terms)
