from funasr import AutoModel
from funasr.utils.load_utils import load_audio_text_image_video, extract_fbank
import torch


def fix_imbalance(result):
    probs = result.get("emotion_probs", {})
    if not probs:
        return result

    top_emotion = max(probs, key=probs.get)
    top_score = probs[top_emotion]

    if top_emotion == "Neutral" and top_score < 0.70:
        sorted_items = sorted(probs.items(), key=lambda x: x[1], reverse=True)
        if len(sorted_items) > 1:
            result["emotion"] = sorted_items[1][0]

    return result


def run_sensevoice_with_probs(audio_path):
    model, kwargs = AutoModel.build_model(
        model="FunAudioLLM/SenseVoiceSmall",
        trust_remote_code=True,
        device="cpu",
        hub="hf",
        disable_update=True,
    )

    frontend = kwargs["frontend"]
    tokenizer = kwargs["tokenizer"]

    audio_sample_list = load_audio_text_image_video(
        audio_path,
        fs=frontend.fs,
        audio_fs=kwargs.get("fs", 16000),
        data_type="sound",
        tokenizer=tokenizer,
    )

    speech, speech_lengths = extract_fbank(
        audio_sample_list,
        data_type="sound",
        frontend=frontend,
    )

    speech = speech.to(device=kwargs["device"])
    speech_lengths = speech_lengths.to(device=kwargs["device"])

    language = "auto"
    use_itn = True
    textnorm = "withitn" if use_itn else "woitn"

    language_query = model.embed(
        torch.LongTensor([[model.lid_dict[language] if language in model.lid_dict else 0]]).to(speech.device)
    ).repeat(speech.size(0), 1, 1)

    textnorm_query = model.embed(
        torch.LongTensor([[model.textnorm_dict[textnorm]]]).to(speech.device)
    ).repeat(speech.size(0), 1, 1)

    speech = torch.cat((textnorm_query, speech), dim=1)
    speech_lengths += 1

    event_emo_query = model.embed(
        torch.LongTensor([[1, 2]]).to(speech.device)
    ).repeat(speech.size(0), 1, 1)

    input_query = torch.cat((language_query, event_emo_query), dim=1)
    speech = torch.cat((input_query, speech), dim=1)
    speech_lengths += 3

    encoder_out, encoder_out_lens = model.encoder(speech, speech_lengths)
    if isinstance(encoder_out, tuple):
        encoder_out = encoder_out[0]

    rich_logits = model.ctc.ctc_lo(encoder_out[:, :4, :])

    emo_ids = {
        "Happy": model.emo_dict["happy"],
        "Sad": model.emo_dict["sad"],
        "Angry": model.emo_dict["angry"],
        "Neutral": model.emo_dict["neutral"],
    }

    emo_position = 2
    emo_token_ids = [emo_ids["Happy"], emo_ids["Sad"], emo_ids["Angry"], emo_ids["Neutral"]]
    emo_logits = rich_logits[0, emo_position, emo_token_ids]
    emo_probs = torch.softmax(emo_logits, dim=-1)

    emotion_probs = {
        "Happy": float(emo_probs[0]),
        "Sad": float(emo_probs[1]),
        "Angry": float(emo_probs[2]),
        "Neutral": float(emo_probs[3]),
    }

    ctc_logits = model.ctc.log_softmax(encoder_out)
    x = ctc_logits[0, : encoder_out_lens[0].item(), :]
    yseq = x.argmax(dim=-1)
    yseq = torch.unique_consecutive(yseq, dim=-1)
    mask = yseq != model.blank_id
    token_int = yseq[mask].tolist()
    text = tokenizer.decode(token_int)

    top_emotion = max(emotion_probs, key=emotion_probs.get)

    result = {
        "text": text,
        "emotion": top_emotion,
        "emotion_probs": emotion_probs,
    }

    return result


if __name__ == "__main__":
    result = run_sensevoice_with_probs("sample.wav")

    print("=== raw result ===")
    print(result)

    print("=== emotion probability scores ===")
    for emotion, score in result["emotion_probs"].items():
        print(f"{emotion}: {score:.6f}")

    result = fix_imbalance(result)

    print("=== final emotion ===")
    print(result["emotion"])