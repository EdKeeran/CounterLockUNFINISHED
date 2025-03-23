from app import app, db, Hero, Item, Counter

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
            'AmmoScavenger', 'ArcaneSurge', 'BoundlessSpirit', 'BulletResistShredder',
            'ColdFront', 'Curse', 'Decay', 'DivinersKevlar', 'DurationExtender',
            'EchoShard', 'EscalatingExposure', 'EtherealShift', 'ExtraCharge',
            'ExtraSpirit', 'ImprovedBurst', 'ImprovedCooldown', 'ImprovedReach',
            'ImprovedSpirit', 'Infuser', 'Knockdown', 'MagicCarpet', 'MysticBurst',
            'MysticReach', 'MysticReverb', 'MysticSlow', 'MysticVulnerability',
            'QuickSilverReload', 'RapidRecharge', 'Refresher', 'SilenceGlyph',
            'SlowingHex', 'SpiritSnatch', 'SpiritStrike', 'SuperiorCooldown',
            'SuperiorDuration', 'Suppressor', 'SurgeofPower', 'TormentPulse',
            'WitheringWhip'
        ],
        'VitalityItems': [
            'BulletArmor', 'PhantomStrike', 'BulletLifesteal', 'ReactiveBarrier',
            'Colossus', 'RescueBeam', 'CombatBarrier', 'RestorativeLocket',
            'DebuffReducer', 'ReturnFire', 'DebuffRemover', 'SiphonBullets',
            'DivineBarrier', 'SoulRebirth', 'EnchantersBarrier', 'SpiritArmor',
            'EnduringSpeed', 'SpiritLifesteal', 'EnduringSpirit', 'SprintBoots',
            'ExtraHealth', 'SuperiorStamina', 'ExtraRegen', 'Unstoppable',
            'ExtraStamina', 'VeilWalker', 'Fortitude', 'Healbane',
            'HealingBooster', 'HealingRite', 'HealthNova', 'ImprovedBulletArmor',
            'ImprovedSpiritArmor', 'Inhibitor', 'Leech', 'Lifestrike',
            'MajesticLeap', 'MeleeLifesteal', 'MetalSkin'
        ],
        'WeaponItems': [
            'ActiveReload', 'PristineEmblem', 'AlchemicalFire', 'RapidRounds',
            'BasicMagazine', 'Ricochet', 'ShadowWeave', 'Berserker', 'BurstFire',
            'CloseQuarters', 'CripplingHeadshot', 'EscalatingResilience',
            'Sharpshooter', 'Silencer', 'SlowingBullets', 'SoulShredderBullets',
            'Fleetfoot', 'SpellslingerHeadshot', 'Frenzy', 'SpiritualOverflow',
            'GlassCannon', 'SwiftStriker', 'HeadHunter', 'TeslaBullets',
            'HeadshotBooster', 'TitanicMagazine', 'HeroicAura', 'ToxicBullets',
            'HighVelocityMag', 'VampiricBurst', 'HollowPointWard', 'WarpStone',
            'HuntersAura', 'IntensifyingMagazine', 'KineticDash', 'LongRange',
            'LuckyShot', 'MedicBullets', 'MeleeCharge', 'MonsterRounds',
            'MysticShot', 'PointBlank'
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
        ("Abrams", "HealBane", 0.8),
        ("Abrams", "Decay", 0.7),
        ("Abrams", "ToxicBullets", 0.7),
        ("Bebop", "ReactiveBarrier", 0.9),
        ("Bebop", "DebuffRemover", 0.6),
        ("Dynamo", "Knockdown", 0.8),
        ("Dynamo", "EtherealShift", 0.7),
        ("Dynamo", "Unstoppable", 0.8),
        ("Grey Talon", "SpiritArmor", 0.9),
        ("Grey Talon", "DebuffReducer", 0.6),
        ("Grey Talon", "DebuffRemover", 0.8),
        ("Grey Talon", "EtherealShift", 0.7),
        ("Haze", "WarpStone", 0.8),
        ("Haze", "ReturnFire", 0.8),
        ("Haze", "MetalSkin", 0.7),
        ("Infernus", "DebuffRemover", 0.8),
        ("Infernus", "ToxicBullets", 0.7),
        ("Infernus", "HealBane", 0.7),
        ("Infernus", "SlowingHex", 0.7),
        ("Infernus", "DebuffReducer", 0.8),
        ("Ivy", "SuperiorStamina", 0.8),
        ("Ivy", "WarpStone", 0.8),
        ("Ivy", "SilenceGlyph", 0.7),
        ("Ivy", "HealBane", 0.7),
        ("Ivy", "ToxicBullets", 0.7),
        ("Ivy", "Knockdown", 0.8),
        ("Kelvin", "SuperiorStamina", 0.8),
        ("Kelvin", "EtherealShift", 0.7),
        ("Kelvin", "HealBane", 0.7),
        ("Kelvin", "ToxicBullets", 0.7),
        ("Kelvin", "Decay", 0.7),
        ("Lady Geist", "Silencer", 0.8),
        ("Lady Geist", "SilenceGlyph", 0.8),
        ("Lady Geist", "ToxicBullets", 0.7),
        ("Lady Geist", "HealBane", 0.7),
        ("Lady Geist", "Decay", 0.7),
        ("Lady Geist", "SpiritArmor", 0.8),
        ("Lash", "SlowingHex", 0.8),
        ("Lash", "SilenceGlyph", 0.8),
        ("Lash", "EtherealShift", 0.7),
        ("Lash", "Knockdown", 0.8),
        ("Lash", "Unstoppable", 0.7),
        ("Mcginnis", "SuperiorStamina", 0.8),
        ("Mcginnis", "MonsterRounds", 0.8),
        ("Mo & Krill", "SuperiorStamina", 0.8),
        ("Mo & Krill", "ReactiveBarrier", 0.8),
        ("Mo & Krill", "ToxicBullets", 0.7),
        ("Mo & Krill", "Knockdown", 0.8),
        ("Mo & Krill", "SlowingHex", 0.7),
        ("Mo & Krill", "HealBane", 0.7),
        ("Paradox", "ReactiveBarrier", 0.8),
        ("Paradox", "ExtraStamina", 0.7),
        ("Paradox", "EtherealShift", 0.8),
        ("Pocket", "SpiritArmor", 0.9),
        ("Pocket", "DebuffRemover", 0.6),
        ("Pocket", "DebuffReducer", 0.8),
        ("Pocket", "SilenceGlyph", 0.8),
        ("Seven", "Knockdown", 0.8),
        ("Shiv", "HealBane", 0.8),
        ("Shiv", "ToxicBullets", 0.7),
        ("Shiv", "Decay", 0.7),
        ("Shiv", "DebuffReducer", 0.8),
        ("Shiv", "DebuffRemover", 0.8),
        ("Vindicta", "SuperiorStamina", 0.8),
        ("Vindicta", "DebuffRemover", 0.8),
        ("Vindicta", "EtherealShift", 0.7),
        ("Vindicta", "Knockdown", 0.8),
        ("Viscous", "SuperiorStamina", 0.8),
        ("Viscous", "SilenceGlyph", 0.8),
        ("Warden", "SuperiorStamina", 0.8),
        ("Warden", "DebuffRemover", 0.8),
        ("Warden", "DebuffReducer", 0.8),
        ("Warden", "EtherealShift", 0.7),
        ("Warden", "SlowingHex", 0.7),
        ("Warden", "HealBane", 0.7),
        ("Warden", "ToxicBullets", 0.7),
        ("Warden", "Decay", 0.7),
        ("Wraith", "ToxicBullets", 0.8),
        ("Wraith", "EtherealShift", 0.7),
        ("Wraith", "MetalSkin", 0.8),
        ("Wraith", "ReturnFire", 0.8),
        ("Yamato", "DebuffReducer", 0.9),
        ("Yamato", "RescueBeam", 0.6),
        ("Yamato", "SilenceGlyph", 0.8)
    ]

    for hero_name, item_name, effectiveness in counter_data:
        # Find the hero and item objects
        hero = hero_objects[hero_name]
        item = item_objects.get(item_name)
        
        if hero and item:
            counter = Counter(hero_id=hero.id, item_id=item.id, effectiveness=effectiveness)
            db.session.add(counter)

    db.session.commit()

print("Database populated successfully!")
