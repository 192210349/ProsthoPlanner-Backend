import os
import xml.etree.ElementTree as ET

layout_dir = r"C:\Users\chait\AndroidStudioProjects\ProsthoPlanner\app\src\main\res\layout"

def check_xml(file_path):
    try:
        ET.parse(file_path)
        return True, None
    except ET.ParseError as e:
        return False, str(e)

files = [f for f in os.listdir(layout_dir) if f.endswith(".xml")]
errors = []

for f in files:
    path = os.path.join(layout_dir, f)
    is_valid, error = check_xml(path)
    if not is_valid:
        errors.append(f"{f}: {error}")

if errors:
    print("\n".join(errors))
else:
    print("All XML files are valid.")
