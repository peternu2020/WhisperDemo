#!/usr/bin/env python
# coding: utf-8

# In[3]:


import textrazor

textrazor.api_key = "4dd8eb5a209397cc64d8396c34de9769c32b80d47df4a94d83020264"

client = textrazor.TextRazor(extractors=["entities", "topics"])
response = client.analyze_url("http://www.bbc.co.uk/news/uk-politics-18640916")

for entity in response.entities():
    print (entity.id, entity.relevance_score, entity.confidence_score, entity.freebase_types)


# In[ ]:




