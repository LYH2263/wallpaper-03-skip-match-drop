from typing import Literal, Optional

from pydantic import BaseModel

MatchType = Literal["straight", "offset"]


class EstimateRequest(BaseModel):
    wall_id: int
    roll_id: int
    save: bool = False
    note: str = ""
    # 当次测算的匹配方式；省略时取卷材默认 match_type
    match: Optional[MatchType] = None


class RollMatchRequest(BaseModel):
    match_type: MatchType
