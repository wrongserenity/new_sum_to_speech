from sklearn.feature_extraction.text import TfidfVectorizer

import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from collections import Counter

from stop_words import get_stop_words

import nltk

class TagCloudCreator:
    def __init__(self):
        nltk.download('stopwords')
        nltk.download('punkt')
        nltk.download('wordnet')
        stop_words_nltk = set(stopwords.words('russian'))
        stop_words_additional = get_stop_words('russian')

        self.stop_words = stop_words_nltk.union(stop_words_additional)

    def get_freq(self, text):
        words = word_tokenize(text)

        lemmatizer = WordNetLemmatizer()
        lemmatized_words = [lemmatizer.lemmatize(word.lower()) for word in words if
                            word.isalpha() and word.lower() not in self.stop_words]

        stemmer = SnowballStemmer('russian')
        stemmed_words = [stemmer.stem(word) for word in lemmatized_words if word.lower() not in self.stop_words]

        preprocessed_text = ' '.join(stemmed_words)

        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([preprocessed_text])

        terms = vectorizer.get_feature_names_out()
        tfidf_values = tfidf_matrix.toarray()[0]
        term_tfidf_dict = dict(zip(terms, tfidf_values))

        word_forms_dict = dict(zip(stemmed_words, lemmatized_words))
        result_dict = {}
        for key, val in term_tfidf_dict.items():
            temp_key = key
            if temp_key in word_forms_dict:
                temp_key = word_forms_dict[temp_key]
            result_dict[temp_key] = val
        return result_dict

    def save_cloud_img(self, freq_dict, file_name, folder="result/tag_clouds/"):
        wordcloud = WordCloud(width=800, height=400, background_color='white', max_words=20).generate_from_frequencies(
            freq_dict)

        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title('Облако тегов: Новости о машинах (с использованием TF-IDF)')
        plt.savefig(folder + file_name)
        plt.clf()
        return folder + file_name