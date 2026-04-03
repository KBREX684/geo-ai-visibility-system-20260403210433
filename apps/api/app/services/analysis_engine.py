from datetime import datetime, timezone


def detect_brand_rank(response_text: str, brand_name: str) -> int:
    lines = [line.strip() for line in response_text.splitlines() if line.strip()]
    for idx, line in enumerate(lines, start=1):
        if brand_name.lower() in line.lower():
            return idx
    return 0


def detect_sentiment(response_text: str, brand_name: str) -> str:
    text = response_text.lower()
    if brand_name.lower() not in text:
        return "neutral"
    positive_keywords = ["推荐", "靠谱", "优秀", "口碑", "好评", "专业"]
    negative_keywords = ["差", "投诉", "不推荐", "坑", "负面"]
    if any(word in text for word in positive_keywords):
        return "positive"
    if any(word in text for word in negative_keywords):
        return "negative"
    return "neutral"


def build_evidence_item(platform: str, prompt_text: str, response_text: str) -> dict:
    excerpt = response_text[:200]
    return {
        "platform": platform,
        "prompt": prompt_text,
        "excerpt": excerpt,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

