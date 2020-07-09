import requests
import matplotlib.pyplot as plt
import numpy as np
import nltk
from nltk.corpus import stopwords
#macbeth = requests.get('http://www.gutenberg.org/cache/epub/2264/pg2264.txt').text
nltk.download('stopwords')
old_stopwords = ['vpon', 'vs', 'vp', 'Ile', 'haue', 'thou', 'thy', 'thee', 'doe']

with open('Labs\mod_1\sect_1\mac.txt', 'r') as f:
    macbeth = f.read()

words = {}
stop_words = list(nltk.corpus.stopwords.words('english')) + old_stopwords

num = 0
dict_of_names = {}


for i in macbeth.split('  '):
    try:
        name = i[0:i.index('.')]
        name = name.replace(' ', '')
        spoken = i[i.index('.')+2::]
        if len(name) < 20:
            try:
                dict_of_names[name]
                for word in spoken.split(' '):
                    try:
                        dict_of_names[name][word] += 1
                    except KeyError:
                        dict_of_names[name][word] = 1
            except KeyError:
                dict_of_names[name] = {}
    except ValueError:
        pass

for name in dict_of_names.items():
    dict_of_names[name[0]] = sorted(name[1].items(), key=lambda x: x[1], reverse=True)[0:25]



def graph(use_words):
    word_list, quantities= list(zip(*use_words))
    x = np.arange(len(word_list))
    plt.figure(figsize=(15, 10))
    plt.bar(x, quantities)
    plt.xticks(x, word_list)
    plt.show()

def query():
    select = input('selection >')
    try:
        graph(dict_of_names[select])
        print(dict_of_names[select])
    except KeyError:
        print('Invalid name!')

print("Optional names are -", dict_of_names.keys())
while True:
    query()