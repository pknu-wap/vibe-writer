import whisper
from pydub import AudioSegment
from funasr import AutoModel
from funasr.utils.postprocess_utils import rich_transcription_postprocess
import numpy as np

#input은 mp3나 wav 같은 형태로 넣으면 될 듯?
#ouput은 [{start:0.0, end:3.0, text:"안녕하세요", angry:0.1, disgust:0.2, fearful:0.3, happy:0.4, neutral:0.5, other:0.6, sad:0.7, surprised:0.8, unknown:0.9}, {start:3.0, end:6.0, text:"반갑습니다", angry:0.1, disgust:0.2, fearful:0.3, happy:0.4, neutral:0.5, other:0.6, sad:0.7, surprised:0.8, unknown:0.9}] 같은 형태로 나옴
def analyze_stt(audio_path):
    model_emo = AutoModel(
            model="iic/emotion2vec_plus_base",
            hub="hf", )
    model = whisper.load_model("medium")

    video=audio_path #인풋,인자가 될거임
    result = model.transcribe(video, word_timestamps=True)

    video_sub=[]

    #추출한 영상 자막과 타임 스탬프를 딕셔너리로 저장하는 for문임
    for i in result["segments"]:
        video_sub.append({'start':i['start'],
                        'end':i['end'],
                        'text':i['text'],
                        'angry':"",
                        'disgust':"",
                        'fearful':"",
                        'happy':"",
                        'neutral':"",
                        'other':"",
                        'sad':"",
                        'surprised':"",
                        'unknown':""})
#    print(video_sub) 
    #영상을 타임 스탬프를 기준으로 자른 후 직접 emotion2vec 모델에 넣ㅇ서 해당 문장의 감정을 분석하여 video_sub 딕셔너리에 저장하는 for문임.
    for i in range(len(video_sub)):
        raw_sound = AudioSegment.from_file(video)
        start_t,end_t = video_sub[i]['start'] * 1000, video_sub[i]['end'] * 1000+1000
        sound= raw_sound[start_t:end_t]
        sound = sound.set_frame_rate(16000).set_channels(1)

        samples = np.array(sound.get_array_of_samples()).astype("float32")
        samples = samples / 32768.0

        rec_result = model_emo.generate(
            samples,
            granularity="utterance",   
            extract_embedding=False,
        )

        video_sub[i]['angry'] = rec_result[0]['scores'][0]
        video_sub[i]['disgust'] = rec_result[0]['scores'][1]
        video_sub[i]['fearful'] = rec_result[0]['scores'][2]
        video_sub[i]['happy'] = rec_result[0]['scores'][3]
        video_sub[i]['neutral'] = rec_result[0]['scores'][4]
        video_sub[i]['other'] = rec_result[0]['scores'][5]
        video_sub[i]['sad'] = rec_result[0]['scores'][6]
        video_sub[i]['surprised'] = rec_result[0]['scores'][7]
        video_sub[i]['unknown'] = rec_result[0]['scores'][8]

    return video_sub
