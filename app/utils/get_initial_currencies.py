import ujson


def get_initial_currencies():
    with open("app/assets/initial_currencies.json", "r") as json_file:
        data = ujson.load(json_file)

    return data
