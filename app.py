from flask import Flask, render_template, jsonify, request, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from sheets_integration import get_hero_items, get_hero_counters

app = Flask(__name__)

# Use SQLite for local development, but store in /tmp for Render deployment
if os.environ.get('RENDER'):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/counterlock.db'
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

class Counter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hero_id = db.Column(db.Integer, db.ForeignKey('hero.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    effectiveness = db.Column(db.Float, nullable=False)

class HeroItems(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hero_id = db.Column(db.Integer, db.ForeignKey('hero.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)

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

@app.route('/api/counters')
def get_counters():
    # Get all counter relationships with their associated heroes and items
    counters = Counter.query.all()
    counter_data = []
    
    # Group counters by hero
    hero_counters = {}
    for counter in counters:
        hero = Hero.query.get(counter.hero_id)
        item = Item.query.get(counter.item_id)
        
        if hero.name not in hero_counters:
            hero_counters[hero.name] = {
                'hero_name': hero.name,
                'counter_items': []
            }
        
        hero_counters[hero.name]['counter_items'].append({
            'name': item.name,
            'category': item.category,
            'effectiveness': counter.effectiveness
        })
    
    return jsonify(list(hero_counters.values()))

@app.route('/api/recommend', methods=['POST'])
def recommend_items():
    enemy_team = request.json.get('enemy_team', [])
    
    # Get all items that counter the enemy heroes
    counters = Counter.query.filter(Counter.hero_id.in_(enemy_team)).all()
    
    # Calculate effectiveness levels
    item_scores = {}
    for counter in counters:
        if counter.item_id not in item_scores:
            item_scores[counter.item_id] = {
                'heroes_countered': 0,
                'total_effectiveness': 0
            }
        item_scores[counter.item_id]['heroes_countered'] += 1
        item_scores[counter.item_id]['total_effectiveness'] += counter.effectiveness

    # Calculate final rankings (Level 1-6)
    rankings = []
    for item_id, scores in item_scores.items():
        item = Item.query.get(item_id)
        level = min(6, max(1, scores['heroes_countered']))
        rankings.append({
            'id': item.id,
            'name': item.name,
            'category': item.category,
            'level': level,
            'heroes_countered': scores['heroes_countered'],
            'effectiveness': scores['total_effectiveness'] / scores['heroes_countered']
        })
    
    # Sort by effectiveness and heroes countered
    rankings.sort(key=lambda x: (-x['heroes_countered'], -x['effectiveness']))
    
    return jsonify(rankings)

@app.route('/api/team_analysis', methods=['POST'])
def analyze_teams():
    enemy_team = request.json.get('enemy_team', [])
    friendly_team = request.json.get('friendly_team', [])
    
    print(f"Analyzing teams - Enemy: {enemy_team}, Friendly: {friendly_team}")
    
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
                                'name': other_hero.name,
                                'effectiveness': 1.0
                            })
                
                counter_items.append({
                    'id': item.id,
                    'name': item.name,
                    'category': item.category,
                    'effectiveness': 1.0,  # Default effectiveness
                    'also_counters': other_countered_heroes
                })
        
        print(f"Found {len(counter_items)} valid counter items for {hero.name}")
        enemy_analysis[hero_id] = {
            'hero_name': hero.name,
            'counter_items': sorted(counter_items, key=lambda x: (-len(x['also_counters']), x['name']))
        }
    
    # Get items for friendly heroes from Google Sheets
    friendly_analysis = {}
    for hero_id in friendly_team:
        hero = heroes[hero_id]
        print(f"\nAnalyzing friendly hero: {hero.name}")
        
        # Get hero's items from Google Sheets
        hero_items = get_hero_items(hero.name)
        print(f"Found {len(hero_items)} items for {hero.name} in sheet")
        items_data = []
        
        for item_name in hero_items:
            if item_name in items:
                item = items[item_name]
                # Check which enemies this item counters
                countered_enemies = []
                for enemy_id in enemy_team:
                    enemy = heroes[enemy_id]
                    if item_name in get_hero_counters(enemy.name):
                        countered_enemies.append({
                            'name': enemy.name,
                            'effectiveness': 1.0  # Default effectiveness
                        })
                
                if countered_enemies:  # Only include items that counter enemies
                    items_data.append({
                        'id': item.id,
                        'name': item.name,
                        'category': item.category,
                        'counters': sorted(countered_enemies, key=lambda x: x['name'])
                    })
        
        print(f"Found {len(items_data)} valid items for {hero.name}")
        friendly_analysis[hero_id] = {
            'hero_name': hero.name,
            'items': sorted(items_data, key=lambda x: (-len(x['counters']), x['name']))
        }
    
    print("\nSending analysis response")
    return jsonify({
        'enemy_analysis': enemy_analysis,
        'friendly_analysis': friendly_analysis
    })

# Initialize database when starting the app
init_db()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
