from collections import defaultdict
from gensim import corpora
from gensim import models
from gensim import similarities
import uuid
Played_audios = set()
# Retrieve all (id,audio_text) for all audios on the current pi.
def retrieve_audio_texts():
    piId = hex(uuid.getnode())
    print(piId)
    # audio_ids, audio_texts = retrieveByRasberryPiId(piId)
    audio_ids, audio_texts = [0,1,2,3,4], [
        "The crucifixion was created in the 14th century  circa 1350-1359 experts are not sure exactly when but it is estimated that it was around 1352",
        "honestly this did not stand out much compared to the many depictions of the crucifixion the only original part was the swan in the birds overlooking it as Christ is supposed to",
        "what strikes me about the crucifixion is that some idiot tried to buy this for 100 Bitcoin that's almost $800,000 absolutely insane I don't understand it",
        "what's really interesting to me about this crucifixion painting is that there is this little bird with a nest on the top and I keep trying to figure out what that's trying to symbolize is the bird God and he is guarding over his children by sending his one and only son Jesus Christ to die for our sins or is the bird Mary Magdalene who's also you know that her son go off and die for this purpose so that's that's a really interesting question for me",
        "the crucifixion is based on a wood panel with gold leaf and be inscribed images that you see the gold brings out the Holiness and spirituality associated with this imagery and prepares it for its placement in a high-end esteem Church",
    ]
    return audio_ids, audio_texts

# Clean up text by removing stop words and words that may not be relevant.
def clean_audio_texts(documents):
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
    return texts

def create_lsi_model(texts):
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=2)
    return dictionary, corpus, lsi


def find_unique_audio(sims,TOTAL_AUDIOS):
  #if len(Played_audios) == TOTAL_AUDIOS:
    #acknowledge repetition
    #return "repeated_audio.mp4" #says something like "Would you like to hear about this again?"

  #most similar id
  id = audio_ids[sims[0][0]]


  for idx in sims:
    #extract next most similar id
    id = audio_ids[sims[idx][idx]] #move to next similar audio, not sure why it's a 2d vector

    if id not in Played_audios:
        return id

    #error("all audios have been played")


  #id is now the most similar, non-repeated audio



def get_best_answer_audio_id(question):
    # Retrieve all texts related to the current art piece.

    audio_ids, audio_texts = retrieve_audio_texts()
    texts = clean_audio_texts(audio_texts)
    dictionary, corpus, lsi = create_lsi_model(texts)
    vec_bow = dictionary.doc2bow(question.lower().split())
    vec_lsi = lsi[vec_bow]  # convert the query to LSI space
    index = similarities.MatrixSimilarity(lsi[corpus])
    index.save('/tmp/deerwester.index')
    index = similarities.MatrixSimilarity.load('/tmp/deerwester.index')
    sims = index[vec_lsi]  # perform a similarity query against the corpus
    TOTAL_AUDIOS = sims.len()
    sims = sorted(enumerate(sims), key=lambda item: -item[1])
    id = find_unique_audio(sims,TOTAL_AUDIOS)
    Played_audios.add(id) #marks audio as played

    #print(sims)
    # for i, s in sims:
    #     print(s, audio_texts[i])


# get_best_answer_audio_id("what strikes you about it?")
