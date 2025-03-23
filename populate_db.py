from app import app, db, Hero, Item, Counter

# First, clear existing data
with app.app_context():
    db.drop_all()
    db.create_all()

    # Add all heroes
    heroes = [
        "Abrams", "Bebop", "Dynamo", "Grey Talon", "Haze",
        "Infernus", "Ivy", "Kelvin", "Lady Geist", "Lash",
        "Mcginnis", "Mo & Krill", "Paradox", "Pocket", "Seven",
        "Shiv", "Vindicta", "Viscous", "Warden", "Wraith", "Yamato"
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
            'SlowingHex', 'EtherealShift', 'SilenceGlyph', 'Suppressor',
            'MysticVulnerability', 'Curse', 'Decay', 'Knockdown',
            'BulletResistShredder', 'MysticBurst', 'MysticReach'
        ],
        'VitalityItems': [
            'ExtraStamina', 'MetalSkin', 'DebuffReducer', 'RescueBeam',
            'BulletArmor', 'Unstoppable', 'SpiritArmor', 'DebuffRemover',
            'ReactiveBarrier', 'ReturnFire', 'ExtraHealth', 'ExtraRegen'
        ],
        'WeaponItems': [
            'SlowingBullets', 'MonsterRounds', 'ToxicBullets',
            'BurstFire', 'LongRange', 'RapidRounds', 'Silencer'
        ]
    }
    
    # Add items to database
    item_objects = {}
    for category, items in item_categories.items():
        for item_name in items:
            item = Item(name=item_name, category=category)
            db.session.add(item)
            item_objects[item_name] = item

    db.session.commit()

    # Counter relationships
    counter_data = [
        ("Shiv", "ReactiveBarrier", 0.7),
        ("Shiv", "BurstFire", 0.8),
        ("Vindicta", "SilenceGlyph", 0.9),
        ("Vindicta", "SlowingBullets", 0.6),
        ("Wraith", "ToxicBullets", 0.8),
        ("Wraith", "EtherealShift", 0.7),
        ("Yamato", "DebuffReducer", 0.9),
        ("Yamato", "RescueBeam", 0.6),
        ("Viscous", "Knockdown", 0.8),
        ("Viscous", "Curse", 0.7),
        ("Warden", "DebuffReducer", 0.9),
        ("Warden", "SpiritArmor", 0.6),
        ("Mcginnis", "MetalSkin", 0.9),
        ("Mcginnis", "SilenceGlyph", 0.6),
        ("Haze", "BulletResistShredder", 0.9),
        ("Haze", "MysticVulnerability", 0.6),
        # Additional counters for more variety
        ("Abrams", "ToxicBullets", 0.8),
        ("Abrams", "Decay", 0.7),
        ("Bebop", "ReactiveBarrier", 0.9),
        ("Bebop", "DebuffRemover", 0.6),
        ("Dynamo", "Knockdown", 0.8),
        ("Dynamo", "EtherealShift", 0.7),
        ("Grey Talon", "SpiritArmor", 0.9),
        ("Grey Talon", "DebuffReducer", 0.6),
        ("Infernus", "ToxicBullets", 0.8),
        ("Infernus", "DebuffRemover", 0.7),
        ("Ivy", "Knockdown", 0.9),
        ("Ivy", "SilenceGlyph", 0.6),
        ("Kelvin", "ExtraStamina", 0.8),
        ("Kelvin", "EtherealShift", 0.7),
        ("Lady Geist", "SpiritArmor", 0.9),
        ("Lady Geist", "ToxicBullets", 0.6),
        ("Lash", "SlowingHex", 0.8),
        ("Lash", "Knockdown", 0.7),
        ("Mo & Krill", "ReactiveBarrier", 0.9),
        ("Mo & Krill", "ToxicBullets", 0.6),
        ("Paradox", "ReactiveBarrier", 0.8),
        ("Paradox", "ExtraStamina", 0.7),
        ("Pocket", "SpiritArmor", 0.9),
        ("Pocket", "DebuffRemover", 0.6),
        ("Seven", "Knockdown", 0.8),
        ("Seven", "ToxicBullets", 0.7)
    ]

    for hero_name, item_name, effectiveness in counter_data:
        # Find the hero and item objects
        hero = hero_objects[hero_name]
        item = item_objects[item_name]
        
        if hero and item:
            counter = Counter(hero_id=hero.id, item_id=item.id, effectiveness=effectiveness)
            db.session.add(counter)

    db.session.commit()

print("Database populated successfully!")
