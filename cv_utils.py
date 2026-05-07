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
