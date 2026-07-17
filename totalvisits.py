import os
LOG_FILE = "logs/allgemein.txt"
if not os.path.exists(LOG_FILE):
    print("Total Visits: 0")
else:
    with open(LOG_FILE, 'r', encoding='utf-8') as f:
        visits = [l for l in f.readlines() if "Visit from IP:" in l]
        print(f"Total Visits: {len(visits)}")
