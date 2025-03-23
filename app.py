from flask import Flask, render_template, jsonify, request, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

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
    effectiveness = db.Column(db.Float, nullable=False)  # How well the item counters the hero (1-10)

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
    
    # Get all counters for enemy heroes
    enemy_counters = Counter.query.filter(Counter.hero_id.in_(enemy_team)).all()
    
    # Organize counters by enemy hero
    enemy_analysis = {}
    for hero_id in enemy_team:
        hero = Hero.query.get(hero_id)
        hero_counters = [c for c in enemy_counters if c.hero_id == hero_id]
        
        # Get items that counter this hero
        counter_items = []
        for counter in hero_counters:
            item = Item.query.get(counter.item_id)
            counter_items.append({
                'id': item.id,
                'name': item.name,
                'category': item.category,
                'effectiveness': counter.effectiveness
            })
        
        enemy_analysis[hero_id] = {
            'hero_name': hero.name,
            'counter_items': sorted(counter_items, key=lambda x: x['effectiveness'], reverse=True)
        }
    
    # Analyze which friendly heroes should buy which items
    friendly_recommendations = {}
    for hero_id in friendly_team:
        hero = Hero.query.get(hero_id)
        
        # Get all possible counter items needed
        needed_items = set()
        for counters in enemy_analysis.values():
            for item in counters['counter_items']:
                needed_items.add(item['id'])
        
        # Find which items this hero has high effectiveness with
        hero_counters = Counter.query.filter_by(hero_id=hero_id).all()
        hero_items = []
        for counter in hero_counters:
            if counter.item_id in needed_items:
                item = Item.query.get(counter.item_id)
                hero_items.append({
                    'id': item.id,
                    'name': item.name,
                    'category': item.category,
                    'effectiveness': counter.effectiveness
                })
        
        friendly_recommendations[hero_id] = {
            'hero_name': hero.name,
            'recommended_items': sorted(hero_items, key=lambda x: x['effectiveness'], reverse=True)
        }
    
    return jsonify({
        'enemy_analysis': enemy_analysis,
        'friendly_recommendations': friendly_recommendations
    })

# Initialize database when starting the app
init_db()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
