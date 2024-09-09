from flask import Blueprint, request, jsonify
from app.models import Entry
from app import db

entry_routes = Blueprint('entry_routes', __name__)

@entry_routes.route('/entries/sort', methods=['GET'])
def sort_entries():
    sort_by = request.args.get('sort_by', 'most_upvoted')
    
    if sort_by == 'most_upvoted':
        entries = Entry.query.order_by(Entry.upvotes.desc()).all()
    elif sort_by == 'most_downvoted':
        entries = Entry.query.order_by(Entry.downvotes.desc()).all()
    else:
        return jsonify({'error': 'Invalid sort parameter'}), 400
    
    return jsonify([entry.to_dict() for entry in entries])