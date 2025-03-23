# CounterLock

A Deadlock counter-item recommendation system that helps players make strategic item choices based on enemy team composition.

## Features
- Select enemy heroes to see what items counter them
- Get item recommendations ranked by effectiveness
- Items are categorized into:
  - Spirit Items (Purple)
  - Vitality Items (Green)
  - Weapon Items (Orange)
- Each item shows:
  - Item image and name
  - Category with color coding
  - Effectiveness level (1-6)
  - Number of enemy heroes countered

## Setup
1. Clone this repository:
```bash
git clone https://github.com/yourusername/CounterLock.git
cd CounterLock
```

2. Create a Python virtual environment (recommended):
```bash
python -m venv venv
.\venv\Scripts\activate  # On Windows
source venv/bin/activate  # On macOS/Linux
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
python populate_db.py
```

5. Run the application:
```bash
python app.py
```

6. Open your web browser and visit:
```
http://127.0.0.1:5000
```

## How to Use
1. Click on enemy hero portraits to select them
2. The system will automatically show recommended items
3. Items are ranked by:
   - Number of heroes countered
   - Overall effectiveness against those heroes
4. Each item shows its effectiveness level:
   - Level 6: Counters multiple heroes very effectively
   - Level 1: Counters at least one hero

## Contributing
Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## License
[Your chosen license]
