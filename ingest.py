# -------------------------------------------------
# ingest.py (API endpoints for device/ThingSpeak)
# -------------------------------------------------
from flask import Blueprint, request, jsonify, abort
from database import db
from models import Reading
from config import Config


bp_ingest = Blueprint('ingest', __name__, url_prefix='/api')


@bp_ingest.post('/ingest')
def ingest():
    # Optional simple API key check
    api_key = request.headers.get('X-INGEST-KEY') or request.args.get('key')
    if Config.INGEST_API_KEY and api_key != Config.INGEST_API_KEY:
        abort(401, description='Invalid ingest key')


    payload = request.get_json(silent=True) or {}
    element_id = payload.get('element_id')
    temperature_c = payload.get('temperature_c')
    
    # ThingSpeak field mapping: field number = element_id, field value = temperature
    # e.g., {"field1":"30.00"} means element_id="1" with temperature=30.0
    if element_id is None or temperature_c is None:
        # Check all possible ThingSpeak fields (field1-field8)
        for field_num in range(1, 9):
            field_key = f'field{field_num}'
            if field_key in payload:
                try:
                    element_id = str(field_num)  # Field number becomes element_id
                    temperature_c = float(payload[field_key])  # Field value is temperature
                    break
                except (ValueError, TypeError):
                    continue

    if element_id is None or temperature_c is None:
        abort(400, description='element_id and temperature_c are required. Send either direct values or ThingSpeak field format.')


    r = Reading(element_id=element_id, temperature_c=float(temperature_c))
    db.session.add(r)
    db.session.commit()


    return jsonify({'status': 'ok', 'id': r.id, 'recorded_at': r.recorded_at.isoformat() + 'Z'})