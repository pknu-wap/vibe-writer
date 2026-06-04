import os
import sys
import whisper
from pydub import AudioSegment
from funasr import AutoModel
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from postprocess import fix_imbalance

# 모델은 import 시 1회만 로드
_model_whisper = whisper.load_model("medium")
_model_emo = AutoModel(model="iic/emotion2vec_plus_base", hub="hf")


def analyze_stt(audio_path):
    final_result = []
    video = audio_path

    result = _model_whisper.transcribe(video, word_timestamps=True)

    video_sub = []
    for i in result["segments"]:
        video_sub.append({
            "start": i["start"],
            "end": i["end"],
            "text": i["text"],
            "angry": 0.0, "disgusted": 0.0, "fearful": 0.0,
            "happy": 0.0, "neutral": 0.0, "other": 0.0,
            "sad": 0.0, "surprised": 0.0, "<unk>": 0.0,
        })

    for i in range(len(video_sub)):
        raw_sound = AudioSegment.from_file(video)
        start_t = video_sub[i]["start"] * 1000
        end_t = video_sub[i]["end"] * 1000 + 1000
        sound = raw_sound[start_t:end_t]
        sound = sound.set_frame_rate(16000).set_channels(1)

        samples = np.array(sound.get_array_of_samples()).astype("float32")
        samples = samples / 32768.0

        rec_result = _model_emo.generate(
            samples,
            granularity="utterance",
            extract_embedding=False,
        )

        scores = rec_result[0]["scores"]
        video_sub[i]["angry"] = scores[0]
        video_sub[i]["disgusted"] = scores[1]
        video_sub[i]["fearful"] = scores[2]
        video_sub[i]["happy"] = scores[3]
        video_sub[i]["neutral"] = scores[4]
        video_sub[i]["other"] = scores[5]
        video_sub[i]["sad"] = scores[6]
        video_sub[i]["surprised"] = scores[7]
        video_sub[i]["<unk>"] = scores[8]

    # ⭐ 각 segment마다 자기 점수로 emotion 계산
    for sub in video_sub:
        sub_scores = {
            "angry": float(sub["angry"]),
            "disgusted": float(sub["disgusted"]),
            "fearful": float(sub["fearful"]),
            "happy": float(sub["happy"]),
            "neutral": float(sub["neutral"]),
            "other": float(sub["other"]),
            "sad": float(sub["sad"]),
            "surprised": float(sub["surprised"]),
            "<unk>": float(sub["<unk>"]),
        }
        final_result.append({
            "start": float(sub["start"]),       # np.float64 → float
            "end": float(sub["end"]),
            "text": sub["text"].lstrip(),       # 맨 앞 공백 제거
            "emotion": fix_imbalance(sub_scores),
        })

    return final_result