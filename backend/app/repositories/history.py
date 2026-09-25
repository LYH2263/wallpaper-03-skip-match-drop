import json
from datetime import datetime, timezone

from app.db import connect


def insert_run(wall_id: int, roll_id: int, result: dict, note: str = "") -> int:
    conn = connect()
    try:
        cur = conn.execute(
            "INSERT INTO calc_runs(wall_id,roll_id,result_json,note,created_at) VALUES (?,?,?,?,?)",
            (wall_id, roll_id, json.dumps(result, ensure_ascii=False), note, datetime.now(timezone.utc).isoformat()),
        )
        conn.commit()
        return int(cur.lastrowid)
    finally:
        conn.close()


def _hydrate(row) -> dict:
    d = dict(row)
    d["result"] = json.loads(d.pop("result_json"))
    return d


_RUN_SELECT = """
    SELECT r.*, w.name wall_name, rl.name roll_name
    FROM calc_runs r
    LEFT JOIN walls w ON w.id=r.wall_id
    LEFT JOIN rolls rl ON rl.id=r.roll_id
"""


def list_runs(limit: int = 50):
    conn = connect()
    try:
        rows = conn.execute(
            _RUN_SELECT + " ORDER BY r.id DESC LIMIT ?",
            (limit,),
        ).fetchall()
        return [_hydrate(r) for r in rows]
    finally:
        conn.close()


def get_run(run_id: int):
    """按编号回看：返回写入时钉住的结果（含 match/drop_len_m/rolls），不重算。"""
    conn = connect()
    try:
        row = conn.execute(
            _RUN_SELECT + " WHERE r.id=?",
            (run_id,),
        ).fetchone()
        return _hydrate(row) if row else None
    finally:
        conn.close()
