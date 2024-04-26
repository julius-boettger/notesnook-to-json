import sys, os, shutil, pathlib, json

if len(sys.argv) != 3:
    print("Error: Expected exactly two arguments (input file and output file).")
    exit(1)

INPUT_PATH = sys.argv[1]
OUTPUT_PATH = sys.argv[2]

EXTRACT_PATH = "extracted"
if os.path.exists(EXTRACT_PATH):
    print(f"Error: There can't be a file or directory called \"{EXTRACT_PATH}\" in the current directory. Please rename or remove it.")
    exit(1)

shutil.unpack_archive(INPUT_PATH, EXTRACT_PATH)

def extract_title(filecontent: str) -> str:
    return filecontent.split("\n", 1)[0]

def extract_content(filecontent: str) -> str:
    delimiter = "----------"
    start = filecontent.index(delimiter)
    end = filecontent.rindex(delimiter)
    return filecontent[(start + len(delimiter)) : end].strip()

notes = []
for file in pathlib.Path(EXTRACT_PATH).iterdir():
    filecontent = file.read_text()
    notes.append({
        "title": extract_title(filecontent),
        "content": extract_content(filecontent)
    })

shutil.rmtree(EXTRACT_PATH)

output = open(OUTPUT_PATH, "w")
output.write(json.dumps(notes, indent=4))
output.close()