from google.oauth2 import service_account
from googleapiclient.discovery import build
from cachetools import TTLCache
import os

# Initialize cache with 5-minute TTL
cache = TTLCache(maxsize=100, ttl=300)  # 300 seconds = 5 minutes

# Constants
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']  # Full access to sheets
SPREADSHEET_ID = '1Ud4vuNexn7eGmBp4WHDrOHRFTxsIDhIkNZPUlwVLWgc'

def get_credentials():
    creds_path = os.path.join('credentials', 'google_sheets.json')
    print(f"Loading credentials from {creds_path}")
    return service_account.Credentials.from_service_account_file(
        creds_path, scopes=SCOPES
    )

def populate_counters():
    """Add counter data to Google Sheets."""
    counter_data = [
        ["Hero Name", "Counter Item"],  # Headers
        ["Abrams", "Healbane"],
        ["Abrams", "Decay"],
        ["Abrams", "ToxicBullets"],
        ["Bebop", "ReactiveBarrier"],
        ["Bebop", "DebuffRemover"],
        ["Calico", "SlowingHex"],
        ["Dynamo", "Knockdown"],
        ["Dynamo", "EtherealShift"],
        ["Dynamo", "Unstoppable"],
        ["Grey Talon", "SpiritArmor"],
        ["Grey Talon", "DebuffReducer"],
        ["Grey Talon", "DebuffRemover"],
        ["Grey Talon", "EtherealShift"],
        ["Haze", "WarpStone"],
        ["Haze", "ReturnFire"],
        ["Haze", "MetalSkin"],
        ["Infernus", "DebuffRemover"],
        ["Infernus", "ToxicBullets"],
        ["Infernus", "Healbane"],
        ["Infernus", "SlowingHex"],
        ["Infernus", "DebuffReducer"],
        ["Ivy", "SuperiorStamina"],
        ["Ivy", "WarpStone"],
        ["Ivy", "SilenceGlyph"],
        ["Ivy", "Healbane"],
        ["Ivy", "ToxicBullets"],
        ["Ivy", "Knockdown"],
        ["Kelvin", "SuperiorStamina"],
        ["Kelvin", "EtherealShift"],
        ["Kelvin", "Healbane"],
        ["Kelvin", "ToxicBullets"],
        ["Kelvin", "Decay"],
        ["Lady Geist", "Silencer"],
        ["Lady Geist", "SilenceGlyph"],
        ["Lady Geist", "ToxicBullets"],
        ["Lady Geist", "Healbane"],
        ["Lady Geist", "Decay"],
        ["Lady Geist", "SpiritArmor"],
        ["Lash", "SlowingHex"],
        ["Lash", "SilenceGlyph"],
        ["Lash", "EtherealShift"],
        ["Lash", "Knockdown"],
        ["Lash", "Unstoppable"],
        ["Mcginnis", "SuperiorStamina"],
        ["Mcginnis", "MonsterRounds"],
        ["Mo & Krill", "SuperiorStamina"],
        ["Mo & Krill", "ReactiveBarrier"],
        ["Mo & Krill", "ToxicBullets"],
        ["Mo & Krill", "Knockdown"],
        ["Mo & Krill", "SlowingHex"],
        ["Mo & Krill", "Healbane"],
        ["Paradox", "ReactiveBarrier"],
        ["Paradox", "ExtraStamina"],
        ["Paradox", "EtherealShift"],
        ["Pocket", "SpiritArmor"],
        ["Pocket", "DebuffRemover"],
        ["Pocket", "DebuffReducer"],
        ["Pocket", "SilenceGlyph"],
        ["Seven", "Knockdown"],
        ["Shiv", "Healbane"],
        ["Shiv", "ToxicBullets"],
        ["Shiv", "Decay"],
        ["Shiv", "DebuffReducer"],
        ["Shiv", "DebuffRemover"],
        ["Vindicta", "SuperiorStamina"],
        ["Vindicta", "DebuffRemover"],
        ["Vindicta", "EtherealShift"],
        ["Vindicta", "Knockdown"],
        ["Viscous", "SuperiorStamina"],
        ["Viscous", "SilenceGlyph"],
        ["Warden", "SuperiorStamina"],
        ["Warden", "DebuffRemover"],
        ["Warden", "DebuffReducer"],
        ["Warden", "EtherealShift"],
        ["Warden", "SlowingHex"],
        ["Warden", "Healbane"],
        ["Warden", "ToxicBullets"],
        ["Warden", "Decay"],
        ["Wraith", "ToxicBullets"],
        ["Wraith", "EtherealShift"],
        ["Wraith", "MetalSkin"],
        ["Wraith", "ReturnFire"],
        ["Yamato", "DebuffReducer"],
        ["Yamato", "RescueBeam"],
        ["Yamato", "SilenceGlyph"]
    ]
    
    try:
        creds = get_credentials()
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        
        # Clear existing data in CounterItems sheet
        sheet.values().clear(
            spreadsheetId=SPREADSHEET_ID,
            range='CounterItems!A:B'
        ).execute()
        
        # Add new counter data
        body = {
            'values': counter_data
        }
        result = sheet.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range='CounterItems!A1',
            valueInputOption='RAW',
            body=body
        ).execute()
        
        print(f"Updated {result.get('updatedCells')} cells")
        
    except Exception as e:
        print(f"Error updating counter data: {str(e)}")

def get_hero_items(hero_name):
    """Get items for a specific hero from Google Sheets."""
    cache_key = f'hero_items_{hero_name}'
    
    # Check cache first
    if cache_key in cache:
        print(f"Found cached items for {hero_name}")
        return cache[cache_key]
    
    try:
        print(f"Fetching items for {hero_name} from Google Sheets")
        creds = get_credentials()
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        
        # Get data from the FriendlyItems sheet
        range_name = 'FriendlyItems!A:B'
        result = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=range_name
        ).execute()
        
        # Extract items for this hero
        values = result.get('values', [])[1:]  # Skip header row
        items = [row[1] for row in values if len(row) > 1 and row[0] == hero_name]
        
        # Cache the results
        cache[cache_key] = items
        print(f"Got {len(items)} items for {hero_name}")
        return items
        
    except Exception as e:
        print(f"Error fetching items for {hero_name}: {str(e)}")
        return []

def get_hero_counters(hero_name):
    """Get counter items for a specific hero from Google Sheets."""
    cache_key = f'hero_counters_{hero_name}'
    
    # Check cache first
    if cache_key in cache:
        print(f"Found cached counters for {hero_name}")
        return cache[cache_key]
    
    try:
        print(f"Fetching counters for {hero_name} from Google Sheets")
        creds = get_credentials()
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        
        # Get data from the CounterItems sheet
        range_name = 'CounterItems!A:B'
        result = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=range_name
        ).execute()
        
        # Extract counter items for this hero
        values = result.get('values', [])[1:]  # Skip header row
        counter_items = [row[1] for row in values if len(row) > 1 and row[0] == hero_name]
        
        # Cache the results
        cache[cache_key] = counter_items
        print(f"Got {len(counter_items)} counters for {hero_name}")
        return counter_items
        
    except Exception as e:
        print(f"Error fetching counters for {hero_name}: {str(e)}")
        return []
