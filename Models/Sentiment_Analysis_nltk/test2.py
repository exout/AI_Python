from Settings.settings import *

stopwords = stopwords.words('swedish')
input_text = "Är Python bättre än Java?" \
             "Jag tror att vi kommer at uppleva många olika saker i framtiden, tex resa till space och " \
             "träffa UFOs"
words = input_text.split()
words_without_stopwords = [word for word in words if word not in stopwords]
text_without_stopwords = " ". join(words_without_stopwords)
print(text_without_stopwords)

stemmer = SnowballStemmer('swedish')
print(stemmer.stem(input_text))


lemmatizer = WordNetLemmatizer()
print(lemmatizer.lemmatize(words))