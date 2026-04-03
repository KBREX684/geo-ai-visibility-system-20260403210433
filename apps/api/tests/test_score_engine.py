from app.services.score_engine import compute_geo_score


def test_compute_geo_score_is_deterministic():
    items = [
        {"brand_mentioned": True, "brand_rank": 1, "sentiment": "positive", "accuracy_score": 0.9},
        {"brand_mentioned": False, "brand_rank": 0, "sentiment": "neutral", "accuracy_score": 0.7},
    ]
    first = compute_geo_score(items)
    second = compute_geo_score(items)
    assert first == second
    assert set(["total", "visibility", "ranking", "sentiment", "accuracy"]).issubset(first.keys())

