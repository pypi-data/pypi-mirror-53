try:
    import simplejson as json

except ImportError:
    import json


def json_adv_process(arg, name_map):
    if isinstance(arg, list):
        return [json_adv_process(a, name_map) for a in arg]

    elif isinstance(arg, dict):
        return {name_map[k]: json_adv_process(v, name_map) for k, v in arg.items()}

    return arg

def json_names(arg, res):
    if isinstance(arg, list):
        for a in arg:
            json_names(a, res)

    elif isinstance(arg, dict):
        for k, v in arg.items():
            res.add(k)
            json_names(v, res)

letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
letter_combos = list(letters) + [a + b for a in letters for b in letters]

def json_adv_dump(arg):
    names = set()
    json_names(arg, names)
    names = list(names)
    name_map = {n: letter_combos[i] for i, n in enumerate(names)}

    return json.dumps([{letter_combos[i]: n for i, n in enumerate(names)}, json_adv_process(arg, name_map)])

def json_adv_dumpobj(arg):
    names = set()
    json_names(arg, names)
    names = list(names)
    name_map = {n: letter_combos[i] for i, n in enumerate(names)}

    return [{letter_combos[i]: n for i, n in enumerate(names)}, json_adv_process(arg, name_map)]

def json_adv_load(arg):
    name_map, arg = json.loads(arg)
    return json_adv_process(arg, name_map)

def json_adv_loadobj(arg):
    name_map, arg = arg
    return json_adv_process(arg, name_map)