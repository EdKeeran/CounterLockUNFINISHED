from app import app, db, Hero, Item

# First, clear existing data
with app.app_context():
    db.drop_all()
    db.create_all()

    # Add all heroes
    heroes = [
        "Abrams", "Bebop", "Calico", "Dynamo", "Grey Talon", "Haze",
        "Holliday", "Infernus", "Ivy", "Kelvin", "Lady Geist", "Lash",
        "Mcginnis", "Mirage", "Mo & Krill", "Paradox", "Pocket", "Seven",
        "Shiv", "Sinclair", "Vindicta", "Viscous", "Vyper", "Warden", "Wraith", "Yamato"
    ]
    
    # Add heroes to database with image paths
    hero_objects = {}
    for hero_name in heroes:
        # Convert hero name to match the PNG filename exactly
        image_name = hero_name.replace(' & ', '&').replace(' ', '')
        hero = Hero(name=hero_name, image_path=f"images/heroes/{image_name}.png.png")
        db.session.add(hero)
        hero_objects[hero_name] = hero

    # Map item names to their categories
    item_categories = {
        'SpiritItems': [
            'Ammo Scavenger', 'Arcane Surge', 'Boundless Spirit', 'Bullet Resist Shredder',
            'Cold Front', 'Curse', 'Decay', 'Diviners Kevlar', 'Duration Extender',
            'Echo Shard', 'Escalating Exposure', 'Ethereal Shift', 'Extra Charge',
            'Extra Spirit', 'Improved Burst', 'Improved Cooldown', 'Improved Reach',
            'Improved Spirit', 'Infuser', 'Knockdown', 'Magic Carpet', 'Mystic Burst',
            'Mystic Reach', 'Mystic Reverb', 'Mystic Slow', 'Mystic Vulnerability',
            'Quick Silver Reload', 'Rapid Recharge', 'Refresher', 'Silence Glyph',
            'Slowing Hex', 'Spirit Snatch', 'Spirit Strike', 'Superior Cooldown',
            'Superior Duration', 'Suppressor', 'Surge Of Power', 'Torment Pulse',
            'Withering Whip'
        ],
        'VitalityItems': [
            'Bullet Armor', 'Phantom Strike', 'Bullet Lifesteal', 'Reactive Barrier',
            'Colossus', 'Rescue Beam', 'Combat Barrier', 'Restorative Locket',
            'Debuff Reducer', 'Return Fire', 'Debuff Remover', 'Siphon Bullets',
            'Divine Barrier', 'Soul Rebirth', 'Enchanters Barrier', 'Spirit Armor',
            'Enduring Speed', 'Spirit Lifesteal', 'Enduring Spirit', 'Sprint Boots',
            'Extra Health', 'Superior Stamina', 'Extra Regen', 'Unstoppable',
            'Extra Stamina', 'Veil Walker', 'Fortitude', 'Healbane',
            'Healing Booster', 'Healing Rite', 'Health Nova', 'Improved Bullet Armor',
            'Improved Spirit Armor', 'Inhibitor', 'Leech', 'Lifestrike',
            'Majestic Leap', 'Melee Lifesteal', 'Metal Skin'
        ],
        'WeaponItems': [
            'Active Reload', 'Pristine Emblem', 'Alchemical Fire', 'Rapid Rounds',
            'Basic Magazine', 'Ricochet', 'Shadow Weave', 'Berserker', 'Burst Fire',
            'CloseQuarters', 'Crippling Headshot', 'Escalating Resilience',
            'Sharpshooter', 'Silencer', 'Slowing Bullets', 'Soul Shredder Bullets',
            'Fleetfoot', 'SpellslingerHeadshot', 'Frenzy', 'Spiritual Overflow',
            'Glass Cannon', 'Swift Striker', 'Head Hunter', 'Tesla Bullets',
            'Headshot Booster', 'Titanic Magazine', 'Heroic Aura', 'Toxic Bullets',
            'High Velocity Mag', 'Vampiric Burst', 'Hollow Point Ward', 'Warp Stone',
            'Hunters Aura', 'Intensifying Magazine', 'Kinetic Dash', 'Long Range',
            'Lucky Shot', 'Medic Bullets', 'Melee Charge', 'Monster Rounds',
            'Mystic Shot', 'Point Blank'
        ]
    }
    
    # Add items to database with image paths
    for category, items in item_categories.items():
        for item_name in items:
            # Use the exact item name and category for the image path
            item = Item(
                name=item_name,
                category=category,
                image_path=f"images/items/{category}/{item_name}.png"
            )
            db.session.add(item)

    # Commit all changes
    db.session.commit()
    print("Database populated successfully!")
