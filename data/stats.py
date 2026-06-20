import json
import os

PATH = 'data/stats.json'

DEFAULT = {
    'differences': {'high_score': 0, 'games_played': 0},
    'patterns':    {'high_score': 0, 'games_played': 0},
    'sequences':   {'high_score': 0, 'games_played': 0},
}


def load():
    if os.path.exists(PATH):
        with open(PATH) as f:
            return json.load(f)
    return {k: dict(v) for k, v in DEFAULT.items()}


def save(stats):
    os.makedirs('data', exist_ok=True)
    with open(PATH, 'w') as f:
        json.dump(stats, f, indent=2)


def record(stats, mode, score):
    stats[mode]['games_played'] += 1
    if score > stats[mode]['high_score']:
        stats[mode]['high_score'] = score
    save(stats)