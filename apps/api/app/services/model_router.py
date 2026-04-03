from app.core.config import get_settings


def pick_model(task_type: str) -> str:
    settings = get_settings()
    strategy = {
        "analysis": settings.model_fallback,
        "content_generation": settings.model_default,
        "diagnostic": settings.model_default,
    }
    return strategy.get(task_type, settings.model_default)

