import re
import os
import time
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from rich.progress import Progress, TextColumn, BarColumn, TimeElapsedColumn
import ollama # Import ollama client
from data_processing_common import sanitize_filename  # Import sanitize_filename

# Define the Ollama models to use. Can be configured via environment variables.
OLLAMA_MODEL_VISION = os.getenv("OLLAMA_MODEL_VISION", "gemma3:4b") # Example VLM
OLLAMA_MODEL_TEXT_FOR_IMAGE_METADATA = os.getenv("OLLAMA_MODEL_TEXT_FOR_IMAGE_METADATA", "gemma3:4b") # For filename/foldername from description

def process_single_image(image_path, silent=False, log_file=None):
    """Process a single image file to generate metadata."""
    start_time = time.time()

    # Create a Progress instance for this file
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TimeElapsedColumn()
    ) as progress:
        task_id = progress.add_task(f"Processing {os.path.basename(image_path)}", total=1.0)
        # image_inference and text_inference arguments are removed as Ollama is used directly
        foldername, filename, description = generate_image_metadata_ollama(image_path, progress, task_id)
    
    end_time = time.time()
    time_taken = end_time - start_time

    message = f"File: {image_path}\nTime taken: {time_taken:.2f} seconds\nDescription: {description}\nFolder name: {foldername}\nGenerated filename: {filename}\n"
    if silent:
        if log_file:
            with open(log_file, 'a') as f:
                f.write(message + '\n')
    else:
        print(message)
    return {
        'file_path': image_path,
        'foldername': foldername,
        'filename': filename,
        'description': description
    }

def process_image_files(image_paths, silent=False, log_file=None):
    """Process image files sequentially."""
    data_list = []
    for image_path in image_paths:
        # image_inference and text_inference arguments removed
        data = process_single_image(image_path, silent=silent, log_file=log_file)
        data_list.append(data)
    return data_list

