import requests
import logging
from app.config import Config

logger = logging.getLogger(__name__)

def send_to_aws_record(temperature, humidity, gas_level):
    data = {
        'temperature': temperature, 
        'humidity': humidity,
        'gas_level': gas_level 
    }
    try:
        response = requests.post(Config.AWS_RECORD_URL, json=data, headers={'Content-Type': 'application/json'}, verify=False)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        logger.error(f"Error sending record to AWS: {e}")
        return None

def send_to_aws_table(seat1, seat2, seat3, seat4):
    data = {
        'seat1': seat1, 
        'seat2': seat2,
        'seat3': seat3,
        'seat4': seat4
    }
    try:
        response = requests.post(Config.AWS_TABLE_URL, json=data, headers={'Content-Type': 'application/json'}, verify=False)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        logger.error(f"Error sending table to AWS: {e}")
        return None
