import json, requests, os

from functools import wraps
from time import time

def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print('func:%r args:[%r, %r] took: %2.4f sec' % \
          (f.__name__, args, kw, te-ts))
        return result
    return wrap

def scrape_files(input_file_name: str, output_dir: str):
    with open(input_file_name, "r") as f:
        data = json.load(f)

    for x, message in enumerate(data):
        if message["attachments"]:
            for i, url in enumerate(message["attachments"]):
                print(f"Downloading image #{i + 1} in message #{x + 1}")

                with open(f"{output_dir}/{message["message_id"]}.{i}.{url.split("?", 1)[0].rsplit(".", 1)[1]}", "wb") as f:
                    f.write(requests.get(url).content)

@timing
def process_scaped(dl_dir: str):
    empty = []

    for file in os.listdir(dl_dir):
        path = f"{dl_dir}/{file}"
        if os.path.getsize(path) == 36:
            with open(path, "rb") as f:
                if f.read() == b"This content is no longer available.":
                    print(f"{path} is not available")

                    f.close()

                    empty.append(file)
                    os.remove(path)
    
    with open(f"{dl_dir}/empty.json", "w") as f:
        json.dump(empty, f)