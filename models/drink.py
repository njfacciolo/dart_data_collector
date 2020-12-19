class Drink():
    def __init__(self):
        self.time_of_drink = 0
        self.drinker = ''
        self.abv = 0
        self.volume_oz = 0

    def get_alcohol_units(self):
        # 1 unit = 5% * 12 oz
        # 1 unit = 5% * 12oz
        # 1 unit = 0.6oz @ 100%

        return (self.volume_oz * (self.abv / 100.0)) / 0.6