import toml
import glob
import os
import sys
import re

absolute_url = os.path.abspath(os.path.join(os.path.realpath(__file__), "..", ".."))
apps = glob.glob(os.path.join(absolute_url, "data/apps/") + "*.toml")
apps.sort()

def get_hex_code(color):
    # Source https://github.com/Peter-Slump/python-contrast-ratio
    result = re.match(r'^#?([a-f0-9]{3,3}|[a-f0-9]{6,6})$', color)

    if result is None:
        raise Exception('Could not extract color')

    result = list(result.group(1))

    if len(result) == 6:
        result = [result[i] + result[i+1] for i in range(0, len(result), 2)]
    else:
        result = [result[i] + result[i] for i in range(0, len(result))]

    return [int(hex_code, 16) for hex_code in result]


def calculate_luminace(color_code):
    index = float(color_code) / 255

    if index < 0.03928:
        return index / 12.92
    else:
        return ( ( index + 0.055 ) / 1.055 ) ** 2.4

def get_luminance(color):
    rgb = get_hex_code(color.lower())
    return 0.2126 * calculate_luminace(rgb[0]) + 0.7152 * calculate_luminace(rgb[1]) + 0.0722 * calculate_luminace(rgb[2])

def calc_contrast(bg, fg):
  fg_luminance = get_luminance(fg)
  bg_luminance = get_luminance(bg)

  return (max((bg_luminance, fg_luminance) )+ 0.05) / (min((bg_luminance, fg_luminance))+ 0.05)


found_invalid = False

for app_file in apps:
  with open(app_file, 'r') as fd:
    app = toml.load(fd)

    name = app.get('name')
    bg = app.get("backgroundColor", "#000")
    fg = app.get("foregroundColor", "#FFF")

    message = ""
    contrast = round(calc_contrast(bg, fg), 2)
    if contrast >= 3:
      message += "✔️  "
    else:
      message += "❌ "
      found_invalid = True
    message += f"{name}: bg/fg {bg}/{fg} = {contrast}/21"
    print(message)

sys.exit(int(found_invalid))
