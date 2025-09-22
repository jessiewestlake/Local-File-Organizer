# Local File Organizer: AI File Management Run Entirely on Your Device, Privacy Assured

Tired of digital clutter? Overwhelmed by disorganized files scattered across your computer? Let AI do the heavy lifting! The Local File Organizer is your personal organizing assistant, using cutting-edge AI to bring order to your file chaos - all while respecting your privacy.

## How It Works 💡

Before:

```
/Users/Local-File-Organizer/sample_data
├── 1.md
├── 1.xlsx
├── 12222_777.docx
├── IMG_0967.PNG
├── c8fed35720671596882b0c6a2ad9586d.gif
├── go_bruin.pptx
├── logo.png
├── output.wav
├── paper_1col.pdf
├── sub_dir1
│   ├── 1111_63.csv
│   └── animal.jpg
├── sub_dir2
│   └── BS.txt
├── text_files
│   └── ccc.md
└── videoplayback.mp4
```

After:

```
/Users/Local-File-Organizer/organized_folder
├── excel_training
│   ├── outline_five_day.md
│   └── outline_five_day.xlsx
├── mathematics
│   └── present_fundamental_arithmetic.docx
├── string_theory
│   └── detailed_introduction_string.pdf
├── data_trend
│   └── presentation_explores_several.pptx
├── truck
│   └── present_list_ford.csv
├── travel_experience
│   └── chicago_consistently_ranked.md
├── banking_record
│   └── present_account_activity.txt
├── portrait
│   └── could_generate.gif
├── technology_brand
│   └── detailed_sent_google.png
├── storage_apps
│   └── detailed_overall_view.PNG
├── marine_life
│   └── detailed_overall_impression.jpg
├── tax_reform
│   └── corporate_tax_revisions_digital_businesses.wav
└── agent_development
    └── google_cloud_agent_development_hackathon.mp4
```

## Organization Modes 🗂️

The Local File Organizer supports four different organization modes:

### 1. By Content (AI-Powered)
Uses AI to analyze file content and create meaningful folder structures based on topics and themes.

### 2. By Date  
Organizes files into folders based on their creation or modification dates.

### 3. By Type
Groups files by their file extensions and types (documents, images, audio, etc.).

### 4. By Johnny.Decimal System 📊
Implements the Johnny.Decimal organizational methodology - a systematic approach to information organization:

**Core Principles:**
- **3 levels only**: Areas → Categories → Items
- **Strict limits**: Max 10 areas, 10 categories per area, 100 items per category
- **Unique numbers**: Everything gets exactly one number that never changes
- **User-defined structure**: You define what areas and categories mean for your needs

**How it works:**
- **Areas (10-19, 20-29, etc.)**: Major life/work domains you define
- **Categories (11, 12, 13, etc.)**: Subcategories within each area  
- **Items (11.01, 11.02, etc.)**: Your actual files with unique numbers

**Example Johnny.Decimal Structure:**
```
organized_folder/
├── 10-19 Life Admin/
│   ├── 11 Banking/
│   │   ├── 11.01 bank_statement_december.pdf
│   │   └── 11.02 investment_portfolio.pdf
│   └── 12 Tax/
│       ├── 12.01 tax_return_2024.pdf
│       └── 12.02 business_receipts.pdf
├── 20-29 Work/
│   └── 21 Current Projects/
│       ├── 21.01 project_proposal.docx
│       └── 21.02 meeting_notes.txt
└── 40-49 Resources/
    └── 41 Documentation/
        ├── 41.01 user_manual.pdf
        └── 41.02 technical_guide.pdf
```

This system provides a **framework for organization** rather than predefined categories, allowing you to create a personalized, scalable filing system that grows with your needs while maintaining structure and findability.

## Updates 🚀

**[2025/01] Johnny.Decimal System Added**:
* Added optional Johnny.Decimal organization mode for hierarchical file management
* Implements the Johnny.Decimal numbering system (Areas: 10-19, Categories: 11-19, Items: 11.01-11.99)
* Creates structured folder hierarchies with meaningful categorization
* Supports 9 main areas: Personal Management, Professional Work, Creative Projects, Reference Materials, Media Collection, Technical Resources, Communication, Archives, and Miscellaneous
* Works with AI-generated content descriptions for better categorization

