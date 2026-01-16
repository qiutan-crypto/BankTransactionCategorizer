import json

file_path = "c:\\Users\\Lifeng Liu\\OneDrive\\文档\\Python Script\\Bank Transaction Categorizer\\ProjectBackup_2026-01-08T22-27-12-427Z.json"

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"Type of data: {type(data)}")
    if isinstance(data, dict):
        print(f"Keys: {list(data.keys())}")
        for k in data.keys():
            print(f"Type of data['{k}']: {type(data[k])}")
            if isinstance(data[k], list):
                 print(f"Length of data['{k}']: {len(data[k])}")
    
except Exception as e:
    print(f"Error: {e}")
