def decide_emotion(scores: dict) -> str:
    if not scores:
        return "neutral"
    return max(scores, key=scores.get)


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