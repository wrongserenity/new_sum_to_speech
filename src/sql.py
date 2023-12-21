import psycopg2


class DB:
    def __init__(self):
        self.host = 'postgres'
        self.user = 'root'
        self.password = 'postgres'
        self.database = 'public'
        self.table_name = 'parsed_url'
        self.cur = self.conn()

    def conn(self):
        try:
            conn = psycopg2.connect(host=self.host, user=self.user, password=self.password)
            print('Connect to db')
        except Exception as e:
            print("DB: ", e)
            exit(0)

        conn.autocommit = True
        cur = conn.cursor()

        return cur

    def select_all_from_table(self, id):
        sql = "SELECT * " + self.table_name + ' where id = ' + id
        self.cur.execute(sql)
        data = self.cur.fetchall()
        return data

    def new_row(self, params):
        sql = ("INSERT INTO " + self.table_name + " (url, text, path_to_audio, article_date, path_to_img) VALUES ('"
               + params['url'] + "', '"
               + params['text'] + "', '"
               + params['path_to_audio'] + "', '"
               + params['article_date'] + "', '"
               + params['path_to_img'] + "')")
        print(sql)
        id = self.cur.execute(sql)
        return id

    def select_rows_by_date(self, date_start, date_end):
        sql = "SELECT text, path_to_audio, path_to_img FROM " + self.table_name + " where article_date >= '" + date_start + "' and article_date <= '" + date_end + "'"
        print(sql)
        self.cur.execute(sql)
        data = self.cur.fetchall()
        result = []
        for item in data:
            result.append({'text': item[0], 'path_to_audio': item[1], 'path_to_img': item[2]})
        print(result)
        return result

    def check_rows_by_url(self, url):
        sql = "SELECT url_id FROM " + self.table_name + " WHERE url='" + url + "'"
        self.cur.execute(sql)
        data = self.cur.fetchall()
        if data:
            return True
        else:
            return False

    def select_all_urls(self):
        sql = "SELECT url FROM " + self.table_name
        self.cur.execute(sql)
        data = self.cur.fetchall()
        data = [item[0] for item in data]
        print(data)
        return data

    def select_max_id(self):
        sql = "SELECT url_id FROM " + self.table_name + " order by url_id desc limit 1"
        self.cur.execute(sql)
        data = self.cur.fetchall()
        print(data)
        if data:
            return data[0][0]
        else:
            return 0
