from textrazor import TextRazor
# from theme_extraction import audio_to_text
import difflib
client = TextRazor("7270e70f5603da8cc1d66e27c99524e658f220078ed51eafb6f3748b", extractors=["entities", "topics"])

# audio_texts = [audio_to_text('crucifixion1.wav'), audio_to_text('crucifixion2.wav'), audio_to_text('crucifixion3.wav'), audio_to_text('crucifixion4.wav')]

audio_texts = [
    "The crucifixion was created in the 14th century  circa 1350-1359 experts are not sure exactly when but it is estimated that it was around 1352",
    "honestly this did not stand out much compared to the many depictions of the crucifixion the only original part was the swan in the birds overlooking it as Christ is supposed to",
    "what strikes me about the crucifixion is that some idiot tried to buy this for 100 Bitcoin that's almost $800,000 absolutely insane I don't understand it",
    "what's really interesting to me about this crucifixion painting is that there is this little bird with a nest on the top and I keep trying to figure out what that's trying to symbolize is the bird God and he is guarding over his children by sending his one and only son Jesus Christ to die for our sins or is the bird Mary Magdalene who's also you know that her son go off and die for this purpose so that's that's a really interesting question for me",
    "the crucifixion is based on a wood panel with gold leaf and be inscribed images that you see the gold brings out the Holiness and spirituality associated with this imagery and prepares it for its placement in a high-end esteem Church",
]
topic_tags = []
for audio_text in audio_texts:
    response = client.analyze(audio_text)
    audio_tags =[]
    for topic in response.topics()[:10]:
        if topic.score > 0.3:
            audio_tags.append(topic.label)
    topic_tags.append(audio_tags)

user_question = "when was the crucifixion created?"
response = client.analyze(user_question)
question_tags =[]
for topic in response.topics():
    print()
    question_tags.append(topic.label)

similarities =[]
print(question_tags)
for audio_tags in topic_tags:
    print(audio_tags)
    similarities.append(difflib.SequenceMatcher(None,audio_tags,question_tags).ratio())

print(similarities)