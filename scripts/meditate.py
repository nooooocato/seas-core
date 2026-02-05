#!/usr/bin/env python3
import os
import sys

def get_journals():
    journals_dir = "journals"
    if not os.path.isdir(journals_dir):
        return []
    
    entries = []
    for entry in os.listdir(journals_dir):
        full_path = os.path.join(journals_dir, entry)
        if os.path.isdir(full_path):
            entries.append(full_path)
    return sorted(entries)

def read_journal_content(journal_path):
    name = os.path.basename(journal_path)
    content = f"--- JOURNAL: {name} ---\n"
    
    case_path = os.path.join(journal_path, "case.md")
    exp_path = os.path.join(journal_path, "experience.md")
    
    if os.path.exists(case_path):
        content += "\n[CASE]\n"
        with open(case_path, 'r', encoding='utf-8') as f:
            content += f.read()
    else:
        content += "\n[CASE MISSING]\n"
        
    if os.path.exists(exp_path):
        content += "\n[EXPERIENCE]\n"
        with open(exp_path, 'r', encoding='utf-8') as f:
            content += f.read()
    else:
        content += "\n[EXPERIENCE MISSING]\n"
        
    content += "\n----------------------------------------\n"
    return content

if __name__ == "__main__":
    # Change to the skill root if needed
    if not os.path.exists("journals") and os.path.exists("../journals"):
        os.chdir("..")

    journals = get_journals()
    
    if not journals:
        print("No journals found.")
        sys.exit(0)
        
    print(f"Found {len(journals)} journals for meditation.\n")
    
    for journal in journals:
        print(read_journal_content(journal))
        
    print("\n[INSTRUCTIONS FOR AGENT]")
    print("1. Analyze the journals above.")
    print("2. Identify recurring errors or successful patterns.")
    print("3. Decide to UPDATE SKILL.md, FIX scripts, or DEFER.")
    print("4. EXECUTE the necessary changes.")
    print("5. VERIFY using 'python3 scripts/verify_integrity.py'.")
    print("6. If successful, ARCHIVE the processed journals.")
