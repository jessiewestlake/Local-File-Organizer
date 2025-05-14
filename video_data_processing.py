import os
import tempfile
import subprocess # For ffmpeg
from audio_data_processing import transcribe_audio_file, generate_audio_metadata_ollama # Reuse
from data_processing_common import sanitize_filename

def convert_video_to_audio_ffmpeg(video_path, output_audio_path, sample_rate=16000, audio_codec='pcm_s16le'):
    """
    Converts a video file to an audio file using ffmpeg.

    Args:
        video_path (str): Path to the input video file.
        output_audio_path (str): Path to save the output audio file (e.g., 'output.wav').
        sample_rate (int): The sample rate for the output audio. 16000 Hz is common for speech.
        audio_codec (str): The audio codec to use. 'pcm_s16le' is standard for WAV.

    Returns:
        bool: True if conversion was successful, False otherwise.
    """
    if not os.path.exists(video_path):
        print(f"Error: Video file not found at {video_path}")
        return False

    command = [
        'ffmpeg',
        '-i', video_path,      # Input video file
        '-vn',                 # No video output (disable video recording)
        '-acodec', audio_codec, # Audio codec (e.g., pcm_s16le for WAV)
        '-ar', str(sample_rate),# Audio sample rate (e.g., 16000 Hz)
        '-ac', '1',            # Number of audio channels (1 for mono, 2 for stereo)
        '-y',                  # Overwrite output file if it exists
        output_audio_path
    ]

    try:
        print(f"Converting {video_path} to {output_audio_path}...")
        process = subprocess.run(command, check=True, capture_output=True, text=True)
        print("Conversion successful!")
        # print("ffmpeg stdout:", process.stdout) # Optional: for debugging
        # print("ffmpeg stderr:", process.stderr) # Optional: for debugging
        return True
    except FileNotFoundError:
        print("Error: ffmpeg command not found. Please ensure ffmpeg is installed and in your PATH.")
        return False
    except subprocess.CalledProcessError as e:
        print(f"Error during ffmpeg conversion for {video_path}:")
        print(f"Command: {' '.join(e.cmd)}")
        print(f"Return code: {e.returncode}")
        print(f"Stderr: {e.stderr}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred during ffmpeg conversion for {video_path}: {e}")
        return False

import os
import tempfile
import subprocess # For ffmpeg
from audio_data_processing import transcribe_audio_file, generate_audio_metadata_ollama # Reuse
from data_processing_common import sanitize_filename
# ... (các import khác nếu cần) ...

# (Hàm convert_video_to_audio_ffmpeg đã định nghĩa ở trên có thể đặt ở đây hoặc trong một file utils chung)

def process_single_video_file(video_path, silent=False, log_file=None):
    # Create a temporary directory for extracted audio if it doesn't exist
    temp_audio_dir = os.path.join(os.path.dirname(video_path), "temp_audio_for_video")
    os.makedirs(temp_audio_dir, exist_ok=True)
    
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    temp_audio_path = os.path.join(temp_audio_dir, f"{base_name}_extracted.wav")

    if convert_video_to_audio_ffmpeg(video_path, temp_audio_path):
        transcribed_text = transcribe_audio_file(temp_audio_path) # From audio_data_processing
        
        if transcribed_text:
            # Reuse or adapt metadata generation logic
            # For simplicity, let's assume generate_audio_metadata_ollama can be used
            # You might want to adjust prompts for video context
            # This part needs a progress bar similar to other processing functions
            # For now, skipping the rich.progress for brevity in this example snippet
            
            # Placeholder for progress bar logic
            class DummyProgress:
                def update(self, task_id, advance): pass
            class DummyTaskId: pass

            foldername, filename, description = generate_audio_metadata_ollama(
                transcribed_text, 
                video_path, # Pass original video path for context if needed by metadata gen
                DummyProgress(), 
                DummyTaskId()
            )
            
            # Clean up the temporary audio file
            try:
                os.remove(temp_audio_path)
                # Optionally remove temp_audio_dir if it's empty
                if not os.listdir(temp_audio_dir):
                    os.rmdir(temp_audio_dir)
            except OSError as e:
                print(f"Error removing temporary audio file {temp_audio_path}: {e}")

            return {'file_path': video_path, 'foldername': foldername, 'filename': filename, 'description': description}
        else:
            message = f"Transcription failed for audio extracted from {video_path}"
            # Clean up temp audio even if transcription failed
            try:
                os.remove(temp_audio_path)
                if not os.listdir(temp_audio_dir):
                    os.rmdir(temp_audio_dir)
            except OSError: pass
            return {'file_path': video_path, 'foldername': 'failed_video_processing', 'filename': base_name + '_transcription_failed', 'description': message}
    else:
        message = f"Failed to extract audio from video: {video_path}"
        return {'file_path': video_path, 'foldername': 'failed_video_processing', 'filename': base_name + '_audio_extraction_failed', 'description': message}

def process_video_files(video_paths, silent=False, log_file=None):
    results = []
    if not video_paths:
        return results
    # Potentially initialize Whisper model once if not already done by audio_data_processing
    # from audio_data_processing import initialize_whisper_model
    # initialize_whisper_model() 
    
    for video_path in video_paths:
        data = process_single_video_file(video_path, silent=silent, log_file=log_file)
        results.append(data)
    return results
