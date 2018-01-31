import json
import hashlib


def _get_hash_target(action):
    hash_target = {
        "selector": action["target"]["selector"],
        "selectorValue": action["target"]["selectorValue"],
        "state": action["target"]["state"]
    }
    return hash_target


def _get_hash_action(action, hash_target):
    hash_action = {
        "target": hash_target,
        "type": action["type"],
    }
    return hash_action


def generate_state_hash(actions):
    hash_source = []
    for action in actions:
        hash_target = _get_hash_target(action)
        hash_action = _get_hash_action(action, hash_target)
        hash_source.append(hash_action)

    hash_source.sort(key=lambda the_action: the_action["type"] + "@" + the_action["target"]["selector"] + "=" + the_action["target"]["selectorValue"])
    json_hash_source = json.dumps(hash_source, sort_keys=True)
    return hashlib.sha1(json_hash_source.encode("utf-8")).hexdigest()


def generate_test_case_hash(test_case):
    hash_source = []
    for event in test_case:
        pass
