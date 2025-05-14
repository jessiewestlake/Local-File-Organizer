import re
import os
import time
import nltk # NLTK is still needed for cleaning text from Whisper
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from rich.progress import Progress, TextColumn, BarColumn, TimeElapsedColumn
import ollama # For generating metadata from transcribed text
import whisper # For transcribing audio
from data_processing_common import sanitize_filename

# Define the Ollama model to use for generating metadata from transcribed text.
OLLAMA_MODEL_TEXT_FOR_AUDIO_METADATA = os.getenv("OLLAMA_MODEL_TEXT_FOR_AUDIO_METADATA", "gemma3:4b")
# Define the Whisper model to use.
WHISPER_MODEL_NAME = os.getenv("WHISPER_MODEL_NAME", "turbo") # Options: "tiny", "base", "small", "medium", "large", "large-v2", "large-v3"

whisper_model_instance = None

def initialize_whisper_model():
    """Initialize the Whisper model if it hasn't been initialized yet."""
    global whisper_model_instance
    if whisper_model_instance is None:
        try:
            print(f"Loading Whisper model: {WHISPER_MODEL_NAME}...")
            whisper_model_instance = whisper.load_model(WHISPER_MODEL_NAME)
            print("Whisper model loaded successfully.")
        except Exception as e:
            print(f"Error loading Whisper model {WHISPER_MODEL_NAME}: {e}")
            whisper_model_instance = None # Ensure it's None if loading failed

def transcribe_audio_file(audio_path):
    """Transcribe an audio file using Whisper."""
    initialize_whisper_model()
    if whisper_model_instance is None:
        print("Whisper model not available. Cannot transcribe.")
        return None
    try:
        print(f"Transcribing audio file: {audio_path}...")
        # For CPU, fp16=False is generally recommended. If you have a compatible GPU and CUDA/PyTorch setup, you might use fp16=True.
        result = whisper_model_instance.transcribe(audio_path, fp16=False)
        transcribed_text = result["text"].strip()
        print(f"Transcription successful for {audio_path}.")
        return transcribed_text
    except Exception as e:
        print(f"Error transcribing audio file {audio_path}: {e}")
        return None

def generate_audio_metadata_ollama(transcribed_text, audio_file_path, progress, task_id):
    """Generate description (summary), folder name, and filename for transcribed audio using Ollama."""
    total_steps = 3 # Summarize, generate filename, generate foldername

    # Step 1: Summarize the transcribed text (similar to text_data_processing)
    summary_prompt = f"""Provide a concise and accurate summary of the following transcribed audio content, focusing on the main ideas and key details.
Limit your summary to a maximum of 150 words and DO NOT need print out your thought.

Transcribed Audio Content:
{transcribed_text}

Summary:"""
    description = "Could not generate summary for audio." # Default
    try:
        response = ollama.generate(
            model=OLLAMA_MODEL_TEXT_FOR_AUDIO_METADATA,
            prompt=summary_prompt,
            stream=False
        )
        description = response['response'].strip()
    except Exception as e:
        print(f"Error calling Ollama for audio summary ({os.path.basename(audio_file_path)}): {e}")
    progress.update(task_id, advance=1 / total_steps)

    # Step 2: Generate filename from the summary
    filename_prompt = f"""Based on the summary of the transcribed audio below, generate a specific and descriptive filename.
Limit the filename to a maximum of 5 words. Use nouns and avoid starting with verbs.
Do not include data type words like 'audio', 'mp3', 'transcription', etc. Use only letters and connect words with underscores.

Summary: {description}

Filename:"""
    filename = "untitled_audio_transcription" # Default
    try:
        filename_response_ollama = ollama.generate(
            model=OLLAMA_MODEL_TEXT_FOR_AUDIO_METADATA,
            prompt=filename_prompt,
            stream=False
        )
        filename = filename_response_ollama['response'].strip()
        filename = re.sub(r'^Filename:\s*', '', filename, flags=re.IGNORECASE).strip()
    except Exception as e:
        print(f"Error calling Ollama for audio filename ({os.path.basename(audio_file_path)}): {e}")
    progress.update(task_id, advance=1 / total_steps)

    # Step 3: Generate folder name from the summary
    foldername_prompt = f"""Based on the summary of the transcribed audio below, generate a general category or theme.
This will be used as the folder name. Limit the category to a maximum of 2 words. Use nouns and avoid verbs.

Summary: {description}

Category:"""
    foldername = "general_audio" # Default
    try:
        foldername_response_ollama = ollama.generate(
            model=OLLAMA_MODEL_TEXT_FOR_AUDIO_METADATA,
            prompt=foldername_prompt,
            stream=False
        )
        foldername = foldername_response_ollama['response'].strip()
        foldername = re.sub(r'^Category:\s*', '', foldername, flags=re.IGNORECASE).strip()
    except Exception as e:
        print(f"Error calling Ollama for audio foldername ({os.path.basename(audio_file_path)}): {e}")
    progress.update(task_id, advance=1 / total_steps)

    # Re-use or adapt the clean_ai_output logic from text_data_processing.py if needed
    # For simplicity, we'll just sanitize directly here.
    # You might want to create a shared cleaning utility if the logic is identical.
    
    # Basic cleaning and sanitization (can be expanded like in text_data_processing.py)
    sanitized_filename = sanitize_filename(filename if filename else "audio_" + os.path.splitext(os.path.basename(audio_file_path))[0], max_words=5)
    sanitized_foldername = sanitize_filename(foldername if foldername else "audio_files", max_words=2)

    return sanitized_foldername, sanitized_filename, description

def process_single_audio_file(audio_path, silent=False, log_file=None):
    """Process a single audio file: transcribe and generate metadata."""
    start_time = time.time()
    transcribed_text = transcribe_audio_file(audio_path)

    if transcribed_text is None:
        message = f"File: {audio_path}\nError: Transcription failed or Whisper model not available.\n"
        # Handle logging/printing as in other modules
        return {'file_path': audio_path, 'foldername': 'failed_audio', 'filename': os.path.splitext(os.path.basename(audio_path))[0] + '_transcription_failed', 'description': 'Transcription failed.'}

    with Progress(TextColumn("[progress.description]{task.description}"), BarColumn(), TimeElapsedColumn()) as progress:
        task_id = progress.add_task(f"Generating metadata for {os.path.basename(audio_path)}", total=1.0)
        foldername, filename, description = generate_audio_metadata_ollama(transcribed_text, audio_path, progress, task_id)

    time_taken = time.time() - start_time
    message = f"File: {audio_path}\nTime taken: {time_taken:.2f} seconds\nTranscription Summary: {description}\nFolder name: {foldername}\nGenerated filename: {filename}\n"
    # Handle logging/printing
    if silent and log_file:
        with open(log_file, 'a', encoding='utf-8') as f: f.write(message + '\n')
    elif not silent:
        print(message)

    return {'file_path': audio_path, 'foldername': foldername, 'filename': filename, 'description': description}

def process_audio_files(audio_paths, silent=False, log_file=None):
    """Process a list of audio files."""
    results = []
    if not audio_paths:
        return results
    initialize_whisper_model() # Initialize Whisper model once before processing batch
    for audio_path in audio_paths:
        data = process_single_audio_file(audio_path, silent=silent, log_file=log_file)
        results.append(data)
    return results