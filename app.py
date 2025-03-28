from flask import Flask, render_template, jsonify, request, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import json
from sheets_integration import get_hero_items, get_hero_counters

app = Flask(__name__, 
           static_folder='static',  # Use local static folder
           static_url_path='/static')

# Use SQLite for local development, but store in /tmp for Render deployment
if os.environ.get('RENDER'):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/counterlock.db'
    # Set up Google Sheets credentials from environment variable
    if os.environ.get('GOOGLE_SHEETS_CREDENTIALS'):
        creds_dir = 'credentials'
        if not os.path.exists(creds_dir):
            os.makedirs(creds_dir)
        creds_path = os.path.join(creds_dir, 'google_sheets.json')
        with open(creds_path, 'w') as f:
            f.write(os.environ.get('GOOGLE_SHEETS_CREDENTIALS'))
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///counterlock.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

db = SQLAlchemy(app)

# Database Models
class Hero(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    image_path = db.Column(db.String(200), nullable=False, default='placeholder.jpg')
    
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    image_path = db.Column(db.String(200), nullable=False, default='placeholder.png')

# Initialize database and populate with data
def init_db():
    with app.app_context():
        # Force recreation of database
        db.drop_all()
        db.create_all()
        
        # Only populate if database is empty
        if not Hero.query.first():
            import populate_db  # This will populate the database

# Routes
@app.route('/')
def index():
    heroes = Hero.query.all()
    # Get all items grouped by category
    spirit_items = Item.query.filter_by(category='SpiritItems').all()
    vitality_items = Item.query.filter_by(category='VitalityItems').all()
    weapon_items = Item.query.filter_by(category='WeaponItems').all()

    return render_template('index.html', 
                         heroes=heroes,
                         spirit_items=spirit_items,
                         vitality_items=vitality_items,
                         weapon_items=weapon_items)

@app.route('/api/heroes')
def get_heroes():
    heroes = Hero.query.all()
    return jsonify([{
        'id': h.id,
        'name': h.name,
        'image_url': url_for('static', filename=h.image_path.replace(' ', ''))  # Remove spaces from image path
    } for h in heroes])

@app.route('/api/team_analysis', methods=['POST'])
def analyze_team():
    try:
        data = request.get_json()
        enemy_team = data.get('enemy_team', [])
        
        if not enemy_team:
            return jsonify({'error': 'No enemy team provided'})
            
        # Get all counter items for each enemy hero
        item_analysis = {}
        for hero_id in enemy_team:
            hero = Hero.query.get(hero_id)
            if hero:
                counter_items = get_hero_counters(hero.name)
                for counter_info in counter_items:
                    item_name = counter_info['item']
                    counter_reason = counter_info['reason']
                    if item_name not in item_analysis:
                        item = Item.query.filter_by(name=item_name).first()
                        if item:
                            item_analysis[item_name] = {
                                'name': item.name,
                                'image_path': url_for('static', filename=item.image_path.replace(' ', '')),  # Remove spaces from image path
                                'category': item.category,
                                'countered_heroes': []
                            }
                    if item_name in item_analysis:
                        item_analysis[item_name]['countered_heroes'].append({
                            'name': hero.name,
                            'image_path': url_for('static', filename=hero.image_path.replace(' ', '')),  # Remove spaces from image path
                            'counter_reason': counter_reason
                        })
        
        # Convert to list and sort by number of heroes countered
        item_analysis_list = list(item_analysis.values())
        item_analysis_list.sort(key=lambda x: len(x['countered_heroes']), reverse=True)
        
        return jsonify({'item_analysis': item_analysis_list})
        
    except Exception as e:
        print(f"Error in analyze_team: {str(e)}")
        return jsonify({'error': str(e)})

# Initialize database when starting the app
init_db()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
