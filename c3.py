import random
import time

def get_vibrator_track(distance, fixv=0):
    distance = distance + 10 + fixv
    vibrator_track = []
    threshold = distance * 3 / 4
    s = 0
    v = 0
    t = 0
    delta_t = 0.2
    while s < distance:
        if s < threshold:
            a = 2
        else:
            a = -3
        v = v + delta_t * a
        delta_s = v * delta_t + 1 / 2 * a * delta_t * delta_t
        vibrator_track.append(round(delta_s))
        s += delta_s
    vibrator_track.extend([-2, -2, -2, -1, -1, -1, -1, -1, -1])
    return vibrator_track

def time_sleep_random():
    time.sleep(1 + random.random())
