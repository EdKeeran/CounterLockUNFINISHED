from flask import Flask, render_template, jsonify, request, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import json
from sheets_integration import get_hero_items, get_hero_counters

app = Flask(__name__)

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
        'image_url': url_for('static', filename=h.image_path)
    } for h in heroes])

@app.route('/api/team_analysis', methods=['POST'])
def analyze_teams():
    enemy_team = request.json.get('enemy_team', [])
    
    print(f"Analyzing enemy team: {enemy_team}")
    
    # Get all heroes
    heroes = {h.id: h for h in Hero.query.all()}
    items = {i.name: i for i in Item.query.all()}
    
    print(f"Found {len(heroes)} heroes and {len(items)} items in database")
    
    # Organize counters by enemy hero
    enemy_analysis = {}
    for hero_id in enemy_team:
        hero = heroes[hero_id]
        print(f"\nAnalyzing enemy hero: {hero.name}")
        
        # Get counter items from Google Sheets
        counter_items = []
        sheet_items = get_hero_counters(hero.name)
        print(f"Found {len(sheet_items)} counter items for {hero.name} in sheet")
        
        for item_name in sheet_items:
            if item_name in items:
                item = items[item_name]
                # Find other enemy heroes that are also countered by this item
                other_countered_heroes = []
                for other_id in enemy_team:
                    if other_id != hero_id:
                        other_hero = heroes[other_id]
                        other_counters = get_hero_counters(other_hero.name)
                        if item_name in other_counters:
                            other_countered_heroes.append({
                                'name': other_hero.name
                            })
                
                counter_items.append({
                    'id': item.id,
                    'name': item.name,
                    'category': item.category,
                    'also_counters': other_countered_heroes
                })
        
        print(f"Found {len(counter_items)} valid counter items for {hero.name}")
        enemy_analysis[hero_id] = {
            'hero_name': hero.name,
            'counter_items': sorted(counter_items, key=lambda x: (-len(x['also_counters']), x['name']))
        }
    
    print("\nSending analysis response")
    return jsonify({
        'enemy_analysis': enemy_analysis
    })

# Initialize database when starting the app
init_db()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
