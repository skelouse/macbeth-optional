import requests
import matplotlib.pyplot as plt
import numpy as np

# not implemented
def get_stop_words():
    import nltk
    from nltk.corpus import stopwords
    nltk.download('stopwords')
    old_stopwords = ['vpon', 'vs', 'vp', 'Ile', 'haue', 'thou', 'thy', 'thee', 'doe']
    return list(nltk.corpus.stopwords.words('english')) + old_stopwords

with open('./mac.txt', 'r') as f:
    macbeth = f.read()

# a 2D dictionary where each name is a key to the value being a dictionary of word counts
"""
Example

{'Macbeth': {
    'hello': 3,
    'goodbye': 2
    },
'Alfred' : {
    'good': 10,
    'bad': 6
    }
}
"""
dict_of_names = {}

# Splitting the whole text by two spaces, because in the text
# there is 2-4 spaces before someone speaks
for i in macbeth.split('  '):
    try:
        # After a name there is a period, so this finds the name
        name = i[0:i.index('.')]
        
        # Replacing the leading spaces with nothing to clean the name
        # case being 3/4 spaces before rather than 2
        name = name.replace(' ', '')

        # The spoken words by _name_ i.e the text after the period
        spoken = i[i.index('.')+2::]

        # There were a couple outliers that had long names of text
        # This removes that
        if len(name) < 20:
            try:
                dict_of_names[name]  # checking if the name is in the dictionary yet
                for word in spoken.split(' '):
                    try:
                        dict_of_names[name][word] += 1
                    except KeyError:
                        dict_of_names[name][word] = 1
            except KeyError:
                # Creates the empty dictionary to the name if line 49 has a key error
                dict_of_names[name] = {}
    except ValueError:
        pass

removals = []

# sorting the spoken words for each name
for name in dict_of_names.items():
    if name[1]:
        dict_of_names[name[0]] = sorted(name[1].items(), key=lambda x: x[1], reverse=True)[0:25]
    else:
        removals.append(name[0])

# removing names with no word counts
# technically shouldn't be a thing, but the parsing is not 100%
for i in removals:
    dict_of_names.pop(i)

def graph(use_words, title):
    'graphs the words'
    word_list, quantities= list(zip(*use_words))
    x = np.arange(len(word_list))
    plt.figure(figsize=(15, 10))
    plt.title(title)
    plt.bar(x, quantities)
    plt.xticks(x, word_list, rotation=30)
    plt.xlabel('Words')
    plt.ylabel('Count')
    plt.show()

def query():
    'takes user input, and creates a graph for the selected name'
    select = input('selection >').title()
    try:
        graph(dict_of_names[select], select)
    except KeyError:
        print('Invalid name!')

print("Optional names are -", dict_of_names.keys())
while True:
    query()