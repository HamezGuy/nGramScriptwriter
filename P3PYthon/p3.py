from collections import Counter, OrderedDict
from itertools import product
import matplotlib.pyplot as plt
from random import choices

import numpy as np
import string
import sys
import re
import math



with open('VforVendetta.txt', encoding='utf-8') as f:
    data = f.read()
# len(data)

data = data.lower()
data = data.translate(str.maketrans('', '', string.punctuation))
data = re.sub('[^a-z]+', ' ', data)
data = ' '.join(data.split(' '))

allchar = ' ' + string.ascii_lowercase

unigram = Counter(data)
unigram_prob = {ch: round((unigram[ch]) / (len(data)), 4) for ch in allchar}

uni_list = [unigram_prob[c] for c in allchar]

def ngram(n):
    # all possible n-grams
    d = dict.fromkeys([''.join(i) for i in product(allchar, repeat=n)],0)
    # update counts
    d.update(Counter([''.join(j) for j in zip(*[data[i:] for i in range(n)])]))
    return d

bigram = ngram(2)  # c(ab)



bigram_prob_smoothed = { c: ( bigram[c] + 1 ) / ( unigram[c[0]] + 27) for c in bigram}

bigram_prob_smoothed = { c: round(bigram_prob_smoothed[c], 4) for c in bigram_prob_smoothed} 


for k in bigram_prob_smoothed:
    if(bigram_prob_smoothed[k] < .0001):
        bigram_prob_smoothed[k] = .0001

countNumber = 0
lineCount = 0
for k in bigram_prob_smoothed:
    if countNumber < 26:
        lineCount += countNumber
        countNumber + 1
    else:
        bigram_prob_smoothed[k] = 1-lineCount
        lineCount = 0
        countNumber = 0

    

for k in unigram:
    print(unigram_prob[k], ",", end='')
    
print("\n")

countNumber = 0

#
#for k in bigram_prob_smoothed:
   # if countNumber < 26:
    #    number = round(bigram_prob_smoothed[k], 4)
 #       print(number, ",", end='')
 #       countNumber += 1
 #   else:
   #     number = round(bigram_prob_smoothed[k], 4)
   #     print(number, ",", end='')
  #      print()
   #     countNumber = 0

trigram = ngram(3)
trigram_prob = {c: (trigram[c]) / (bigram_prob_smoothed[c[:2]]) for c in trigram} #used to be just normal bigram


def gen_bi(c):
    w = [bigram_prob_smoothed[c + i] for i in allchar]
    return choices(allchar, weights=w)[0]
    

def gen_tri(ab):
    w_tri = [trigram_prob[ab + i] for i in allchar]
    return choices(allchar, weights=w_tri)[0]   


def gen_sen(c, num):
    res = c + gen_bi(c)
    for i in range(num - 2):
        if bigram[res[-2:]] == 0:
            t = gen_bi(res[-1])
        else:
            t = gen_tri(res[-2:])
        res += t
    return res


example_sentence = gen_sen('h', 100)


with open('script.txt', encoding='utf-8') as f:
    young = f.read() 

dict2 = Counter(young)
likeli = [dict2[c] / len(young) for c in allchar]


post_young = [round(likeli[i] / (likeli[i] + uni_list[i]), 4) for i in range(27)]
post_hugh = [1 - post_young[i] for i in range(27)]

pA = [0.0923, 0.0027, 0.0129, 0.0083, 0.005, 0.0014, 0.0096, 0.0096, 0.0027, 
0.0021, 0.1306, 0.0146, 0.0042, 0.0097, 0.0029, 0.0029, 0.0097, 0.2221, 0.0027, 0.0027, 0.0014, 
0.0075, 0.0223, 0.0084, 0.1361, 0.0096, 0.266]

i = 0
for x in pA:
    num = (post_young[i] * x)/(post_young[i] * x + (1-post_young[i]) * post_young[i])
    print(num, ",", end='', sep='')
    i = i + 1
    

    