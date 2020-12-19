import csv
from datetime import datetime, timedelta, timezone
import os
from collections import defaultdict
from models.drink import Drink


def load_daily_drinks(file, drinkers = None):
    # if drinkers is None -> load all drinkers
    ret = defaultdict(lambda: [])
    if not os.path.exists(file):
        return ret

    # TODO: Investigate timezones
    # Not sure if time zone stuff is needed, so it's been ignored
    # tz = datetime.now().astimezone().tzinfo
    # print(tz)
    # cutoff = datetime.now(tz)

    # Generate the cutoff as 6am
    cutoff = datetime.now()
    if cutoff.hour < 6:
        cutoff = datetime.now() - timedelta(days=1)
    cutoff = cutoff.replace(hour=6, minute=0, second=0, microsecond=0)

    print('Cut off is: {}'.format(cutoff))

    with open(path, 'r') as drink_data:
        for row in reversed(list(csv.reader(drink_data))):
            drink = generate_drink_from_data(row)

            if drink is not None and drink.time_of_drink > cutoff:
                if drinkers is None or drink.drinker in drinkers:
                    ret[drink.drinker].append(drink)
            else:
                break

    return ret


def generate_drink_from_data(data):
    f, success = try_parse_float(data[0].strip())
    if not success:
        return None

    d = Drink()
    time = int(f)
    d.time_of_drink = datetime.fromtimestamp(time)
    d.drinker = data[1].strip()
    d.abv, success = try_parse_float(data[2])
    if not success:
        return None

    d.volume_oz, success = try_parse_float(data[3])
    if not success:
        return None

    return d

def try_parse_float(value):
    try:
        return float(value), True
    except ValueError:
        return None, False


def try_parse_string(value):
    try:
        v = str(value).strip(' ').lower()
        if v != '':
            return v, True
        else:
            return None, False
    except ValueError:
        return None, False

if __name__ == "__main__":
    path = os.getcwd() + '//drinks//drink_log.csv'

    drinks = load_daily_drinks(path)
    print(drinks)


