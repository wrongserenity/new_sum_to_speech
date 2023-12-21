from bs4 import BeautifulSoup
import requests
import re

from parser.news_data_preprocessor import NewsDataPreprocessor
from sql import DB
from parser.news_summarizer import NewsSummarizer
from parser.news_tts import NewsTts
import nltk
from parser.news_tag_cloud import TagCloudCreator
from datetime import datetime

nltk.download('punkt')


class Parser:
    def __init__(self, main_url):
        self.main_url = main_url
        self.news_tts = NewsTts()
        self.news_summarizer = NewsSummarizer()
        self.db = DB()
        self.news_preprocessor = NewsDataPreprocessor()
        self.tag_cloud = TagCloudCreator()

    def cleanhtml(self, raw_html):
        CLEANR = re.compile('<.*?>')
        cleantext = re.sub(CLEANR, '', raw_html)
        return cleantext

    def get_links(self, url):
        response = requests.get(url)
        data = response.text
        soup = BeautifulSoup(data, 'lxml')
        links = []
        # all_urls = self.db.select_all_urls()
        for link in soup.find_all('a'):
            link_url = link.get('href')
            if link_url is not None and link_url.startswith('/') and not link_url.endswith(
                    '/') and not self.db.check_rows_by_url(self.main_url + link_url):
                links.append(self.main_url + link_url + '\n')
                full_link = self.main_url + link_url
                self.get_text_from_url(full_link)

        # self.write_to_file(links)
        return links

    def write_to_file(self, links):
        with open('../data.txt', 'a') as f:
            f.writelines(links)

    def get_all_links(self, url):
        print(url)
        for link in self.get_links(url):
            self.get_all_links(link)

    def get_text_from_url(self, url):
        response = requests.get(url)
        data = response.text
        soup = BeautifulSoup(data, 'lxml')
        texts = []
        params = {}
        for text in soup.find_all('p'):
            if len(self.cleanhtml(text.text)) > 50:
                texts.append(self.cleanhtml(text.text))
        try:
            date_text = soup.find_all('div', {"class": "date"})[0].text
            # self.write_to_file(url)
            # self.write_to_file('\n')
            # self.write_to_file(date_text)
            # self.write_to_file('\n')
            # self.write_to_file('\n'.join(texts))
            # self.write_to_file('\n' * 3)
            extr_text = self.news_summarizer.get_text_extract_sum('\n'.join(texts), n=3)
            abst_text = self.news_summarizer.get_text_abstract_sum(extr_text)
            print(extr_text)
            extr_text = self.news_preprocessor.process_text(extr_text)



            audio_sum = self.news_tts.get_audio(extr_text)
            id = str(int(self.db.select_max_id()) + 1)
            path_img = self.tag_cloud.save_cloud_img(self.tag_cloud.get_freq(extr_text), id + '.jpg')
            print(date_text)
            # news_tts.play_audio(audio_sum)
            path_to_audio = self.news_tts.save_wav_of_tts(audio_sum, id + '.ogg')
            date_text = datetime.strptime(date_text, '%d.%m.%Y').strftime("%m.%d.%Y")
            params = {'url': url, 'text': abst_text, 'path_to_audio': path_to_audio, 'article_date': date_text,
                      'path_to_img': path_img}
            self.db.new_row(params)
        except Exception as e:
            print("Parser: ", e)
            exit(0)

# r = 'http://moymotor.ru'
# all_urls = []
# parser = Parser(r)
# parser.get_all_links(r)
# parser.write_to_file([r])
