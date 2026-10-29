import secrets
import json

keys = {
    "API-key01": secrets.token_hex(16),
    "API-key02": secrets.token_hex(16),
    "API-key03": secrets.token_hex(16),
}

file = open("keys.json", "w")
json.dump(keys, file)
file.close()

for name in keys:
    print(name, keys[name])
