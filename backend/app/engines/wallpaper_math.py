"""Wallpaper rolls: perimeter strips, pattern repeat on drop length, strips per roll.

匹配方式 match:
- straight（直对）: drop_len = 层高 + 花高，与改造前同参一致
- offset（跳对）: 在层高基础上再加半个花高（半花高向上取到毫米后换算）
花高为 0 时两种方式结果相同；跳对且花高为负时拒绝测算。
"""

from app.engines.helpers import ceil_units, floor_units

MATCH_STRAIGHT = "straight"
MATCH_OFFSET = "offset"
MATCH_TYPES = (MATCH_STRAIGHT, MATCH_OFFSET)

_MM = 0.001


def roll_count(
    perimeter: float,
    height: float,
    roll_width: float,
    roll_length: float,
    pattern_cm: float,
    match: str = MATCH_STRAIGHT,
) -> dict:
    if roll_width <= 0 or roll_length <= 0:
        raise ValueError("invalid roll size")
    if match not in MATCH_TYPES:
        raise ValueError("invalid match type")
    pattern_raw = float(pattern_cm) / 100.0
    if match == MATCH_OFFSET and pattern_raw < 0:
        raise ValueError("negative pattern repeat")
    pattern_m = max(0.0, pattern_raw)
    if match == MATCH_OFFSET:
        # 半个花高，向上取到毫米（0.001m）后换算
        extra_m = ceil_units(pattern_m / 2.0 / _MM) * _MM
    else:
        extra_m = pattern_m
    drop_len = float(height) + extra_m
    if drop_len <= 0:
        raise ValueError("invalid drop length")
    drops = ceil_units(float(perimeter) / float(roll_width))
    strips_per_roll = max(1, floor_units(float(roll_length) / drop_len))
    rolls = ceil_units(drops / strips_per_roll)
    return {
        "drops": drops,
        "drop_len_m": round(drop_len, 3),
        "pattern_m": round(pattern_m, 3),
        "match": match,
        "strips_per_roll": strips_per_roll,
        "rolls": rolls,
    }
