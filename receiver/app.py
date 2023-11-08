import connexion
import jsonify
import datetime
import requests
import json
from flask import Response
import yaml
import logging, logging.config
import uuid
from pykafka import KafkaClient

with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

def report_patrol(body):
    event_name = 'PatrolReport'
    trace_id = str(uuid.uuid4())
    body['trace_id'] = trace_id
    logger.info(f'Received event {event_name} PatrolReport request with a trace id of {trace_id}')
    url = app_config["eventstore1"]["url"]
    h = {"Content-Type": "application/json"}

    #r = requests.post(url, json.dumps(body), headers = h)

    client = KafkaClient(hosts=f'{app_config['events']['hostname']}:{app_config['events']['port']}')
    topic = client.topics[str.encode(app_config['events']['topic'])]
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

    client = KafkaClient(hosts=f'{app_config['events']['hostname']}:{app_config['events']['port']}')
    topic = client.topics[str.encode(app_config['events']['topic'])]
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