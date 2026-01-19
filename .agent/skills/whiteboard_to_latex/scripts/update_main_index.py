#!/usr/bin/env python3
import os
import re

"""
Main Index Updater

Usage:
    python update_main_index.py

Description:
    Ensures all N/NX.tex files are included in MTS.tex via \\input.
    Automatically adds missing files in numerical order.
"""

def update_index():
    n_dir = "N"
    main_file = "MTS.tex"
    
    # 1. Check paths
    if not os.path.exists(n_dir):
        print(f"  ! Directory {n_dir} not found!")
        return
    
    if not os.path.exists(main_file):
        print(f"  ! File {main_file} not found!")
        return

    # 2. Find N files
    files = [f for f in os.listdir(n_dir) if re.match(r'N\d+\.tex', f)]
    files.sort(key=lambda x: int(re.search(r'N(\d+)', x).group(1)))
    
    if not files:
        print(f"  = No N*.tex files found in {n_dir}")
        return

    print(f"> Checking: {len(files)} files in {n_dir}")

    # 3. Read main file
    with open(main_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 4. Find existing inputs
    existing = set(re.findall(r'\\input\{N/(N\d+\.tex)\}', content))
    missing = [f for f in files if f not in existing]
    
    if not missing:
        print("  = All files already included!")
        return

    print(f"  + Missing: {', '.join(missing)}")

    # 5. Find insertion point
    input_pat = re.compile(r'(\\input\{N/N\d+\.tex\}\s*\\newpage)')
    matches = list(input_pat.finditer(content))
    
    if matches:
        insert_pos = matches[-1].end()
    else:
        end_doc = re.search(r'\\end\{document\}', content)
        if end_doc:
            insert_pos = end_doc.start()
        else:
            print("  ! Cannot find insertion point!")
            return

    # 6. Build insertion
    insertion = ""
    if insert_pos > 0 and content[insert_pos - 1] != '\n':
        insertion += "\n"
    
    for f in missing:
        insertion += f"\n\\input{{N/{f}}}\n\\newpage"

    # 7. Write changes
    new_content = content[:insert_pos] + insertion + content[insert_pos:]
    with open(main_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"  + Added {len(missing)} file(s) to {main_file}")

if __name__ == "__main__":
    update_index()
