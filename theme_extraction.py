import speech_recognition as sr
import nltk
import gensim
from gensim import corpora
from stemming.porter2 import stem
from nltk import PorterStemmer
stemmer = PorterStemmer()
from nltk.stem import WordNetLemmatizer
# nltk.download()
nltk.download('wordnet')


def audio_to_text(fname):
    audio_f = sr.AudioFile(fname)
    r = sr.Recognizer()
    with audio_f as source:
        audio = r.record(source)
    try:
        qst = r.recognize_google(audio)
    except sr.UnknownValueError:
        qst = None
    print(qst)
    return qst

def tokenize_sentences(document):
    sentences = nltk.sent_tokenize(document)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    return sentences


def get_entities(audio_file):
    txt = audio_to_text(audio_file)
    entities = []
    if txt is None:
        return entities
    sentences = tokenize_sentences(txt)
    sentences = [nltk.pos_tag(sent) for sent in sentences]
    for tagged_sentence in sentences:
        for chunk in nltk.ne_chunk(tagged_sentence):
            if chunk[1] == "NN":
                entities.append(chunk[0].lower())
    return entities

# print(get_entities('cat1.wav'))

def lemmatize_stemming(text):
    return stemmer.stem(WordNetLemmatizer().lemmatize(text))
# Tokenize and lemmatize
def preprocess(text):
    result=[]
    for token in gensim.utils.simple_preprocess(text) :
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
            # result.append(lemmatize_stemming(token))
            result.append(token)
    # dataset = [d.split() for d in text]
    dataset = result
    dictionary = corpora.Dictionary([dataset])
    bow_corpus = [dictionary.doc2bow(doc) for doc in [dataset]]
    lda_model =  gensim.models.LdaMulticore(bow_corpus, 
                                   num_topics = 1, 
                                   id2word = dictionary,                                    
                                   passes = 10,
                                   workers = 2)
    for idx, topic in lda_model.print_topics(-1):
        print("Topic: {} \nWords: {}".format(idx, topic ))
        print("\n")
    return lda_model

txt = audio_to_text('crucifixion1.wav')
print(preprocess(txt))