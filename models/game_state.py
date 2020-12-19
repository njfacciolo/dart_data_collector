class Game_State:
    def __init__(self, player_count, to_close):
        self.to_close = to_close
        self.player_count = player_count
        self.states = []
        self._reset_game()

    def set_player_names(self, names):
        for name, state in zip(names, self.states):
            state.player_name = name

    def _reset_game(self):
        self.states = []
        for player in range(self.player_count):
            self.states.append(Game_Score(self.to_close))


    def update_state(self, throw):
        assert throw.thrower < len(self.states)

        state = self.states[throw.thrower]
        remainder = state.add_throw(throw)

        # check if the remainder gets added to the score or is ignored
        if remainder > 0:
            for i in range(len(self.states)):
                if i == throw.thrower:
                    continue
                s = self.states[i]
                if s.is_closed(throw.point_value):
                    return self._get_image_id(state, throw.point_value)

        state.score += remainder
        return self._get_image_id(state, throw.point_value)

    def _get_image_id(self, score, point_value):
        key = 'b' if point_value == 25 else str(point_value)
        hits = score.status[key]

        if sum(hits) < 3:
            return str(sum(hits))

        tsum = 0
        for i in range(len(hits)):
            tsum += hits[i]
            if tsum >= 3 and i == 0:
                return '3_1'
            if i > 1:
                break
            if tsum >= 3 and hits[0] == 1:
                return '3_2'

        return '3_3'

class Game_Score:
    def __init__(self, to_close):
        self.player_name = ""
        self.to_close = to_close
        self.score = 0
        self.status = {}
        for i in range(1,21,1):
            self.status[str(i)] = []
        self.status['b'] = []

    def add_throw(self, throw):
        # add to score, return remainder of points that could go to final score

        val, mult = throw.point_value, throw.multiplier
        key = 'b' if val == 25 else str(val)

        assert key in self.status

        remaining_hits = max(0, mult - max(0, (self.to_close - sum(self.status[key]))))
        self.status[key].append(mult)

        return remaining_hits * val

    def is_closed(self, value):
        key = 'b' if value == 25 else str(value)

        assert key in self.status
        return sum(self.status[key]) >= 3










