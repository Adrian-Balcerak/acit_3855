import connexion
import logging, logging.config
import yaml
from pykafka import KafkaClient
import json
from flask import Response
from flask_cors import CORS, cross_origin
import os

app = connexion.FlaskApp(__name__, specification_dir='')
CORS(app.app)
app.app.config['CORS_HEADERS'] = 'Content-Type'


if "TARGET_ENV" in os.environ and os.environ["TARGET_ENV"] == "test":
    app_config_file = "/config/app_conf.yml"
    log_config_file = "/config/log_conf.yml"
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

def get_patrol_report(index):
    print('1')
    hostname = "%s:%d" % (app_conf["events"]["hostname"],
    app_conf["events"]["port"])
    client = KafkaClient(hosts=hostname)
    print('2')
    topic = client.topics[str.encode(app_conf["events"]["topic"])]

    # Here we reset the offset on start so that we retrieve
    # messages at the beginning of the message queue.
    # To prevent the for loop from blocking, we set the timeout to
    # 100ms. There is a risk that this loop never stops if the
    # index is large and messages are constantly being received!

    consumer = topic.get_simple_consumer(reset_offset_on_start=True,
    consumer_timeout_ms=1000)
    logger.info("Retrieving ReportPatrol at index %d" % index)
    try:
        count = 0
        for msg in consumer:
            msg_str = msg.value.decode('utf-8')
            msg = json.loads(msg_str)
            if msg['type'] == 'PatrolReport':
                if count == index:
                    return Response(json.dumps(msg['payload'], indent=1), 200)
                else:
                    count += 1

    except:
        logger.error("No more messages found")
    logger.error("Could not find Report Patrol at index %d" % index)
    return { "message": "Not Found"}, 404

def get_infrared_report(index):
    hostname = "%s:%d" % (app_conf["events"]["hostname"],
    app_conf["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_conf["events"]["topic"])]

    # Here we reset the offset on start so that we retrieve
    # messages at the beginning of the message queue.
    # To prevent the for loop from blocking, we set the timeout to
    # 100ms. There is a risk that this loop never stops if the
    # index is large and messages are constantly being received!

    consumer = topic.get_simple_consumer(reset_offset_on_start=True,
    consumer_timeout_ms=1000)
    logger.info("Retrieving InfraredtPatrol at index %d" % index)
    try:
        count = 0
        for msg in consumer:
            msg_str = msg.value.decode('utf-8')
            msg = json.loads(msg_str)
            if msg['type'] == 'InfraredReport':
                if count == index:
                    return Response(json.dumps(msg['payload'], indent=1), 200)
                else:
                    count += 1

    except:
        logger.error("No more messages found")
    logger.error("Could not find Report Patrol at index %d" % index)
    return { "message": "Not Found"}, 404

app.add_api("openapi.yml", strict_validation=True, validate_responses=True)

if __name__ == '__main__':
    app.run(port=8110)