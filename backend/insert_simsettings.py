import yaml
import json
import subprocess

"""
Inserts dummy simulation settings into the mongodb by sending a POST request to the specified URL with the placeholder settings.

Returns:
    None
"""

with open("placeholder_simsettings.yml", "r") as f:
    placeholder = yaml.safe_load(f)

placeholder_str = str(placeholder)
placeholder_str = placeholder_str.replace("'", '"')
placeholder_str = placeholder_str.replace("True", "true")
placeholder_str = placeholder_str.replace("False", "false")
print(placeholder_str)
placeholder_dict = json.loads(placeholder_str)
# placeholder_str = '"' + placeholder_str + '"'

# print(placeholder_str)
# subprocess.run(
#     [
#         "curl",
#         "-X",
#         "GET",
#         "http://127.0.0.1:8000/simulations",
#     ]
# )
subprocess.run(
    [
        "curl",
        "-X",
        "POST",
        "http://127.0.0.1:8080/simsettings",
        "-H",
        "accept: application/json",
        "-H",
        "Content-Type: application/json",
        "-d",
        json.dumps(placeholder_dict),
    ]
)
#!curl -X POST "http://127.0.0.1:8000/simsettings" -H  "accept: application/json" -H  "Content-Type: application/json" -d  "$placeholder_str"
