import pytest

from app.engines.wallpaper_math import MATCH_OFFSET, MATCH_STRAIGHT, roll_count


def test_plain_master_bed():
    r = roll_count(16.0, 2.7, 0.53, 10.0, 0)
    assert r["drops"] == 31
    assert r["drop_len_m"] == 2.7
    assert r["strips_per_roll"] == 3
    assert r["rolls"] == 11


def test_pattern_wall_straight():
    r = roll_count(20.0, 2.8, 0.53, 10.0, 64, MATCH_STRAIGHT)
    assert r["drops"] == 38
    assert r["drop_len_m"] == 3.44
    assert r["strips_per_roll"] == 2
    assert r["rolls"] == 19
    assert r["match"] == "straight"


def test_straight_default_matches_legacy_args():
    # 直对：显式传参与改造前同参结果一致
    assert roll_count(20.0, 2.8, 0.53, 10.0, 64) == roll_count(
        20.0, 2.8, 0.53, 10.0, 64, MATCH_STRAIGHT
    )


def test_offset_half_pattern_rounds_up_to_mm():
    # 半花高 = 0.64/2 = 0.32m，已整毫米；drop_len = 2.8 + 0.32 = 3.12
    r = roll_count(20.0, 2.8, 0.53, 10.0, 64, MATCH_OFFSET)
    assert r["drop_len_m"] == 3.12
    assert r["strips_per_roll"] == 3   # floor(10/3.12)=3
    assert r["rolls"] == 13            # ceil(38/3)
    assert r["match"] == "offset"


def test_offset_half_pattern_rounds_up_when_odd_mm():
    # 花高 0.645m -> 半花高 0.3225m -> 向上取到毫米 0.323m -> drop_len 3.123
    r = roll_count(20.0, 2.8, 0.53, 10.0, 64.5, MATCH_OFFSET)
    assert r["drop_len_m"] == 3.123


def test_zero_pattern_same_for_both_matches():
    s = roll_count(16.0, 2.7, 0.53, 10.0, 0, MATCH_STRAIGHT)
    o = roll_count(16.0, 2.7, 0.53, 10.0, 0, MATCH_OFFSET)
    # 花高为 0：drop_len、条数、卷数完全一致（仅 match 标签不同）
    for k in ("drops", "drop_len_m", "pattern_m", "strips_per_roll", "rolls"):
        assert s[k] == o[k]
    assert o["drop_len_m"] == 2.7


def test_offset_negative_pattern_rejected():
    with pytest.raises(ValueError):
        roll_count(20.0, 2.8, 0.53, 10.0, -64, MATCH_OFFSET)


def test_straight_negative_pattern_treated_as_zero():
    # 直对保持改造前行为：负花高按 0 计
    r = roll_count(20.0, 2.8, 0.53, 10.0, -64, MATCH_STRAIGHT)
    assert r["drop_len_m"] == 2.8
    assert r["pattern_m"] == 0.0
