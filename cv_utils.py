from pathlib import Path
from moviepy.editor import VideoFileClip, concatenate_videoclips

def seconds_to_mmss(seconds):
    """Convert seconds to MM:SS format."""
    seconds = int(round(seconds))
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes:02d}:{secs:02d}"

def mmss_to_seconds(time_str):
    """Convert MM:SS format to seconds."""
    minutes, seconds = time_str.strip().split(":")
    return int(minutes) * 60 + int(seconds)

def mmss_to_seconds_flexible(time_str):
    """
    Convert M:SS or MM:SS to seconds.
    """
    time_str = clean_timestamp(time_str)
    minutes, seconds = time_str.strip().split(":")
    return int(minutes) * 60 + int(seconds)


def clean_timestamp(time_str):
    """
    Clean timestamp mistakes such as:
    MM:00:20 -> 00:20
    00:20 -> 00:20
    """
    time_str = time_str.strip()
    time_str = time_str.replace("MM:", "")
    time_str = time_str.replace("SS", "")
    return time_str

def output_dir(pth: str)-> str:
    try:
        dir = Path(pth)
        dir.mkdir(parents=True, exist_ok=True)
    except IOError as e:
        raise IOError(f"path {pth} for ")
    return dir

def load_vid_pth(pth):
    video_path = Path(pth)
    if not video_path.exists():
        raise FileNotFoundError(f"Video not found: {video_path}")
    return video_path

def normalise_dash(line: str)->str:
    return line.replace("–", "-").replace("—", "-")



def stitch_video_segments(video_path, timestamps, output_path="summarized_video.mp4"):
    """
    Extracts specific time segments from a video and stitches them together seamlessly.
    
    Parameters:
    - video_path : str
        The path to the original video.
    - timestamps : List[tuples]
        A list containing (start, stop) times in seconds.
    - output_path (str or Path): Where to save the final stitched video.
    """
    print(f"Loading video from: {video_path}")
    
    try:
        video_path=load_vid_pth(video_path)
        print(f"path found {video_path}")
        video = VideoFileClip(str(video_path))
        clips = []
        for start, stop in timestamps:
            clip = video.subclip(start, stop)
            clips.append(clip)
    
        if not clips:
            raise ValueError("fNo clips found in {clips}")

        final_video = concatenate_videoclips(clips)
        final_video.write_videofile(
            str(output_path), 
            codec="libx264", 
            audio_codec="aac",
            logger=None
        )        
        video.close()
        for clip in clips:
            clip.close()

        print(f"Video successfully generated, saved to {output_path}")
        
    except Exception as e:
        print(f"An error occurred while processing the video: {e}")
