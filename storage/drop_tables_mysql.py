import mysql.connector

db_conn = mysql.connector.connect(host='ec2-35-167-228-45.us-west-2.compute.amazonaws.com', user='root', password='1234', database='events')

db_cursor = db_conn.cursor()
db_cursor.execute('''
          DROP TABLE report_patrol, report_infrared
          ''')

db_conn.commit()
db_conn.close()