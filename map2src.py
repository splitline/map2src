import os
import os.path
import errno
import sys
import requests
import json

if len(sys.argv) < 2 or len(sys.argv) > 3:
    print("Usage: python map2src.py url [output_dir]")
    sys.exit()

url = sys.argv[1]
output_dir = sys.argv[2] if len(sys.argv) == 3 else "./"

if not os.path.exists(output_dir):
    os.mkdir(output_dir)
if not os.path.isdir(output_dir):
    print("Error: File `{}` exists, but not a directory".format(output_dir))
    sys.exit()

map_file = json.loads(requests.get(url).text)

for i, src_name in enumerate(map_file['sources']):
    src_name = src_name.replace("webpack:///", "")
    src_name = os.path.join(output_dir, src_name)
    try:
        os.makedirs(os.path.dirname(src_name))
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(os.path.dirname(src_name)):
            pass
        else:
            raise
    print("[+]", src_name)
    src = open(src_name, 'w')
    src.write(map_file['sourcesContent'][i])
    src.close()

map_filename = os.path.join(output_dir, os.path.basename(url))
print("[+]", map_filename)
json.dump(map_file, open(map_filename, "w"))

print("Done.")