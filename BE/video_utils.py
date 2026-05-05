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

def get_still_cut(video_path, timestamp):
    video = VideoFileClip(video_path)
    frame = video.get_frame(timestamp)
    video.close()
    
    return frame


if __name__ == "__main__":
    result = extract_audio("C:/Users/jine7/Desktop/구동하.mp4")
    print(result)

    frame = get_still_cut("C:/Users/jine7/Desktop/구동하.mp4", 3.0)
    print(frame.shape)
