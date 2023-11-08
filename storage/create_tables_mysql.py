import mysql.connector

db_conn = mysql.connector.connect(host="ec2-35-167-228-45.us-west-2.compute.amazonaws.com", user="root", password="1234", database="events")

db_cursor = db_conn.cursor()
db_cursor.execute('''
    CREATE TABLE report_patrol
        (date_created VARCHAR(100) NOT NULL,
        officer_id INTEGER NOT NULL,
        reporter VARCHAR(100) NOT NULL,
        status_code INTEGER NOT NULL,
        timestamp VARCHAR(100) NOT NULL,
        writeup VARCHAR(250) NOT NULL,
        trace_id VARCHAR(100) NOT NULL,
        CONSTRAINT report_patrol_pk PRIMARY KEY (date_created))''')

db_cursor.execute('''
    CREATE TABLE report_infrared
        (date_created VARCHAR(100) NOT NULL,
        sensor_id VARCHAR(100) NOT NULL,
        status_code INT NOT NULL,
        temperature INT NOT NULL,
        timestamp VARCHAR(100) NOT NULL,
        trace_id VARCHAR(100) NOT NULL,
        CONSTRAINT report_infrared_pk PRIMARY KEY (date_created))
''')

db_conn.commit()
db_conn.close()