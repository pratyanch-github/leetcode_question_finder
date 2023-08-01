import chardet
import re

# function for finding encoding
def find_encoding(fname):
    r_file = open(fname, 'rb').read()
    result = chardet.detect(r_file)
    charenc = result['encoding']
    return charenc

# function to tokenize text
def tokenize_text(text):
    # Tokenize the text into alphabetic words
    tokens = re.findall(r'\b[A-Za-z]+\b', text)
    return tokens

def preprocess(document_text):
    # remove the leading numbers from the string, remove not alpha numeric characters, make everything lowercase
    terms = [term.lower() for term in document_text.strip().split()[1:]]
    return terms

filename = './qData/index.txt'
my_encoding = find_encoding(filename)

with open(filename, 'r', encoding=my_encoding) as f:
    lines = f.readlines()

vocab = {}
documents = []
for index, line in enumerate(lines):
    # read statement and add it to the line and then preprocess
    tokens = preprocess(line)
    filename = f'./qData/{index+1}/{index+1}.txt'
    my_encoding = find_encoding(filename)
    with open(filename, 'r', encoding=my_encoding) as f:
        text = f.read()  # Read the file as a single string, not lines
    tokens.extend(tokenize_text(text))
    documents.append(tokens)
    tokens = set(tokens)
    for token in tokens:
        if token not in vocab:
            vocab[token] = 1
        else:
            vocab[token] += 1


# Sort the vocab by the values in descending order
vocab = dict(sorted(vocab.items(), key=lambda item: item[1], reverse=True))

print('Number of documents:', len(documents))
print('Size of vocab:', len(vocab))
print('Sample document:', documents[0], documents[1], documents[2])

# Save the vocab in a text file
with open('tf-idf/vocab.txt', 'w', encoding='utf-8') as f:
    for key in vocab.keys():
        f.write("%s\n" % key)  # key means the word

# Save the idf values in a text file
with open('tf-idf/idf-values.txt', 'w', encoding='utf-8') as f:
    for key in vocab.keys():
        f.write("%s\n" % vocab[key])  # vocab[key] means frequency of the word in all documents

# Save the documents in a text file
with open('tf-idf/documents.txt', 'w', encoding='utf-8') as f:
    for document in documents:
        f.write("%s\n" % ' '.join(document))  # document contains the problem names without stopwords and numeric values at front

# Now we are creating a dictionary which contains, token ---> index of document in the documents
# While vocab contains, token ---> frequency of token in all documents
# Inverted_index[token].size will give the number of documents in which token is present
# Inverted_index[token] will give the list of indices of documents in which token is present
# Documents.size will give the number of documents
inverted_index = {}   # inverted index
for index, document in enumerate(documents):
    for token in document:
        if token not in inverted_index:
            inverted_index[token] = [index]
        else:
            inverted_index[token].append(index)

# Save the inverted index in a text file
with open('tf-idf/inverted-index.txt', 'w', encoding='utf-8') as f:
    for key in inverted_index.keys():
        f.write("%s\n" % key)
        f.write("%s\n" % ' '.join([str(doc_id) for doc_id in inverted_index[key]]))
