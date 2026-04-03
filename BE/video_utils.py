from moviepy import VideoFileClip
import os

def extract_audio(video_path):
    video = VideoFileClip(video_path)
    audio = video.audio
    
    base = os.path.splitext(video_path)[0]
    audio_path = base + ".wav"
    
    audio.write_audiofile(audio_path)
    video.close()
    
    return audio_path

if __name__ == "__main__":
    result = extract_audio("C:/Users/jine7/Desktop/구동하.mp4")
    print(result)