def generate_image_metadata_ollama(image_path, progress, task_id):
    """Generate description, folder name, and filename for an image file using Ollama."""

    # Total steps in processing an image
    total_steps = 3

    # Step 1: Generate description using Ollama Vision model
    description_prompt = "Please provide a detailed description of this image, focusing on the main subject and any important details."
    description = "Could not generate description." # Default
    try:
        # For Ollama VLM, you typically provide the image path directly in the 'images' list
        response = ollama.generate(
            model=OLLAMA_MODEL_VISION,
            prompt=description_prompt,
            images=[image_path], # Pass the image path
            stream=False
        )
        description = response['response'].strip()
    except FileNotFoundError:
        print(f"Error: Image file not found at {image_path} for Ollama processing.")
        # Keep default description or handle as needed
    except Exception as e:
        print(f"Error calling Ollama Vision for image description ({image_path}): {e}")
        # Keep default description
    progress.update(task_id, advance=1 / total_steps)

    # Step 2: Generate filename using text_inference
    filename_prompt = f"""Based on the description below, generate a specific and descriptive filename for the image.
Limit the filename to a maximum of 5 words. Use nouns and avoid starting with verbs like 'depicts', 'shows', 'presents', etc.
Do not include any data type words like 'image', 'jpg', 'png', etc. Use only letters and connect words with underscores.

Description: {description}

Example:
Description: A photo of a sunset over the mountains.
Filename: sunset_over_mountains

Now generate the filename.

Output only the filename, without any additional text.

Filename:"""
    filename = "untitled_image" # Default
    try:
        filename_response_ollama = ollama.generate(
            model=OLLAMA_MODEL_TEXT_FOR_IMAGE_METADATA, # Use a text model for this
            prompt=filename_prompt,
            stream=False
        )
        filename = filename_response_ollama['response'].strip()
    except Exception as e:
        print(f"Error calling Ollama for image filename ({image_path}): {e}")
        # Keep default filename
    # Remove 'Filename:' prefix if present
    filename = re.sub(r'^Filename:\s*', '', filename, flags=re.IGNORECASE).strip()
    progress.update(task_id, advance=1 / total_steps)

    # Step 3: Generate folder name from description using text_inference
    foldername_prompt = f"""Based on the description below, generate a general category or theme that best represents the main subject of this image.
This will be used as the folder name. Limit the category to a maximum of 2 words. Use nouns and avoid verbs.
Do not include specific details, words from the filename, or any generic terms like 'untitled' or 'unknown'.

Description: {description}

Examples:
1. Description: A photo of a sunset over the mountains.
   Category: landscapes

2. Description: An image of a smartphone displaying a storage app with various icons and information.
   Category: technology

3. Description: A close-up of a blooming red rose with dew drops.
   Category: nature

Now generate the category.

Output only the category, without any additional text.

Category:"""
    foldername = "general_images" # Default
    try:
        foldername_response_ollama = ollama.generate(
            model=OLLAMA_MODEL_TEXT_FOR_IMAGE_METADATA, # Use a text model for this
            prompt=foldername_prompt,
            stream=False
        )
        foldername = foldername_response_ollama['response'].strip()
    except Exception as e:
        print(f"Error calling Ollama for image foldername ({image_path}): {e}")
        # Keep default foldername
    # Remove 'Category:' prefix if present
    foldername = re.sub(r'^Category:\s*', '', foldername, flags=re.IGNORECASE).strip()
    progress.update(task_id, advance=1 / total_steps)

    # Remove any unwanted words and stopwords
    unwanted_words = set([
        'the', 'and', 'based', 'generated', 'this', 'is', 'filename', 'file', 'image', 'picture', 'photo',
        'folder', 'category', 'output', 'only', 'below', 'text', 'jpg', 'png', 'jpeg', 'gif', 'bmp', 'svg',
        'logo', 'in', 'on', 'of', 'with', 'by', 'for', 'to', 'from', 'a', 'an', 'as', 'at', 'red', 'blue',
        'green', 'color', 'colors', 'colored', 'text', 'graphic', 'graphics', 'main', 'subject', 'important',
        'details', 'description', 'depicts', 'show', 'shows', 'display', 'illustrates', 'presents', 'features',
        'provides', 'covers', 'includes', 'demonstrates', 'describes'
    ])
    stop_words = set(stopwords.words('english'))
    all_unwanted_words = unwanted_words.union(stop_words)
    lemmatizer = WordNetLemmatizer()

    # Function to clean and process the AI output
    def clean_ai_output(text, max_words):
        # Remove file extensions and special characters
        text = re.sub(r'\.\w{1,4}$', '', text)  # Remove file extensions like .jpg, .png
        text = re.sub(r'[^\w\s]', ' ', text)  # Remove special characters
        text = re.sub(r'\d+', '', text)  # Remove digits
        text = text.strip()
        # Split concatenated words (e.g., 'GoogleChrome' -> 'Google Chrome')
        text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
        # Tokenize and lemmatize words
        words = word_tokenize(text)
        words = [word.lower() for word in words if word.isalpha()]
        words = [lemmatizer.lemmatize(word) for word in words]
        # Remove unwanted words and duplicates
        filtered_words = []
        seen = set()
        for word in words:
            if word not in all_unwanted_words and word not in seen:
                filtered_words.append(word)
                seen.add(word)
        # Limit to max words
        filtered_words = filtered_words[:max_words]
        return '_'.join(filtered_words)

    # Process filename
    filename = clean_ai_output(filename, max_words=3)
    if not filename or filename.lower() in ('untitled', ''):
        # Use keywords from the description
        filename = clean_ai_output(description, max_words=3)
    if not filename:
        filename = 'image_' + os.path.splitext(os.path.basename(image_path))[0]

    sanitized_filename = sanitize_filename(filename, max_words=3)

    # Process foldername
    foldername = clean_ai_output(foldername, max_words=2)
    if not foldername or foldername.lower() in ('untitled', ''):
        # Attempt to extract keywords from the description
        foldername = clean_ai_output(description, max_words=2)
        if not foldername:
            foldername = 'images'

    sanitized_foldername = sanitize_filename(foldername, max_words=2)

    return sanitized_foldername, sanitized_filename, description
