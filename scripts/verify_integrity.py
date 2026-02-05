#!/usr/bin/env python3
import os
import sys

def verify_structure():
    required_dirs = ["journals", "archives", "scripts", "references"]
    required_files = ["SKILL.md", "references/SPECIFICATION.md"]
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
        for line in header.split("\n"):
            if "evolution:" in line: continue
            if line.startswith("  ") and ":" in line:
                k, v = line.split(":", 1)
                config[k.strip()] = v.strip().strip('"')
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
