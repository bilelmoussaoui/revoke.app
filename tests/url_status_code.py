import toml
import glob
import os
import requests
import sys

urls = ['devicesURL', 'sessionsURL', 'appsURL']
valid_responses = [200, 401, 403]

absolute_url = os.path.abspath(os.path.join(os.path.realpath(__file__), "..", ".."))
apps = glob.glob(os.path.join(absolute_url, "data/apps/") + "*.toml")
apps.sort()


found_invalid = False

for app_file in apps:
  with open(app_file, 'r') as fd:
    app = toml.load(fd)

    name = app.get('name')
    for attr in urls:
      url = app.get(attr)
      if url:
        message = ""
        status_code = requests.get(url).status_code
        if status_code in valid_responses:
          message += "✔️  "
        else:
          message += "❌ "
          found_invalid = True
        message += f"{name}: {url}"
        print(message)

sys.exit(int(found_invalid))
