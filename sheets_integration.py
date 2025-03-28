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
        
        # Get data from the CounterItems sheet, including counter reason
        range_name = 'CounterItems!A:C'  # Updated to include column C
        result = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=range_name
        ).execute()
        
        # Extract counter items and reasons for this hero
        values = result.get('values', [])[1:]  # Skip header row
        counter_items = []
        for row in values:
            if len(row) > 1 and row[0] == hero_name:
                counter_info = {
                    'item': row[1],
                    'reason': row[2] if len(row) > 2 else ''  # Get reason if available
                }
                counter_items.append(counter_info)
        
        # Cache the results
        cache[cache_key] = counter_items
        print(f"Got {len(counter_items)} counters for {hero_name}")
        return counter_items
        
    except Exception as e:
        print(f"Error fetching counters for {hero_name}: {str(e)}")
        return []
