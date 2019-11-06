from collections import defaultdict
from gensim import corpora
from gensim import models
from gensim import similarities

documents = [
    "The crucifixion was created in the 14th century  circa 1350-1359 experts are not sure exactly when but it is estimated that it was around 1352",
    "honestly this did not stand out much compared to the many depictions of the crucifixion the only original part was the swan in the birds overlooking it as Christ is supposed to",
    "what strikes me about the crucifixion is that some idiot tried to buy this for 100 Bitcoin that's almost $800,000 absolutely insane I don't understand it",
    "what's really interesting to me about this crucifixion painting is that there is this little bird with a nest on the top and I keep trying to figure out what that's trying to symbolize is the bird God and he is guarding over his children by sending his one and only son Jesus Christ to die for our sins or is the bird Mary Magdalene who's also you know that her son go off and die for this purpose so that's that's a really interesting question for me",
    "the crucifixion is based on a wood panel with gold leaf and be inscribed images that you see the gold brings out the Holiness and spirituality associated with this imagery and prepares it for its placement in a high-end esteem Church",
]

# remove common words and tokenize
stoplist = set('for a of the and to in'.split())
texts = [
    [word for word in document.lower().split() if word not in stoplist]
    for document in documents
]

# remove words that appear only once
frequency = defaultdict(int)
for text in texts:
    for token in text:
        frequency[token] += 1

texts = [
    [token for token in text if frequency[token] > 1]
    for text in texts
]

dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]
lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=2)
doc = "when was it created?"
vec_bow = dictionary.doc2bow(doc.lower().split())
vec_lsi = lsi[vec_bow]  # convert the query to LSI space
print(vec_lsi)

index = similarities.MatrixSimilarity(lsi[corpus])
print(index)
index.save('/tmp/deerwester.index')
index = similarities.MatrixSimilarity.load('/tmp/deerwester.index')

sims = index[vec_lsi]  # perform a similarity query against the corpus
sims = sorted(enumerate(sims), key=lambda item: -item[1])
print(sims)
for i, s in sims:
    print(s, documents[i])