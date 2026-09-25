from app.db import connect

MATCH_TYPES = ("straight", "offset")


def list_rolls():
    conn = connect()
    try:
        return [dict(r) for r in conn.execute("SELECT * FROM rolls ORDER BY id").fetchall()]
    finally:
        conn.close()


def get_roll(rid: int):
    conn = connect()
    try:
        row = conn.execute("SELECT * FROM rolls WHERE id=?", (rid,)).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def set_match_type(rid: int, match_type: str):
    """只改卷材默认匹配方式，不影响任何已落库的 run。"""
    conn = connect()
    try:
        cur = conn.execute("UPDATE rolls SET match_type=? WHERE id=?", (match_type, rid))
        conn.commit()
        return cur.rowcount > 0
    finally:
        conn.close()
