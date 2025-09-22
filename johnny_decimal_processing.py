"""
Johnny.Decimal System Implementation for Local File Organizer

The Johnny.Decimal system uses a hierarchical numbering approach:
- Areas: 10-19, 20-29, 30-39, etc. (broad categories)
- Categories: 11, 12, 13, etc. (subcategories within areas)
- Items: 11.01, 11.02, 11.03, etc. (individual files)

Example structure:
10-19 Personal Management
├── 11 Finance
│   ├── 11.01 Bank statements
│   ├── 11.02 Tax documents
│   └── 11.03 Investment records
├── 12 Health
│   ├── 12.01 Medical records
│   └── 12.02 Insurance documents
└── 13 Education
    ├── 13.01 Certificates
    └── 13.02 Course materials
"""

import os
import re
from typing import Dict, List, Tuple
from data_processing_common import sanitize_filename


class JohnnyDecimalOrganizer:
    """Johnny.Decimal system organizer for file management."""
    
    def __init__(self):
        # Define standard areas and categories based on common file types
        self.areas = {
            10: "Personal Management",
            20: "Professional Work", 
            30: "Creative Projects",
            40: "Reference Materials",
            50: "Media Collection",
            60: "Technical Resources",
            70: "Communication",
            80: "Archives",
            90: "Miscellaneous"
        }
        
        # Define categories within each area
        self.categories = {
            # Personal Management (10-19)
            11: "Finance",
            12: "Health", 
            13: "Education",
            14: "Legal Documents",
            15: "Travel",
            16: "Personal Projects",
            17: "Insurance",
            18: "Housing",
            19: "Personal Archive",
            
            # Professional Work (20-29)
            21: "Projects",
            22: "Reports",
            23: "Presentations", 
            24: "Contracts",
            25: "Research",
            26: "Meeting Notes",
            27: "Professional Development",
            28: "Business Documents",
            29: "Work Archive",
            
            # Creative Projects (30-39)
            31: "Photography",
            32: "Writing",
            33: "Design",
            34: "Music",
            35: "Video",
            36: "Art",
            37: "Crafts",
            38: "Creative Tools",
            39: "Creative Archive",
            
            # Reference Materials (40-49)
            41: "Documentation",
            42: "Manuals",
            43: "Research Papers",
            44: "Books",
            45: "Articles",
            46: "Standards",
            47: "Guidelines",
            48: "Templates",
            49: "Reference Archive",
            
            # Media Collection (50-59)
            51: "Images",
            52: "Audio",
            53: "Video Files",
            54: "Graphics",
            55: "Multimedia",
            56: "Screenshots",
            57: "Digital Art",
            58: "Media Tools",
            59: "Media Archive",
            
            # Technical Resources (60-69)
            61: "Code",
            62: "Configurations",
            63: "Databases",
            64: "Systems",
            65: "Software",
            66: "Technical Documentation",
            67: "Development Tools",
            68: "Technical Projects",
            69: "Technical Archive",
            
            # Communication (70-79)
            71: "Emails",
            72: "Messages",
            73: "Social Media",
            74: "Forums",
            75: "Correspondence",
            76: "Announcements",
            77: "Marketing",
            78: "Public Relations",
            79: "Communication Archive",
            
            # Archives (80-89)
            81: "Old Projects",
            82: "Backup Files",
            83: "Historical Data",
            84: "Legacy Systems",
            85: "Old Media",
            86: "Retired Documents",
            87: "Archive Tools",
            88: "Migration Data",
            89: "General Archive",
            
            # Miscellaneous (90-99)
            91: "Temporary Files",
            92: "Downloads",
            93: "Uncategorized",
            94: "Tools",
            95: "Utilities",
            96: "Experimental",
            97: "Testing",
            98: "Sandbox",
            99: "Mixed Content"
        }
        
        # Category mapping based on content keywords
        self.content_category_mapping = {
            # Finance related
            "finance": 11, "money": 11, "bank": 11, "tax": 11, "budget": 11, "investment": 11,
            "financial": 11, "accounting": 11, "receipt": 11, "invoice": 11,
            
            # Health related  
            "health": 12, "medical": 12, "doctor": 12, "hospital": 12, "medicine": 12,
            "healthcare": 12, "treatment": 12, "therapy": 12, "diagnosis": 12,
            
            # Education related
            "education": 13, "school": 13, "university": 13, "course": 13, "learning": 13,
            "study": 13, "academic": 13, "research": 13, "thesis": 13, "degree": 13,
            
            # Legal related
            "legal": 14, "contract": 24, "agreement": 24, "law": 14, "court": 14,
            "lawyer": 14, "attorney": 14, "litigation": 14,
            
            # Travel related
            "travel": 15, "trip": 15, "vacation": 15, "flight": 15, "hotel": 15,
            "tourism": 15, "journey": 15, "destination": 15,
            
            # Technology related
            "technology": 66, "tech": 66, "software": 65, "hardware": 64, "computer": 64,
            "programming": 61, "code": 61, "development": 61, "system": 64,
            
            # Creative related
            "photo": 31, "image": 51, "picture": 51, "photography": 31,
            "music": 34, "audio": 52, "sound": 52, "video": 53, "film": 53, "movie": 53,
            "art": 36, "design": 33, "creative": 36, "drawing": 36, "painting": 36,
            
            # Professional related
            "project": 21, "work": 21, "business": 28, "professional": 21,
            "report": 22, "presentation": 23, "meeting": 26,
            
            # Reference related
            "manual": 42, "documentation": 41, "guide": 42, "reference": 41,
            "book": 44, "article": 45, "paper": 43, "standard": 46
        }
        
        # File extension to category mapping
        self.extension_category_mapping = {
            # Images
            ".jpg": 51, ".jpeg": 51, ".png": 51, ".gif": 51, ".bmp": 51, ".tiff": 51, ".svg": 51,
            
            # Audio
            ".mp3": 52, ".wav": 52, ".flac": 52, ".aac": 52, ".ogg": 52, ".m4a": 52,
            
            # Video
            ".mp4": 53, ".avi": 53, ".mkv": 53, ".mov": 53, ".wmv": 53, ".flv": 53,
            
            # Documents
            ".pdf": 41, ".doc": 22, ".docx": 22, ".txt": 41, ".md": 41,
            
            # Spreadsheets
            ".xls": 22, ".xlsx": 22, ".csv": 22,
            
            # Presentations
            ".ppt": 23, ".pptx": 23,
            
            # Code
            ".py": 61, ".js": 61, ".html": 61, ".css": 61, ".java": 61, ".cpp": 61, ".c": 61,
            ".php": 61, ".rb": 61, ".go": 61, ".rs": 61, ".ts": 61,
            
            # Archives
            ".zip": 82, ".rar": 82, ".7z": 82, ".tar": 82, ".gz": 82,
            
            # Configuration
            ".json": 62, ".xml": 62, ".yaml": 62, ".yml": 62, ".ini": 62, ".cfg": 62, ".conf": 62
        }

    def categorize_file(self, file_path: str, content_description: str = "") -> Tuple[int, int, str]:
        """
        Categorize a file into Johnny.Decimal system.
        
        Returns:
            Tuple of (area_number, category_number, item_description)
        """
        file_name = os.path.basename(file_path).lower()
        file_ext = os.path.splitext(file_path)[1].lower()
        content_lower = content_description.lower()
        
        # Try to categorize based on content keywords first
        for keyword, category in self.content_category_mapping.items():
            if keyword in content_lower or keyword in file_name:
                area = (category // 10) * 10
                return area, category, self.categories[category]
        
        # Try to categorize based on file extension
        if file_ext in self.extension_category_mapping:
            category = self.extension_category_mapping[file_ext]
            area = (category // 10) * 10
            return area, category, self.categories[category]
        
        # Default to miscellaneous
        return 90, 93, self.categories[93]

    def generate_johnny_decimal_path(self, file_path: str, content_description: str = "",
                                   item_counter: Dict[int, int] = None) -> Tuple[str, str]:
        """
        Generate Johnny.Decimal path for a file.
        
        Args:
            file_path: Original file path
            content_description: AI-generated description of file content
            item_counter: Dictionary to track item numbers per category
            
        Returns:
            Tuple of (folder_path, new_filename)
        """
        if item_counter is None:
            item_counter = {}
            
        area, category, category_name = self.categorize_file(file_path, content_description)
        
        # Get or create item number for this category
        if category not in item_counter:
            item_counter[category] = 1
        else:
            item_counter[category] += 1
            
        item_number = f"{category}.{item_counter[category]:02d}"
        
        # Create folder structure
        area_name = f"{area}-{area+9} {self.areas[area]}"
        category_folder = f"{category} {category_name}"
        
        folder_path = os.path.join(area_name, category_folder)
        
        # Generate filename with Johnny.Decimal number
        original_name = os.path.splitext(os.path.basename(file_path))[0]
        file_ext = os.path.splitext(file_path)[1]
        
        # Sanitize and create new filename
        if content_description:
            # Use content description for more meaningful filename
            filename_base = sanitize_filename(content_description, max_words=4)
        else:
            filename_base = sanitize_filename(original_name, max_words=4)
            
        # Ensure we have a valid filename base
        if not filename_base or filename_base.strip() == "":
            filename_base = "document"
            
        new_filename = f"{item_number} {filename_base}{file_ext}"
        
        return folder_path, new_filename


def process_files_johnny_decimal(file_paths: List[str], output_path: str, 
                                file_descriptions: Dict[str, str] = None,
                                dry_run: bool = False, silent: bool = False, 
                                log_file: str = None) -> List[Dict]:
    """
    Process files using Johnny.Decimal organization system.
    
    Args:
        file_paths: List of file paths to organize
        output_path: Base output directory
        file_descriptions: Optional dictionary of file_path -> description
        dry_run: If True, don't actually move files
        silent: If True, suppress output
        log_file: Optional log file path
        
    Returns:
        List of operation dictionaries
    """
    organizer = JohnnyDecimalOrganizer()
    operations = []
    item_counters = {}  # Track item numbers per category
    
    if file_descriptions is None:
        file_descriptions = {}
    
    for file_path in file_paths:
        # Skip hidden files
        if os.path.basename(file_path).startswith('.'):
            continue
            
        # Get content description if available
        content_description = file_descriptions.get(file_path, "")
        
        # Generate Johnny.Decimal path
        folder_path, new_filename = organizer.generate_johnny_decimal_path(
            file_path, content_description, item_counters
        )
        
        # Create full destination path
        full_folder_path = os.path.join(output_path, folder_path)
        destination_path = os.path.join(full_folder_path, new_filename)
        
        # Create operation record
        operation = {
            'source': file_path,
            'destination': destination_path,
            'link_type': 'hardlink',  # Default to hardlink
            'folder_name': folder_path,
            'new_file_name': new_filename
        }
        
        operations.append(operation)
        
        # Log operation if not silent
        if not silent:
            message = f"Johnny.Decimal: {file_path} -> {folder_path}/{new_filename}"
            if log_file:
                with open(log_file, 'a') as f:
                    f.write(message + '\n')
            else:
                print(message)
    
    return operations