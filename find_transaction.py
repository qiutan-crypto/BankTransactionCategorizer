import json
import os

file_path = "c:\\Users\\Lifeng Liu\\OneDrive\\文档\\Python Script\\Bank Transaction Categorizer\\ProjectBackup_2026-01-08T22-27-12-427Z.json"

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"Loaded {len(data)} items (or keys if dict)")
    
    transactions = []
    if isinstance(data, list):
        transactions = data
    elif isinstance(data, dict):
        if 'transactions' in data:
            transactions = data['transactions']
        else:
            # Maybe it's a state export
            transactions = data.get('state', {}).get('transactions', [])

    print(f"Found {len(transactions)} transactions")

    found_count = 0
    for i, tx in enumerate(transactions):
        # Replicate logic from applyRules
        # fields: Description, description, Bank Description, Payee, From/To, "From To"
        
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
        print("No matches found for '3122' or 'pay the check'.")

except Exception as e:
    print(f"Error: {e}")
