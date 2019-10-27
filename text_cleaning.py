#!/usr/bin/env python
# coding: utf-8

# In[1]:


from nltk.tokenize import sent_tokenize, word_tokenize, RegexpTokenizer
from nltk.corpus import stopwords

def remove_stop_words(article):
    tokenizer = RegexpTokenizer(r'\w+')
    stop_words = set(stopwords.words('english'))
    
    words = tokenizer.tokenize(article)
    words_without_stop_words = ["" if word in stop_words else word for word in words]
    article_clean = " ".join(words_without_stop_words).strip()
    return article_clean

def only_article_text(article):
    return article.split('words')[1].split('LOAD-DATE:')[0].strip()

def remove_white_space(article):
    return article.strip()


# In[ ]:




