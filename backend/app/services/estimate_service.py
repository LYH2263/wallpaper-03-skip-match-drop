from fastapi import HTTPException

from app.engines.wallpaper_math import MATCH_STRAIGHT, MATCH_TYPES, roll_count
from app.repositories import history, rolls, walls


def run_estimate(wall_id: int, roll_id: int, save: bool, note: str, match: str | None = None):
    wall = walls.get_wall(wall_id)
    if not wall:
        raise HTTPException(404, "wall not found")
    roll = rolls.get_roll(roll_id)
    if not roll:
        raise HTTPException(404, "roll not found")
    if wall.get("data_quality") == "dirty" or roll.get("data_quality") == "dirty":
        raise HTTPException(422, "dirty seed entity")

    # 当次匹配方式：显式传入优先，否则取卷材默认；只影响本次，不改写卷材默认值
    match = match or roll.get("match_type") or MATCH_STRAIGHT
    if match not in MATCH_TYPES:
        raise HTTPException(422, "invalid match type")
    try:
        calc = roll_count(
            wall["perimeter"], wall["height"], roll["width"], roll["length"],
            roll["pattern_cm"], match,
        )
    except ValueError as exc:
        # 跳对且花高为负等非法输入：拒绝测算，不写 run、不增行
        raise HTTPException(422, str(exc))

    run_id = None
    if save:
        # 落库钉住匹配方式、drop_len 与卷数（均在 calc/result_json 内）
        run_id = history.insert_run(wall_id, roll_id, {**calc, "wall_id": wall_id, "roll_id": roll_id}, note)
    return {"wall": wall, "roll": roll, "run_id": run_id, **calc}
