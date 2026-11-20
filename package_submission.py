"""Package the Lab 02 submission into clean .ZIP archives matching the required format.
"""

import os
import zipfile

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ZIP_NAMES = [
    "NoSQL_Lab_02_M_Gouthami_24BTRCL130.zip",
    "NoSQL_Lab_2_Submission.zip"
]

folders_to_include = [
    "Activity_2.1",
    "Activity_2.1_Try_It_Yourself",
    "Activity_2.2",
    "Activity_2.2_Try_It_Yourself",
    "config",
    "screenshots"
]

files_to_include = [
    "NoSQL_Lab_02_Report.docx"
]

for zip_name in ZIP_NAMES:
    zip_path = os.path.join(BASE_DIR, zip_name)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        # Add activity folders and supporting assets
        for folder in folders_to_include:
            folder_full = os.path.join(BASE_DIR, folder)
            if os.path.exists(folder_full):
                for root, dirs, files in os.walk(folder_full):
                    for file in files:
                        full_path = os.path.join(root, file)
                        rel_path = os.path.relpath(full_path, BASE_DIR)
                        zf.write(full_path, rel_path)

        # Add DOCX report
        for f in files_to_include:
            f_full = os.path.join(BASE_DIR, f)
            if os.path.exists(f_full):
                zf.write(f_full, f)

    print(f"[OK] Created {zip_path} ({os.path.getsize(zip_path):,} bytes)")

print("\nVerification of ZIP contents:")
with zipfile.ZipFile(os.path.join(BASE_DIR, ZIP_NAMES[0]), "r") as zf:
    for info in zf.infolist():
        print(f"  {info.filename:60} ({info.file_size:,} bytes)")
