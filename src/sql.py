import psycopg2


class DB:
    def __init__(self):
        self.host = 'localhost'
        self.user = 'postgres'
        self.password = 'postgres'
        self.database = 'parsing'
        self.table_name = 'parsed_url'

    def conn(self):
        try:
            conn = psycopg2.connect(host=self.host, database=self.database,
                                    user=self.user, password=self.password)
            print('Connect to db')
        except Exception as e:
            print(e)
            exit(0)

        conn.autocommit = True
        cur = conn.cursor()

        return cur

    def select_all_from_table(self, id):
        sql = "SELECT * " + self.table_name + ' where id = ' + id
        cur = self.conn()
        cur.execute(sql)
        data = cur.fetchall()
        return data

    def new_row(self, params):
        sql = ("INSERT INTO " + self.table_name + " (url, text, path_to_audio, article_date) VALUES ('"
               + params['url'] + "', '"
               + params['text'] + "', '"
               + params['path_to_audio'] + "', '"
               + params['article_date'] +
               "')")
        print(sql)
        cur = self.conn()
        id = cur.execute(sql)
        return id

    def select_rows_by_date(self, date_start, date_end):
        sql = "SELECT path_to_audio FROM " + self.table_name + " where article_date >= '" + date_start + "' and article_date <= '" + date_end + "'"
        cur = self.conn()
        cur.execute(sql)
        data = cur.fetchall()
        data = [item[0] for item in data]
        return data

    def check_rows_by_url(self, url):
        sql = "SELECT url_id FROM " + self.table_name + " WHERE url='" + url + "'"
        cur = self.conn()
        cur.execute(sql)
        data = cur.fetchall()
        if data:
            return True
        else:
            return False

    def select_all_urls(self):
        sql = "SELECT url FROM " + self.table_name
        cur = self.conn()
        cur.execute(sql)
        data = cur.fetchall()
        data = [item[0] for item in data]
        print(data)
        return data

    def select_max_id(self):
        sql = "SELECT url_id FROM " + self.table_name + " order by url_id desc limit 1"
        cur = self.conn()
        cur.execute(sql)
        data = cur.fetchall()
        print(data)
        return data[0][0]