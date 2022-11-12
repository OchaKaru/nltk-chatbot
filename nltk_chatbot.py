# -*- coding: utf-8 -*-
"""nltk_chatbot.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/gist/OchaKaru/805aaa3af1200d7bce9dcc863f8e6051/nltk_chatbot.ipynb
"""

import numpy as np
import nltk
import string
import random

f = open('corpus.txt', 'r', errors = 'ignore')
raw_doc = f.read()
raw_doc = raw_doc.lower()
nltk.download('punkt') #punkt tokenizer
nltk.download('wordnet') #using wordnet dictionary
nltk.download('omw-1.4')

sentence_tokens = nltk.sent_tokenize(raw_doc)
word_tokens = nltk.word_tokenize(raw_doc)

word_tokens[:2]

lemmer = nltk.stem.WordNetLemmatizer()
def LemTokens(tokens):
  return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
def LemNormalize(text):
  return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

GREET_INPUTS = ("hello", "hi", "greetings", "sup", "what's up", "hey",)
GREET_RESP = ["hi", "hey", "hi there", "hello", "sup", "how you doin'"]
def greet(sentence):
  for word in sentence.split():
    if word.lower() in GREET_INPUTS:
      return random.choice(GREET_RESP)

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def response(user_response):
  robo1_response = ''
  TfidfVec = TfidfVectorizer(tokenizer = LemNormalize,  stop_words = 'english')
  tfidf = TfidfVec.fit_transform(sentence_tokens)
  vals = cosine_similarity(tfidf[-1], tfidf)
  idx = vals.argsort()[0][-2]
  flat = vals.flatten()
  flat.sort()
  req_tfidf = flat[-2]
  if(req_tfidf == 0):
    robo1_response = robo1_response + "I am sorry! I don't understand you"
    return robo1_response
  else:
    robo1_response = robo1_response + sentence_tokens[idx]
    return robo1_response

flag = True
print("Bot: Hello.")
while(flag == True):
  user_response = input()
  user_response = user_response.lower()
  if(user_response != "bye"):
    if(greet(user_response) != None):
      print("Bot: " + greet(user_response))
    else:
      sentence_tokens.append(user_response)
      word_tokens = word_tokens + nltk.word_tokenize(user_response)
      final_words = list(set(word_tokens))
      print("Bot: ", end="")
      print(response(user_response))
      sentence_tokens.remove(user_response)
  else:
    flag = False