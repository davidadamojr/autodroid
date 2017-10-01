import json
import hashlib

def generate_state_id(actions):
    hash_source = []
    for action in actions:
        hash_target = {
            "selector": actions["target"]["selector"],
            "selectorValue": actions["target"]["selectorValue"],
            "state": actions["target"]["state"]
        }
        hash_action = {
            "target": hash_target,
            "type": action["type"],
        }
        hash_source.append(hash_action)

    json_hash_source = json.dumps(hash_source, sort_keys=True)
    return hashlib.sha1(json_hash_source)