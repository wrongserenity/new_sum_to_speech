from num2words import num2words
import spacy
import pymorphy2

NUMBER_CASE_BY_PREP = {
    "в": "loct",
    "на": "accs",
    "к": "datv",
    "по": "accs",
    "с": "gent",
    "про": "accs",
}

DOMAIN_ABBR_DICT = {
    "г.": "год",
    "квт": "киловатт",
    "л.": "литр",
    "об.": "обороты",
    "тыс": "тысяча",
    "млн": "миллион",
    "млрд": "миллиард",
    "трлн": "триллион",
    "квтч": "киловатт в час",
    "см": "сантиметр",
    "кг": "килограмм",
    "т.": "тонна",
    "ч.": "час",
    "мин.": "минута",
    "сек.": "секунда",
    "мм": "миллиметр"
}

NEIGHBOURS_IDXS = [-1, 1]


class NewsDataPreprocessor:
    def __init__(self):
        self.morph = pymorphy2.MorphAnalyzer()
        self.nlp = spacy.load("ru_core_news_sm")

    def process_text(self, input_text_):
        try:
            doc = self.nlp(input_text_)
            result_words = []

            is_need_extend_abbr = False

            for i in range(len(doc)):
                if doc[i].is_digit:
                    print(doc[i].text)
                    case = self.get_case_in_neighbour_words(doc, i)
                    result_words.append(self.convert_num_to_word_with_case(doc[i].text, case))
                    continue
                result_words.append(doc[i].text)
                if doc[i].text in DOMAIN_ABBR_DICT.keys():
                    is_need_extend_abbr = True
            result_text = " ".join(result_words)

            if is_need_extend_abbr:
                doc = self.nlp(result_text)
                result_words = []
                for i in range(len(doc)):
                    if doc[i].text in DOMAIN_ABBR_DICT:
                        case = self.get_case_in_neighbour_words(doc, i)
                        result_words.append(self.convert_word_to_case(DOMAIN_ABBR_DICT[doc[i].text], case))
                        continue
                    result_words.append(doc[i].text)
                result_text = " ".join(result_words)
            return self.process_punctuation(result_text)
        except Exception as e:
            print("Preprocessor: ", e)
            exit(0)

    def get_case_in_neighbour_words(self, doc_, index_):
        if doc_[index_].is_digit:
            for ix in NEIGHBOURS_IDXS[::-1]:
                is_noun = ix > 0
                is_prep = ix < 0
                candidate_ = self.try_get_case_by_index(doc_, index_ + ix, is_noun_check=is_noun, is_prep_check=is_prep)
                if candidate_ is not None:
                    return candidate_
        else:
            for ix in NEIGHBOURS_IDXS:
                candidate_ = self.try_get_case_by_index(doc_, index_ + ix)
                if candidate_ is not None:
                    return candidate_
        return "nomn"

    def try_get_case_by_index(self, doc_, index_, is_noun_check=False, is_prep_check=False):
        if index_ >= len(doc_) or index_ < 0:
            return None

        if not doc_[index_].is_alpha:
            return None

        word_text = doc_[index_].text
        word_info = self.morph.parse(word_text)[0]

        if is_noun_check and not word_info.tag.POS == "NOUN":
            return None

        if is_prep_check and not word_info.tag.POS == "PREP":
            return None

        if word_info.tag.POS == "PREP" and word_info.normal_form in NUMBER_CASE_BY_PREP.keys():
            return NUMBER_CASE_BY_PREP[word_info.normal_form]

        return word_info.tag.case

    def convert_num_to_word_with_case(self, num, case):
        num_text = num2words(num, lang='ru', ordinal=True)

        num_words = num_text.split(" ")
        num_words[-1] = self.convert_word_to_case(num_words[-1], case)
        result = " ".join(num_words)
        return result

    def convert_word_to_case(self, word, case):
        morph_word = self.morph.parse(word)[0]
        return morph_word.inflect({case}).word

    @staticmethod
    def process_punctuation(sentence):
        for p in [".", ",", "!", "?", ";", ":"]:
            sentence = sentence.replace((" " + p), p)
        return sentence