**[2025/05] v0.0.3**:
* Major Backend Change: Switched AI inference from Nexa SDK to gemma3 and openai-whisper for local LLM/VLM processing. 
* Enhanced Text Processing: Integrated MarkItDown for robust conversion of various text file types (DOCX, PDF, PPTX, etc.) to Markdown before AI analysis. 
* Audio File Support: Added processing for audio files using Whisper for transcription and Gemma3:4b for metadata generation and image to text generation. 
* Video File Support: Added processing for video files using ffmpeg to extract audio, Whisper for transcription, and Ollama for metadata generation.
- Added file support: .md, .excel, .ppt, and .csv .txt, .docx, .doc, .pdf, .md, .xls, .xlsx, .ppt, .pptx, .csv, .mp3, .wav, .m4a, .flac, .aac, .ogg, .mp4, .mov, .avi, .mkv, .flv, .wmv.

**[2024/09] v0.0.2**:
Original from https://github.com/QiuYannnn/Local-File-Organizer.git
* Featured by [Nexa Gallery](https://nexaai.com/gallery) and [Nexa SDK Cookbook](https://github.com/NexaAI/nexa-sdk/tree/main/examples)!
* Dry Run Mode: check sorting results before committing changes
* Silent Mode: save all logs to a txt file for quieter operation
* Added file support:  `.md`, .`excel`, `.ppt`, and `.csv` 
* Three sorting options: by content, by date, and by type
* The default text model is now [Llama3.2 3B](https://nexaai.com/meta/Llama3.2-3B-Instruct/gguf-q3_K_M/file)
* Improved CLI interaction experience
* Added real-time progress bar for file analysis

Please update the project by deleting the original project folder and reinstalling the requirements. Refer to the installation guide from Step 4.


## Roadmap 📅

- [ ] Copilot Mode: chat with AI to tell AI how you want to sort the file (ie. read and rename all the PDFs)
- [ ] Change models with CLI 
- [x] ebook format support
- [x] audio file support
- [x] video file support
- [x] Implement best practices like Johnny Decimal
- [x] Check file duplication and more for pre-processing sort file-> using https://github.com/tfeldmann/organize 
- [ ] Dockerfile for easier installation

## Prerequisites 💻

- **Operating System:** Compatible with Windows, macOS, and Linux.
- **Python Version:** Python 3.12
- **Conda:** Anaconda or Miniconda installed.
- **Git:** For cloning the repository (or you can download the code as a ZIP file).
- **Ollama**: Installed and running on your system. Download from ollama.com. 
- **markitdown**: for converting some file types. Install from pandoc.org.
- **ffmpeg**: Required for extracting audio from video files. Install from ffmpeg.org.

## Installation 🛠

### 1. Install Python

Before installing the Local File Organizer, make sure you have Python installed on your system. We recommend using Python 3.12 or later.

You can download Python from [the official website]((https://www.python.org/downloads/)).

Follow the installation instructions for your operating system.

### 2. Clone the Repository

Clone this repository to your local machine using Git:

```zsh
git clone https://github.com/cuongtv89ks/Local-File-Organizer
```


Or download the repository as a ZIP file and extract it to your desired location.

### 3. Set Up the Python Environment

Create a new Conda environment named `local_file_organizer` with Python 3.12:

```zsh
conda create --name local_file_organizer python=3.12
```

Activate the environment:

```zsh
conda activate local_file_organizer
```
### 4. Install Dependencies 

1. Ensure you are in the project directory:
   ```zsh
   cd path/to/Local-File-Organizer
   ```
   Replace `path/to/Local-File-Organizer` with the actual path where you cloned or extracted the project.

2. Install the required dependencies:
   ```zsh
   pip install -r requirements.txt
   ```

   ```zsh
   # on Ubuntu or Debian
  sudo apt update && sudo apt install ffmpeg

    # on Arch Linux
    sudo pacman -S ffmpeg

    # on MacOS using Homebrew (https://brew.sh/)
    brew install ffmpeg

    # on Windows using Chocolatey (https://chocolatey.org/)
    choco install ffmpeg

    # on Windows using Scoop (https://scoop.sh/)
    scoop install ffmpeg
   ```

With the environment activated and dependencies installed, run the script using:

### 5. Running the Script🎉
```zsh
python main.py
```

## Notes
- **Processing Time:**
  - Processing may take time depending on the number and size of files.
  - The script uses multiprocessing to improve performance.

- **Customizing Prompts:**
  - You can adjust prompts in `data_processing.py` to change how metadata is generated.

## License

This project is dual-licensed under the MIT License and Apache 2.0 License. You may choose which license you prefer to use for this project.

- See the [MIT License](LICENSE-MIT) for more details.