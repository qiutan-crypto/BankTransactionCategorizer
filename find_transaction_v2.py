import json

file_path = "c:\\Users\\Lifeng Liu\\OneDrive\\文档\\Python Script\\Bank Transaction Categorizer\\ProjectBackup_2026-01-08T22-27-12-427Z.json"

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        root = json.load(f)
    
    data = root.get('data', {})
    print(f"Keys in root['data']: {list(data.keys())}")
    
    transactions = data.get('transactions', [])
    print(f"Found {len(transactions)} transactions in root['data']['transactions']")
    
    rules = data.get('rules', [])
    print(f"Found {len(rules)} rules in root['data']['rules']")

    found_count = 0
    for i, tx in enumerate(transactions):
        if not tx: continue 
        # Replicate logic from applyRules
        parts = []
        for key in ['Description', 'description', 'Bank Description', 'Payee', 'From/To', 'From To']:
            val = tx.get(key)
            if val:
                parts.append(str(val))
        
        full_desc = " ".join(parts)
        
        # Search for 3122
        if "3122" in full_desc or "3122" in str(tx):
            print(f"\n--- Found 3122 in Transaction {i} ---")
            print(f"Full Desc: {full_desc}")
            print(f"Raw Object: {json.dumps(tx, ensure_ascii=False, indent=2)}")
            found_count += 1
            
        if "pay the check" in full_desc.lower() or "pay the check" in str(tx).lower():
             print(f"\n--- Found 'pay the check' in Transaction {i} ---")
             print(f"Full Desc: {full_desc}")
             print(f"Raw Object: {json.dumps(tx, ensure_ascii=False, indent=2)}")
             found_count += 1
             
    if found_count == 0:
        print("No matches found for '3122' or 'pay the check' in transactions.")

except Exception as e:
    print(f"Error: {e}")
