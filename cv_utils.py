from pathlib import Path

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

def normalise_dash(line: str)->str:
    return line.replace("–", "-").replace("—", "-")

def run_and_parse_pipeline(video_name, video_path, output_dir, prompt_name, prompt_text, parser_func):
    """
    Generic pipeline to sample frames, run the VLM, save raw text, and parse the output.
    """
    video_output_dir = output_dir / video_name
    video_output_dir.mkdir(parents=True, exist_ok=True)
    frame_dir = video_output_dir / "sampled_frames"

    # 1. Sample frames (will overwrite/reuse if they already exist)
    sampled_frames = sample_frames_from_video(
        video_path=video_path,
        output_frame_dir=frame_dir,
        every_n_seconds=FRAME_EVERY_N_SECONDS,
        max_frames=MAX_FRAMES_FOR_VLM
    )
    
    sampled_frames_df = pd.DataFrame(sampled_frames)
    sampled_frames_df.to_csv(video_output_dir / "sampled_frames_metadata.csv", index=False)

    # 2. Run VLM
    vlm_output = run_qwen_vlm(
        sampled_frames=sampled_frames,
        prompt=prompt_text,
        max_new_tokens=512
    )
    
    # 3. Save Raw Output
    save_text(vlm_output, video_output_dir / f"vlm_raw_{prompt_name}.txt")

    # 4. Parse Output
    parsed_df = parser_func(vlm_output)
    
    if parsed_df.empty:
        print(f"\nWARNING: Parser found no events for {prompt_name}.")
        print(vlm_output)

    # 5. Format and Save Parsed Data
    parsed_df.insert(0, "video_name", video_name)
    parsed_df.insert(1, "prompt_name", prompt_name)
    parsed_df.to_csv(video_output_dir / f"parsed_{prompt_name}.csv", index=False)

    return sampled_frames_df, vlm_output, parsed_df