def map_emotion(emotion: str) -> str:
    emotion = emotion.lower()

    if emotion in ["happy", "surprised"]:
        return "Happy"
    elif emotion == "sad":
        return "Sad"
    elif emotion in ["angry", "disgust", "disgusted", "fearful"]:
        return "Angry"
    elif emotion in ["neutral", "other", "unknown"]:
        return "Neutral"
    else:
        return "Neutral"


def fix_imbalance(scores: dict) -> str:
    if not scores:
        return "Neutral"

    if scores.get("neutral", 0.0) >= 0.70:
        return "Neutral"

    top_emotion = max(scores, key=scores.get)
    return map_emotion(top_emotion)


def apply_final_emotion(results: list) -> list:
    emotion_keys = [
        "angry",
        "disgust",
        "fearful",
        "happy",
        "neutral",
        "other",
        "sad",
        "surprised",
        "unknown",
    ]

    processed_results = []

    for item in results:
        scores = {key: item.get(key, 0.0) for key in emotion_keys}
        final_emotion = fix_imbalance(scores)

        processed_item = item.copy()
        processed_item["final_emotion"] = final_emotion

        processed_results.append(processed_item)

    return processed_results


if __name__ == "__main__":
    sungjae_results = [
        {
            "start": 0.0,
            "end": 3.0,
            "text": "안녕하세요",
            "angry": 0.1,
            "disgust": 0.2,
            "fearful": 0.3,
            "happy": 0.4,
            "neutral": 0.5,
            "other": 0.6,
            "sad": 0.7,
            "surprised": 0.8,
            "unknown": 0.9,
        },
        {
            "start": 3.0,
            "end": 6.0,
            "text": "반갑습니다",
            "angry": 0.1,
            "disgust": 0.2,
            "fearful": 0.3,
            "happy": 0.4,
            "neutral": 0.8,
            "other": 0.1,
            "sad": 0.2,
            "surprised": 0.3,
            "unknown": 0.1,
        },
        {
            "start": 6.0,
            "end": 9.0,
            "text": "화가 납니다",
            "angry": 0.75,
            "disgust": 0.1,
            "fearful": 0.05,
            "happy": 0.02,
            "neutral": 0.1,
            "other": 0.01,
            "sad": 0.03,
            "surprised": 0.04,
            "unknown": 0.02,
        },
        {
            "start": 9.0,
            "end": 12.0,
            "text": "기분이 좋습니다",
            "angry": 0.02,
            "disgust": 0.01,
            "fearful": 0.03,
            "happy": 0.65,
            "neutral": 0.2,
            "other": 0.05,
            "sad": 0.04,
            "surprised": 0.7,
            "unknown": 0.01,
        },
    ]

    result = apply_final_emotion(sungjae_results)

    print("=== integration test result ===")
    for item in result:
        print(
            {
                "start": item["start"],
                "end": item["end"],
                "text": item["text"],
                "final_emotion": item["final_emotion"],
            }
        )

    print("\n=== mapping table ===")
    mapping_table = {
        "happy": "Happy",
        "surprised": "Happy",
        "sad": "Sad",
        "angry": "Angry",
        "disgust": "Angry",
        "disgusted": "Angry",
        "fearful": "Angry",
        "neutral": "Neutral",
        "other": "Neutral",
        "unknown": "Neutral",
    }

    for emotion, mapped_emotion in mapping_table.items():
        print(f"{emotion} -> {mapped_emotion}")