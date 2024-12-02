from flask import Blueprint, request, jsonify
from app.services import insert_data, insert_table
from app.queues import data_queue, table_queue
import logging


logger = logging.getLogger(__name__)

bp = Blueprint('main', __name__)

@bp.route('/data', methods=['POST'])
def receive_data():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON'}), 400
    
    temperature = data.get('temperature')
    if temperature is None:
        return jsonify({'error': 'Missing required field (temperature)'}), 400
    
    humidity = data.get('humidity', '')
    gas_level = data.get('gas_level', '')
    
    try:
        data_id = insert_data(temperature, humidity, gas_level)
        data_queue.put({'id': data_id, 'temperature': temperature, 'humidity': humidity, 'gas_level': gas_level})
        logger.info(f"Data received and queued with id={data_id}")
        return jsonify({'status': 'ok'}), 200
    except Exception as e:
        logger.error(f"Error inserting data: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@bp.route('/table', methods=['POST'])
def receive_table():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON'}), 400
    
    seat1 = data.get('seat1')
    if seat1 is None:
        return jsonify({'error': 'Missing required field (seat1)'}), 400
    
    seat2 = data.get('seat2', 0)
    seat3 = data.get('seat3', 0)
    seat4 = data.get('seat4', 0)
    
    try:
        table_id = insert_table(seat1, seat2, seat3, seat4)
        table_queue.put({'id': table_id, 'seat1': seat1, 'seat2': seat2, 'seat3': seat3, 'seat4': seat4})
        logger.info(f"Table data received and queued with id={table_id}")
        return jsonify({'status': 'ok'}), 200
    except Exception as e:
        logger.error(f"Error inserting table data: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
