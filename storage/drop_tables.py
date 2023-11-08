import sqlite3

conn = sqlite3.connect('readings.sqlite')

c = conn.cursor()
c.execute('''
          DROP TABLE report_patrol
          ''')
c.execute('''
          DROP TABLE report_infrared
          ''')

conn.commit()
conn.close()