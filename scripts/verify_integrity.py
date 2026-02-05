#!/usr/bin/env python3
import os
import sys

def verify_structure():
    required_dirs = ["journals", "archives", "scripts", "references"]
    required_files = ["SKILL.md", "references/Meta-Specification.md"]
    missing = [d for d in required_dirs if not os.path.isdir(d)]
    missing += [f for f in required_files if not os.path.isfile(f)]
    
    if missing:
        print(f"ERROR: Missing components: {', '.join(missing)}")
        return False
    return True

def get_evolution_config():
    try:
        with open("SKILL.md", 'r', encoding='utf-8') as f:
            content = f.read()
        if not content.startswith("---"): return None
        
        header = content.split("---")[1]
        config = {}
        required_keys = ["version", "max_history_size"]
        found_keys = []
        
        for line in header.split("\n"):
            line = line.strip()
            if not line: continue
            if "evolution:" in line: continue
            if ":" in line:
                k, v = line.split(":", 1)
                k = k.strip()
                config[k] = v.strip().strip('"')
                if k in required_keys:
                    found_keys.append(k)
        
        missing = [k for k in required_keys if k not in found_keys]
        if missing:
            print(f"ERROR: Missing metadata: {', '.join(missing)}")
            return None
            
        return config
    except Exception as e:
        print(f"ERROR: Metadata parse failed: {e}")
        return None

if __name__ == "__main__":
    if not os.path.exists("SKILL.md") and os.path.exists("../SKILL.md"): os.chdir("..")
    
    if verify_structure() and get_evolution_config():
        print("SUCCESS: SEAS Integrity Verified.")
        sys.exit(0)
    sys.exit(1)
