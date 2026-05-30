def map_emotion(scores: dict) -> str:
    if not scores:
        return "Neutral"

    emotion_keys = [
        "angry",
        "disgusted",
        "fearful",
        "happy",
        "neutral",
        "other",
        "sad",
        "surprised",
        "<unk>",
    ]

    valid_scores = {
        key: value
        for key, value in scores.items()
        if key in emotion_keys and isinstance(value, (int, float))
    }

    if not valid_scores:
        return "Neutral"

    top_emotion = max(valid_scores, key=valid_scores.get)

    if top_emotion == "happy":
        return "Happy"

    if top_emotion == "sad":
        return "Sad"

    if top_emotion == "angry":
        return "Angry"

    return "Neutral"


def postprocess_emotion(scores: dict) -> str:
    return map_emotion(scores)


def fix_imbalance(scores: dict) -> str:
    return map_emotion(scores)