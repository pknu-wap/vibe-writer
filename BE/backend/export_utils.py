import subprocess
import os

def merge_video(frames_dir, audio_path, output_name="output.mp4"):
    """
    이미지 프레임들과 오디오 파일을 하나로 합치는 함수
    :param frames_dir: 이미지 파일들이 들어있는 폴더 경로
    :param audio_path: 합성할 오디오 파일 경로
    :param output_name: 최종 결과물 파일 이름
    """
    
    # 1. 이미지 파일 패턴 설정 (예: frame_0001.png, frame_0002.png ...)
    image_pattern = os.path.join(frames_dir, "frame_%04d.png")
    
    # 2. FFmpeg 명령어 구성
    command = [
        'ffmpeg',
        '-y',                          # 기존 파일이 있으면 덮어쓰기
        '-framerate', '30',            # 초당 프레임 수 (FPS)
        '-i', image_pattern,           # 입력 이미지 경로
        '-i', audio_path,              # 입력 오디오 경로
        '-c:v', 'libx264',             # 비디오 코덱 (H.264)
        '-pix_fmt', 'yuv420p',         # 대부분의 재생기에서 지원하는 픽셀 포맷
        '-c:a', 'aac',                 # 오디오 코덱 (AAC)
        '-shortest',                   # 영상/오디오 중 짧은 쪽에 맞춤
        output_name                    # 최종 파일명
    ]
    
    try:
        # 3. 명령어 실행
        print(f"합성을 시작합니다: {output_name}")
        subprocess.run(command, check=True)
        print("합성이 완료되었습니다!")
        
    except subprocess.CalledProcessError as e:
        print(f"합성 중 오류 발생: {e}")
    except FileNotFoundError:
        print("FFmpeg를 찾을 수 없습니다. 경로 설정을 확인해 주세요.")

# 사용 예시 (나중에 실제 경로로 수정)
# merge_video("./frames", "./background_music.mp3")