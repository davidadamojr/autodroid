import json
import hashlib


def generate_state_id(actions):
    hash_source = []
    for action in actions:
        hash_target = {
            "selector": action["target"]["selector"],
            "selectorValue": action["target"]["selectorValue"],
            "state": action["target"]["state"]
        }
        hash_action = {
            "target": hash_target,
            "type": action["type"],
        }
        hash_source.append(hash_action)

    hash_source.sort(key=lambda the_action: the_action["type"] + "@" + the_action["target"]["selector"] + "=" + the_action["target"]["selectorValue"])
    json_hash_source = json.dumps(hash_source, sort_keys=True)
    return hashlib.sha1(json_hash_source.encode("utf-8")).hexdigest()