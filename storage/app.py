import connexion
from connexion import NoContent
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
from flask import Response
import mysql.connector
import pymysql
import yaml
import json
import datetime
import logging, logging.config
from pykafka import KafkaClient
from pykafka.common import OffsetType
from threading import Thread
from declaratives import Base, ReportInfrared, ReportPatrol

app = connexion.FlaskApp(__name__, specification_dir='')

with open('db_conf.yml', 'r') as f:
    db_config = yaml.safe_load(f.read())

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

DB_ENGINE = create_engine(
    f'mysql+pymysql://{db_config["datastore"]["user"]}:{db_config["datastore"]["password"]}@{db_config["datastore"]["hostname"]}:{db_config["datastore"]["port"]}/{db_config["datastore"]["db"]}'
    )
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)

def report_patrol(body):
    logger.info(f'Connecting to DB. Hostname: {db_config["datastore"]["hostname"]}, Port: {db_config["datastore"]["port"]}')
    session = DB_SESSION()

    rp = ReportPatrol(body['officer_id'], 
                           body['reporter'],
                           body['status_code'],
                           body['timestamp'],
                           body['writeup'],
                           body['trace_id'])
    
    session.add(rp)
    session.commit()
    session.close()

    event_name = 'PatrolReport'
    logger.debug(f'Stored Event {event_name} request with a trace if of {body["trace_id"]}')

    return Response("🙏🔥🔥", 201)


def report_infrared(body):
    
    session = DB_SESSION()

    ri = ReportInfrared(body['sensor_id'], 
                           body['status_code'],
                           body['temperature'],
                           body['timestamp'],
                           body['trace_id'])
    
    session.add(ri)
    session.commit()
    session.close()

    event_name = 'InfraredReport'
    logger.debug(f'Stored Event {event_name} request with a trace if of {body["trace_id"]}')

    return Response("🙏🔥🔥", 201)

def get_report_patrol(timestamp, timestamp_end):
    session = DB_SESSION()

    readings = session.query(ReportPatrol).filter(and_(ReportPatrol.date_created >= timestamp, ReportPatrol.date_created < timestamp_end))

    results_list = []

    for reading in readings:
        results_list.append(reading.to_dict())

    session.close()

    logger.info("Query for Patrol Reports after %s returns %d results" % (timestamp, len(results_list)))

    return Response(json.dumps(results_list), 200)

def get_report_infrared(timestamp, timestamp_end):
    session = DB_SESSION()

    readings = session.query(ReportInfrared).filter(and_(ReportInfrared.date_created >= timestamp, ReportInfrared.date_created < timestamp_end))

    results_list = []

    for reading in readings:
        results_list.append(reading.to_dict())

    session.close()

    logger.info("Query for Patrol Reports after %s returns %d results" % (timestamp, len(results_list)))

    return Response(json.dumps(results_list), 200)

def process_messages():
    """ Process event messages """
    hostname = "%s:%d" % (db_config["events"]["hostname"],
        db_config["events"]["port"])
    print('hostname')
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(db_config["events"]["topic"])]

    # Create a consume on a consumer group, that only reads new messages
    # (uncommitted messages) when the service re-starts (i.e., it doesn't
    # read all the old messages from the history in the message queue).

    consumer = topic.get_simple_consumer(consumer_group=b'event_group',
        reset_offset_on_start=False,
        auto_offset_reset=OffsetType.LATEST)

    # This is blocking - it will wait for a new message

    for msg in consumer:
        msg_str = msg.value.decode('utf-8')
        msg = json.loads(msg_str)
        logger.info("Message: %s" % msg)
        payload = msg["payload"]
        session = DB_SESSION()
        if msg["type"] == "PatrolReport": # Change this to your event type
            # Store the event1 (i.e., the payload) to the DB
            ev = ReportPatrol(payload['officer_id'], 
                                payload['reporter'],
                                payload['status_code'],
                                payload['timestamp'],
                                payload['writeup'],
                                payload['trace_id'])

        elif msg["type"] == "InfraredReport": # Change this to your event type
            # Store the event2 (i.e., the payload) to the DB
            ev = ReportInfrared(payload['sensor_id'], 
                           payload['status_code'],
                           payload['temperature'],
                           payload['timestamp'],
                           payload['trace_id'])

        session.add(ev)
        session.commit()
        session.close()
        # Commit the new message as being read
        consumer.commit_offsets()

app.add_api("openapi.yml")

if __name__ == '__main__':
    t1 = Thread(target=process_messages)
    t1.setDaemon(True)
    t1.start()

    app.run(port='8090')
