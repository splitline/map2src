#!/usr/bin/env python3

import os
import errno
import sys
import requests
from urllib.parse import urlparse
import json

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: ./map2src.py http://url/to/bundle.js.map output_dir")
        sys.exit()

    url = sys.argv[1]
    output_dir = sys.argv[2]

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    if not os.path.isdir(output_dir):
        print("[-] Error: File `{}` exists, but not a directory".format(output_dir))
        sys.exit()

    if url.startswith('http://') or url.startswith('https://'):
        json_str = requests.get(url, verify=False).text
    else:
        json_str = open(url).read()

    print("[*] Source map loaded.")

    map_file = json.loads(json_str)

    if len(map_file['sourcesContent']) != len(map_file['sources']):
        print("[*] Warning: Length of `sources` and `sourcesContent` doesn't match")

    for i, orig_src_path in enumerate(map_file['sources']):
        orig_src_path = os.path.abspath(urlparse(orig_src_path).path).lstrip("/")
        src_path = os.path.join(output_dir, orig_src_path)

        if os.path.exists(src_path):
            print(f"[*] {src_path} exists, skipped.")
            continue

        try:
            os.makedirs(os.path.dirname(src_path))
        except OSError as err:
            if err.errno == errno.EEXIST and os.path.isdir(os.path.dirname(src_path)):
                pass
            else:
                raise err
        print("[+] Saveing", src_path)

        try:
            src = open(src_path, 'w')
            src.write(map_file['sourcesContent'][i])
            src.close()
        except:
            print("[-] Failed:", src_path)

    map_filename = os.path.join(output_dir, os.path.basename(url))
    print("[+]", map_filename)
    json.dump(map_file, open(map_filename, "w"))

    print("Done.")
