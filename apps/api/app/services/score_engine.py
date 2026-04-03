from collections import Counter


def _sentiment_score(sentiment: str) -> float:
    return {"positive": 1.0, "neutral": 0.6, "negative": 0.2}.get(sentiment, 0.6)


def compute_geo_score(analysis_items: list[dict]) -> dict:
    if not analysis_items:
        return {
            "total": 0.0,
            "visibility": 0.0,
            "ranking": 0.0,
            "sentiment": 0.0,
            "accuracy": 0.0,
        }

    total_items = len(analysis_items)
    mentions = sum(1 for item in analysis_items if item.get("brand_mentioned"))
    avg_rank = sum(item.get("brand_rank", 0) for item in analysis_items if item.get("brand_rank", 0) > 0)
    ranked_count = sum(1 for item in analysis_items if item.get("brand_rank", 0) > 0)
    avg_rank = avg_rank / ranked_count if ranked_count else 0
    avg_sentiment = sum(_sentiment_score(item.get("sentiment", "neutral")) for item in analysis_items) / total_items
    avg_accuracy = sum(float(item.get("accuracy_score", 0.7)) for item in analysis_items) / total_items

    visibility = (mentions / total_items) * 100
    ranking = max(0.0, 100 - (avg_rank - 1) * 12) if avg_rank else 0.0
    sentiment = avg_sentiment * 100
    accuracy = avg_accuracy * 100
    total = visibility * 0.4 + ranking * 0.3 + sentiment * 0.2 + accuracy * 0.1

    sentiments = Counter(item.get("sentiment", "neutral") for item in analysis_items)
    return {
        "total": round(total, 2),
        "visibility": round(visibility, 2),
        "ranking": round(ranking, 2),
        "sentiment": round(sentiment, 2),
        "accuracy": round(accuracy, 2),
        "sentiment_count": dict(sentiments),
    }

