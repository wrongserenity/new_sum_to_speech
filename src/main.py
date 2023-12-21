from parser.news_parsing import Parser

if __name__ == "__main__":
    r = 'http://moymotor.ru'
    all_urls = []
    parser = Parser(r)
    parser.get_all_links(r)

