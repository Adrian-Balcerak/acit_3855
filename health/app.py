import connexion
import datetime
import requests
import json
from flask import Response
from flask_cors import CORS, cross_origin
import yaml
import logging, logging.config
import uuid
from apscheduler.schedulers.background import BackgroundScheduler

app = connexion.FlaskApp(__name__, specification_dir='')
CORS(app.app)
app.app.config['CORS_HEADERS'] = 'Content-Type'

import os

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

print(log_config['handlers']['file']['filename'])

logger = logging.getLogger('basicLogger')

logger.info("App Conf File: %s" % app_config_file)
logger.info("Log Conf File: %s" % log_config_file)

def get_health():
    logger.info("Request for stats has begun.")

    try:
        with open(app_config['datastore']['filename'], 'r') as file:
            health = json.load(file)
    except:
        fp = open(app_config['datastore']['filename'], 'w')
        health = {
    "receiver": "unknown",
    "storage": "unknown",
    "processing": "unknown",
    "audit": "unknown",
    "last_update": "2022-03-22T11:12:23"
}
        fp.write(health)
        fp.close()

    logger.info("Request has completed.")

    return Response(json.dumps(health), 200)
    

def check_health():
    logger.info("Perform Health Checks")
    
    results = {}
    try:
        receiver = requests.get(app_config['targets']['receiver'])
        results["receiver"] = receiver.json()['status']
    except:
        results["receiver"] = "Down"
    try:
        storage = requests.get(app_config['targets']['storage'])
        results["storage"] = storage.json()['status']
    except:
        results["storage"] = "Down"
    try:
        processor = requests.get(app_config['targets']['processor'])
        results["processor"] = processor.json()['status']
    except:
        results["processor"] = "Down"
    try:
        audit = requests.get(app_config['targets']['audit'])
        results["audit"] = audit.json()['status']
    except:
        results["audit"] = "Down"
    
    results["last_u"] = datetime.datetime.now()

    logger.debug(results)

    results = json.dumps(results, indent=4, default=str)

    with open(app_config['datastore']['filename'], "w") as outfile:
        outfile.write(results)

    logger.info("health check stored")

def init_scheduler():
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(check_health,
                'interval',
                seconds=app_config['scheduler']['period_sec'])
    sched.start()

app.add_api("openapi.yml", strict_validation=True, validate_responses=True)

if __name__ == '__main__':
    init_scheduler()
    app.run(port='8120')