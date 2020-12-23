import csv
from datetime import datetime, timedelta, timezone
import os
from collections import defaultdict
from models.drink import Drink
from gui.configuration import METABOLIC_RATE, ABSORPTION_RATE
import random
from data.parse_util import try_parse_float


def load_daily_drinks(file, time=datetime.now(), drinkers = None):
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
    cutoff = time
    if cutoff.hour < 6:
        cutoff = datetime.now() - timedelta(days=1)
    cutoff = cutoff.replace(hour=6, minute=0, second=0, microsecond=0)

    # print('Cut off is: {}'.format(cutoff))

    with open(file, 'r') as drink_data:
        for row in reversed(list(csv.reader(drink_data))):
            drink = generate_drink_from_data(row)

            if drink is not None and drink.time_of_drink > cutoff:
                if drinkers is None or drink.drinker in drinkers:
                    ret[drink.drinker].append(drink)
            else:
                break

    return ret

def calculate_bac_curve(drinks):
    drinks.sort(key= lambda x: x.time_of_drink)
    bac_curve = []
    if drinks is None or len(drinks) < 1:
        return []

    current_backlog = 0

    time = drinks[0].time_of_drink


    #Start sober
    t1 = time - timedelta(minutes=1)
    bac_curve.append((t1, 0.0))

    step_minutes = 3
    removed_per_step = METABOLIC_RATE * (step_minutes/60)
    added_per_step = (1/ABSORPTION_RATE) * (step_minutes/60)

    drank_index = 0
    while time < drinks[-1].time_of_drink + timedelta(hours=2):
        num_drinks = bac_curve[-1][1]

        # add to backlog to metabolize
        while drank_index < len(drinks) and drinks[drank_index].time_of_drink < time:
            current_backlog += drinks[drank_index].get_alcohol_units()
            drank_index += 1

        # Absorb alcohol
        change = min(added_per_step, current_backlog)
        num_drinks += change
        current_backlog -= change

        # Metabolize alcohol
        num_drinks = max(0, num_drinks - removed_per_step)
        bac_curve.append((time, num_drinks))

        time += timedelta(minutes=step_minutes)

        # Debugging
        # print(num_drinks)

    return bac_curve

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



def generate_dummy_drink_data(drinker_name = 'n', start_time=None):
    dummy_drinks = []

    if start_time is None:
        t = datetime.now().replace(hour=12)
    else:
        t = start_time

    for i in range(10):

        d = Drink()
        d.time_of_drink = t
        d.drinker=drinker_name
        d.volume_oz=12.0+ (random.randint(0,1)*4.0)
        d.abv=5.0 + (random.random()*5.5) - 1.0
        dummy_drinks.append(d)
        minute_delta = (random.random() * 20) + 30
        t = t + timedelta(minutes=minute_delta)
    return calculate_bac_curve(dummy_drinks)


if __name__ == "__main__":
    path = os.getcwd() + '//drinks//drink_log.csv'

    # drink_dic = load_daily_drinks(path)
    dummy_curve = generate_dummy_drink_data()


