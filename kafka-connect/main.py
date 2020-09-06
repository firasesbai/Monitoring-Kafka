from logger import *
import os
import requests
import time

def get_list_connectors(kafka_connect_url):
    url = str(kafka_connect_url) + '/connectors'
    response = requests.get(url)
    return response.json()

def get_connector_status(kafka_connect_url, connector):
    url = str(kafka_connect_url) + '/connectors/' + connector + '/status'
    response = requests.get(url)
    return response.json()

def restart_connector(kafka_connect_url, connector):
     url = str(kafka_connect_url) + '/connectors/' + connector + '/restart'
     response = requests.post(url)
     return response

def restart_task(kafka_connect_url, connector, task_id):
     url = str(kafka_connect_url) + '/connectors/' + connector + '/tasks/' + str(task_id) + '/restart'
     response = requests.post(url)
     return response

def main():
    logger_name = os.getenv('LOGGER_NAME')

    logger_path = 'logs/' + logger_name + '.log'
    setup_logger(logger_name, logger_path)
    logger_name = logging.getLogger(logger_name)

    logger_name.info('Loading Configuration...')
    kafka_connect_url = os.getenv('KAFKA_CONNECT_URL')
    logger_name.info('KEY_CONNECT_URL= ' + str(kafka_connect_url))
    check_window = os.getenv('CHECK_WINDOW')
    logger_name.info('CHECK_WINDOW= ' + str(check_window))
    logger_name.info('Starting monitoring connectors...')
    while True:
        list_connectors = get_list_connectors(kafka_connect_url)
        logger_name.debug(list_connectors)
        for connector in list_connectors:
            status = get_connector_status(kafka_connect_url, connector)
            if status['connector']['state'] == 'RUNNING':
                 for task in status['tasks']:
                     if task['state'] == 'RUNNING':
                         pass
                     else:
                         logger_name.info('Connector: ' + str(status['name']) + ' has task: ' + str(task['id']) + 'with state: ' + str(task['state']) + ' , reason: ' + str(task['trace']))
                         restart_response = restart_task(kafka_connect_url, status['name'], task['id'])
                         logger_name.info('Result of restarting task: ' + str(task['id']) + str(restart_response))
            else:
                logger_name.info('Connector: ' + str(status['name']) + ' has state: ' + str(status['connector']['state']))
                restart_response = restart_connector(kafka_connect_url, status['name'])
                logger_name.info('Result of restarting connector: ' + str(status['name']) + str(restart_response))
        time.sleep(int(check_window))

if __name__ == '__main__':
    main()

