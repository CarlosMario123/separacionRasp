import queue
import threading
import time
import socket
import logging
from app.aws_client import send_to_aws_record, send_to_aws_table
from app.services import mark_synced

logger = logging.getLogger(__name__)

data_queue = queue.Queue()
table_queue = queue.Queue()

def is_internet_available(host="www.google.com", port=80, timeout=3):
    try:
        socket.create_connection((host, port), timeout)
        return True
    except OSError:
        return False

def process_data_queue():
    while True:
        try:
            data = data_queue.get(timeout=1)
            if is_internet_available():
                logger.info(f"Sending data to AWS: {data}")
                response = send_to_aws_record(data['temperature'], data['humidity'], data['gas_level'])
                if response and response.status_code == 201:
                    mark_synced('data', data['id'])
                    logger.info(f"Data sent successfully for id={data['id']}")
                else:
                    data_queue.put(data)
                    logger.warning(f"Failed to send data for id={data['id']}, retrying...")
                    time.sleep(5)
            else:
                data_queue.put(data)
                logger.warning("No internet connection. Waiting to resend data...")
                time.sleep(5)
        except queue.Empty:
            continue
        except Exception as e:
            logger.error(f"Error processing data queue: {e}")

def process_table_queue():
    while True:
        try:
            data = table_queue.get(timeout=1)
            if is_internet_available():
                logger.info(f"Sending table data to AWS: {data}")
                response = send_to_aws_table(data['seat1'], data['seat2'], data['seat3'], data['seat4'])
                if response and response.status_code == 201:
                    mark_synced('tables', data['id'])
                    logger.info(f"Table data sent successfully for id={data['id']}")
                else:
                    table_queue.put(data)
                    logger.warning(f"Failed to send table data for id={data['id']}, retrying...")
                    time.sleep(5)
            else:
                table_queue.put(data)
                logger.warning("No internet connection. Waiting to resend table data...")
                time.sleep(5)
        except queue.Empty:
            continue
        except Exception as e:
            logger.error(f"Error processing table queue: {e}")

def start_background_threads():
    data_thread = threading.Thread(target=process_data_queue, daemon=True)
    table_thread = threading.Thread(target=process_table_queue, daemon=True)
    data_thread.start()
    table_thread.start()
