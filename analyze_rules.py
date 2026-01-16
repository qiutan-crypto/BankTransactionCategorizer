import json
import re

file_path = "c:\\Users\\Lifeng Liu\\OneDrive\\文档\\Python Script\\Bank Transaction Categorizer\\ProjectBackup_2026-01-08T22-27-12-427Z.json"

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        root = json.load(f)
    
    rules = root.get('data', {}).get('rules', [])
    print(f"Loaded {len(rules)} rules.")
    
    # Target description
    target_desc = "Check 3122"
    target_amount = -600
    
    print(f"\n--- Checking rules against '{target_desc}' ---")
    
    matched_rules = []
    
    for i, r in enumerate(rules):
        raw = str(r.get('payee') or r.get('match') or r.get('pattern') or '')
        pattern = raw
        
        # Simple regex simulation for the check
        # (ignoring complex amount logic for a moment, just pattern match)
        
        try:
            # Check if regex
            # In JS code: new RegExp(pattern, 'i')
            # Python re.search is somewhat similar
            if re.search(pattern, target_desc, re.IGNORECASE):
                print(f"Rule {i} MATCHES pattern '{pattern}': {r}")
                matched_rules.append(r)
            elif pattern.lower() in target_desc.lower():
                 print(f"Rule {i} MATCHES substring '{pattern}': {r}")
                 matched_rules.append(r)
        except Exception as e:
            pass

    # Search for "pay the check" in rules
    print(f"\n--- Searching for 'pay the check' in rules ---")
    for i, r in enumerate(rules):
        r_str = str(r)
        if "pay the check" in r_str.lower():
            print(f"Found in Rule {i}: {r}")

except Exception as e:
    print(f"Error: {e}")
