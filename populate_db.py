from app import app, db, Hero, Item
from sheets_integration import populate_counters, populate_friendly_items

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

    # Populate Google Sheets with counter data
    populate_counters()
    populate_friendly_items()

    print("Database populated successfully!")
