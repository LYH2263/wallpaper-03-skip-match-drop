from fastapi import APIRouter, HTTPException
from app.repositories import rolls as repo
from app.schemas.estimate import RollMatchRequest

router = APIRouter()


@router.get("/rolls")
def list_rolls():
    return {"items": repo.list_rolls()}


@router.get("/rolls/{roll_id}")
def get_roll(roll_id: int):
    row = repo.get_roll(roll_id)
    if not row:
        raise HTTPException(404)
    return row


@router.patch("/rolls/{roll_id}")
def update_roll_match(roll_id: int, body: RollMatchRequest):
    """修改卷材默认匹配方式（直对/跳对），不影响任何已落库的 run。"""
    if not repo.get_roll(roll_id):
        raise HTTPException(404)
    repo.set_match_type(roll_id, body.match_type)
    return repo.get_roll(roll_id)
