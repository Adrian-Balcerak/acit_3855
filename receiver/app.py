import connexion
import datetime
import requests
import json
from flask import Response
import yaml
import logging, logging.config
import uuid
from pykafka import KafkaClient
import time
import os

if "TARGET_ENV" in os.environ and os.environ["TARGET_ENV"] == "test":
    app_config_file = "config/app_conf.yml"
    log_config_file = "config/log_conf.yml"
else:
    app_config_file = "app_conf.yml"
    log_config_file = "log_conf.yml"

with open(app_config_file, 'r') as f:
    app_config = yaml.safe_load(f.read())

with open(log_config_file, 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

logger.info("App Conf File: %s" % app_config_file)
logger.info("Log Conf File: %s" % log_config_file)

tries_max = app_config['events']['retry']
sleep_time = app_config['events']['sleep']
attempt = 0
while attempt < tries_max:
    logger.info("Trying to establish a connection to the Kafka Client")
    try:
        client = KafkaClient(hosts=f'{app_config["events"]["hostname"]}:{app_config["events"]["port"]}')
        break
    except:
        logger.debug("Failed to establish a connection to the Kafka Client")
        time.sleep(sleep_time)
        attempt+= 1

def report_patrol(body):
    event_name = 'PatrolReport'
    trace_id = str(uuid.uuid4())
    body['trace_id'] = trace_id
    logger.info(f'Received event {event_name} PatrolReport request with a trace id of {trace_id}')
    url = app_config["eventstore1"]["url"]
    h = {"Content-Type": "application/json"}

    #r = requests.post(url, json.dumps(body), headers = h)
    
    try:
        topic = client.topics[str.encode(app_config["events"]["topic"])]
        producer = topic.get_sync_producer()
    except:
        client = KafkaClient(hosts=f'{app_config["events"]["hostname"]}:{app_config["events"]["port"]}')
        topic = client.topics[str.encode(app_config["events"]["topic"])]
        producer = topic.get_sync_producer()
    msg = { "type": event_name, "datetime" :
        datetime.datetime.now().strftime(
            "%Y-%m-%dT%H:%M:%S"),
            "payload": body }
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))
    
    logger.info(f'Returned Event {event_name} response (Id: {trace_id}) with status {str(201)}')
    return Response("🙏🔥🔥", 201)

def report_infrared(body):
    event_name = 'InfraredReport'
    trace_id = str(uuid.uuid4())
    body['trace_id'] = trace_id
    logger.info(f'Received event {event_name} PatrolReport request with a trace id of {trace_id}')
    url = app_config["eventstore2"]["url"]
    h = {"Content-Type": "application/json"}

    #r = requests.post(url, json.dumps(body), headers = h)

    try:
        topic = client.topics[str.encode(app_config["events"]["topic"])]
        producer = topic.get_sync_producer()
    except:
        client = KafkaClient(hosts=f'{app_config["events"]["hostname"]}:{app_config["events"]["port"]}')
        topic = client.topics[str.encode(app_config["events"]["topic"])]
        producer = topic.get_sync_producer()
    msg = { "type": event_name, "datetime" :
        datetime.datetime.now().strftime(
            "%Y-%m-%dT%H:%M:%S"),
            "payload": body }
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))

    logger.info(f'Returned Event {event_name} response (Id: {trace_id}) with status {str(201)}')
    return Response("🙏🔥🔥", 201)

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)

if __name__ == '__main__':
    app.run(port='8080')