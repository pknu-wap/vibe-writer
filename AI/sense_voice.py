from funasr import AutoModel
from funasr.utils.postprocess_utils import rich_transcription_postprocess
import torchaudio
import torchaudio.transforms as T

def analyze(audio_path):
    #딕셔너리를 반환값으로 할 예정(아마도?)
    return 