import sqlite3

conn = sqlite3.connect('readings.sqlite')

c = conn.cursor()
c.execute('''
    CREATE TABLE report_patrol
        (officer_id INTEGER NOT NULL,
        reporter VARCHAR(100) NOT NULL,
        status_code INTEGER NOT NULL,
        timestamp VARCHAR(100) NOT NULL,
        writeup VARCHAR(250) NOT NULL,
        date_created VARCHAR(100) PRIMARY KEY NOT NULL,
        trace_id VARCHAR(100) NOT NULL)
          ''')

c.execute('''
    CREATE TABLE report_infrared
        (sensor_id VARCHAR(100) NOT NULL,
        status_code INTEGER NOT NULL,
        temperature INTEGER NOT NULL,
        timestamp VARCHAR(100) NOT NULL,
        date_created VARCHAR(100) PRIMARY KEY NOT NULL,
        trace_id VARCHAR(100) NOT NULL)
''')

conn.commit()
conn.close()
