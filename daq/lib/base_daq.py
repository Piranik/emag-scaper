# ar trebui sa fie o clasa care isi face autoschedule cand sa ia date, iar functia de date ar fi implementata
# separat in fiecare clasa extinsa
import random

LOWER_BOUND = 60
HIGH_BOUND = 120

class BaseDaq(object):
    '''Base data data acquisition'''

    def __init__(self):
        self._history = []

    def _generate_new_time(self):
        ok = False
        new_time = None
        while not ok:
            new_time = random.randint(LOWER_BOUND, HIGH_BOUND)
            ok = new_time not in self._history
        self._history.append(new_time)
        self._history = self._history[-3:]

    def _schedule_next_acquisition(self):
        if self._history:
            