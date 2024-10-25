from mysql.connector import pooling

#这个文件是mysql的连接池

class DB:
    def __init__(self, config):
        self.pool = pooling.MySQLConnectionPool(pool_name="mypool", pool_size=5, **config)


    def get_connection(self):
        return self.pool.get_connection()

    def close_connection(self, connection):
        connection.close()

    def execute_query(self, query, params=None):
        connection = self.get_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute(query, params)
            result = cursor.fetchall()
            return result
        finally:
            cursor.close()
            self.close_connection(connection)

    def execute_many(self, query, data):        
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.executemany(query, data)
            connection.commit()
        finally:
            self.close_connection(connection)

    def execute_insert(self, query, data):  
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(query, data)
            connection.commit()
            return cursor.lastrowid
        finally:
            self.close_connection(connection)   


config = {
    'user': 'root',
    'password': 'Zlr7788521001!',
    'host': 'localhost',
    'database': 'atman_mirror',
}

db = DB(config)



# db.db.execute_insert("INSERT INTO bot_response_log (mentioned_conversation_tweet_id, mentioned_conversation_tweet_text, mentioned_tweet_id, mentioned_tweet_text, tweet_response_id, tweet_response_text, tweet_response_created_at) VALUES (%s, %s, %s, %s, %s, %s, %s)", (str(mentioned_conversation_tweet.id), mentioned_conversation_tweet.text, str(mention.id), mention.text, response_tweet.data['id'], response_text, now.strftime('%Y-%m-%d %H:%M:%S')))
# main函数 写一个sql查询


if __name__ == "__main__":
    result = db.execute_query("SELECT * FROM bot_response_log")
    print(result)


# CREATE TABLE bot_response_log (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     mentioned_conversation_tweet_id VARCHAR(255),
#     mentioned_conversation_tweet_text TEXT,
#     mentioned_tweet_id VARCHAR(255),
#     mentioned_tweet_text TEXT,
#     tweet_response_id VARCHAR(255),
#     tweet_response_text TEXT,
#     tweet_response_created_at DATETIME
# );


