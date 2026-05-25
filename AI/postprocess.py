def decide_emotion(scores: dict) -> str:
    if not scores:
        return "neutral"

    emotion_keys = [
        "angry",
        "disgust",
        "disgusted",
        "fearful",
        "happy",
        "neutral",
        "other",
        "sad",
        "surprised",
        "unknown",
        "<unk>",
    ]

    valid_scores = {
        key: value
        for key, value in scores.items()
        if key in emotion_keys and isinstance(value, (int, float))
    }

    if not valid_scores:
        return "neutral"

    return max(valid_scores, key=valid_scores.get)


def map_emotion(emotion: str) -> str:
    if not emotion:
        return "Neutral"

    emotion = emotion.lower()

    if emotion in ["happy", "surprised"]:
        return "Happy"

    if emotion == "sad":
        return "Sad"

    if emotion in ["angry", "disgust", "disgusted", "fearful"]:
        return "Angry"

    return "Neutral"


def postprocess_emotion(scores: dict) -> str:
    emotion = decide_emotion(scores)
    return map_emotion(emotion)


def fix_imbalance(scores: dict) -> str:
    return postprocess_emotion(scores)