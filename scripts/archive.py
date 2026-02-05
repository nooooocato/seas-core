#!/usr/bin/env python3
import os
import shutil
import zipfile
import datetime

def archive():
    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    if not os.path.exists("journals"): return
    
    # 1. Prepare Staging
    stage = f"temp_archive_{ts}"
    os.makedirs(f"{stage}/journals", exist_ok=True)
    os.makedirs(f"{stage}/pre_evolution_snapshot", exist_ok=True)
    
    # 2. Snapshot current state
    for item in ["SKILL.md", "scripts", "references"]:
        if os.path.isfile(item): shutil.copy(item, f"{stage}/pre_evolution_snapshot/")
        elif os.path.isdir(item): shutil.copytree(item, f"{stage}/pre_evolution_snapshot/{item}")

    # 3. Move Journals
    journals = [d for d in os.listdir("journals") if os.path.isdir(f"journals/{d}")]
    if not journals: 
        shutil.rmtree(stage)
        print("Nothing to archive.")
        return
        
    for j in journals:
        shutil.move(f"journals/{j}", f"{stage}/journals/")
    
    # 4. Zip and Cleanup
    zip_path = f"archives/update-{ts}.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(stage):
            for f in files:
                p = os.path.join(root, f)
                z.write(p, os.path.relpath(p, stage))
                
    # 5. History update
    with open("archives/HISTORY.md", "a") as h:
        h.write(f"\n## [{ts}] Evolution Archival\n- Processed {len(journals)} journals.\n- Snapshot saved in {zip_path}\n")
        
    shutil.rmtree(stage)
    print(f"Archived successfully: {zip_path}")

if __name__ == "__main__":
    if not os.path.exists("journals") and os.path.exists("../journals"): os.chdir("..")
    archive()
