#!/usr/bin/env python3
import os
import shutil
import zipfile
import datetime

def archive():
    # Get skill root directory (parent of scripts/)
    skill_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(skill_root)
    
    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    journals_dir = "journals"
    
    if not os.path.exists(journals_dir):
        print("No journals directory found.")
        return
    
    # 1. Prepare Staging
    stage = f"temp_archive_{ts}"
    os.makedirs(f"{stage}/journals", exist_ok=True)
    os.makedirs(f"{stage}/pre_evolution_snapshot", exist_ok=True)
    
    # 2. Snapshot current state
    for item in ["SKILL.md", "scripts", "references"]:
        if os.path.isfile(item): 
            shutil.copy(item, f"{stage}/pre_evolution_snapshot/")
        elif os.path.isdir(item): 
            shutil.copytree(item, f"{stage}/pre_evolution_snapshot/{item}", dirs_exist_ok=True)

    # 3. Move Journals
    journals = [d for d in os.listdir(journals_dir) if os.path.isdir(os.path.join(journals_dir, d))]
    if not journals: 
        shutil.rmtree(stage)
        print("Nothing to archive.")
        return
        
    for j in journals:
        shutil.move(os.path.join(journals_dir, j), os.path.join(stage, "journals/"))
    
    # 4. Zip and Cleanup
    archives_dir = "archives"
    os.makedirs(archives_dir, exist_ok=True)
    zip_path = os.path.join(archives_dir, f"update-{ts}.zip")
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(stage):
            for f in files:
                p = os.path.join(root, f)
                z.write(p, os.path.relpath(p, stage))
                
    # 5. History update
    history_file = os.path.join(archives_dir, "HISTORY.md")
    with open(history_file, "a") as h:
        h.write(f"\n## [{ts}] Evolution Archival\n")
        h.write(f"- **Action:** Automatic archival after evolution.\n")
        h.write(f"- **Processed:** {len(journals)} journals ({', '.join(journals)}).\n")
        h.write(f"- **Snapshot:** {os.path.basename(zip_path)}\n")
        
    shutil.rmtree(stage)
    print(f"Archived successfully: {zip_path}")

if __name__ == "__main__":
    archive()
