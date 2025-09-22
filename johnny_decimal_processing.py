"""
Johnny.Decimal System Implementation for Local File Organizer

The Johnny.Decimal system is an organizational methodology with these core principles:
- Areas: 10-19, 20-29, 30-39, etc. (10 possible areas maximum)
- Categories: 11-19, 21-29, 31-39, etc. (10 categories per area maximum)  
- Items: 11.01-11.99, 12.01-12.99, etc. (100 items per category maximum)

Key principles:
- Everything has one place and one unique number
- Numbers never change once assigned
- Maximum 3 levels of hierarchy (Area/Category/Item)
- User defines their own organizational structure
- System provides the framework, not predefined categories

Example structure:
10-19 Life Admin
├── 11 Banking
│   ├── 11.01 Bank statements
│   └── 11.02 Account setup
├── 12 Tax
│   ├── 12.01 Tax returns
│   └── 12.02 Receipts
└── 13 Insurance
    └── 13.01 Policies

Reference: https://johnnydecimal.com/
"""

import os
import re
from typing import Dict, List, Tuple, Optional
from data_processing_common import sanitize_filename


class JohnnyDecimalOrganizer:
    """
    Johnny.Decimal system organizer implementing the official methodology.
    
    Provides the structural framework while allowing users to define their own
    areas and categories based on their specific organizational needs.
    """
    
    def __init__(self, custom_areas: Optional[Dict[int, str]] = None, 
                 custom_categories: Optional[Dict[int, str]] = None):
        """
        Initialize the organizer with optional custom areas and categories.
        
        Args:
            custom_areas: Dict of area_number -> area_name (10, 20, 30, etc.)
            custom_categories: Dict of category_number -> category_name (11, 12, etc.)
        """
        # Define default areas if none provided - these are just examples
        # Users should customize these based on their needs
        self.areas = custom_areas or {
            10: "Life Admin",      # Personal administration
            20: "Work",            # Professional activities  
            30: "Projects",        # Active projects
            40: "Resources",       # Reference materials
            50: "Archive",         # Historical/completed items
        }
        
        # Validate areas follow Johnny.Decimal rules
        self._validate_areas()
        
        # Define default categories if none provided - these are examples
        # Users should customize based on their specific area contents
        self.categories = custom_categories or self._create_default_categories()
        
    def _validate_areas(self):
        """Validate that areas follow Johnny.Decimal rules."""
        if len(self.areas) > 10:
            raise ValueError("Johnny.Decimal system allows maximum 10 areas")
        
        for area_num in self.areas.keys():
            if area_num % 10 != 0 or area_num < 10 or area_num > 90:
                raise ValueError(f"Area number {area_num} invalid. Must be 10, 20, 30, ..., 90")
    
    def _create_default_categories(self) -> Dict[int, str]:
        """Create default categories for defined areas."""
        categories = {}
        
        # Only create a few example categories, not all possible ones
        # Users should extend this based on their needs
        for area_num, area_name in self.areas.items():
            if area_num == 10:  # Life Admin
                categories.update({
                    11: "Banking",
                    12: "Tax", 
                    13: "Insurance"
                })
            elif area_num == 20:  # Work
                categories.update({
                    21: "Projects",
                    22: "Admin",
                    23: "Development"
                })
            elif area_num == 30:  # Projects  
                categories.update({
                    31: "Active",
                    32: "Planning"
                })
            elif area_num == 40:  # Resources
                categories.update({
                    41: "Documentation",
                    42: "Templates"
                })
            elif area_num == 50:  # Archive
                categories.update({
                    51: "Completed",
                    52: "Historical"
                })
        
        return categories
    
    def get_available_areas(self) -> Dict[int, str]:
        """Get all available areas."""
        return self.areas.copy()
    
    def get_categories_for_area(self, area_number: int) -> Dict[int, str]:
        """Get all categories for a specific area."""
        area_start = area_number
        area_end = area_number + 9
        return {cat_num: name for cat_num, name in self.categories.items() 
                if area_start <= cat_num <= area_end}
    
    def add_category(self, category_number: int, category_name: str):
        """Add a new category to the system."""
        area_number = (category_number // 10) * 10
        
        if area_number not in self.areas:
            raise ValueError(f"Area {area_number} not defined")
        
        if category_number < area_number or category_number > area_number + 9:
            raise ValueError(f"Category {category_number} not in valid range for area {area_number}")
        
        self.categories[category_number] = category_name

    def categorize_file_intelligently(self, file_path: str, content_description: str = "") -> Tuple[int, int, str]:
        """
        Intelligently suggest a category for a file based on content and type.
        
        Returns:
            Tuple of (area_number, category_number, category_name)
        """
        file_name = os.path.basename(file_path).lower()
        file_ext = os.path.splitext(file_path)[1].lower()
        content_lower = content_description.lower()
        
        # Simple keyword-based suggestions for common file types
        keyword_suggestions = {
            # Life Admin (10-19)
            "bank": 11, "statement": 11, "account": 11, "finance": 11,
            "tax": 12, "return": 12, "receipt": 12,
            "insurance": 13, "policy": 13, "claim": 13,
            
            # Work (20-29) 
            "project": 21, "proposal": 21, "plan": 21,
            "admin": 22, "form": 22, "process": 22,
            "code": 23, "develop": 23, "script": 23,
            
            # Projects (30-39)
            "active": 31, "current": 31, "ongoing": 31,
            "planning": 32, "idea": 32, "draft": 32,
            
            # Resources (40-49)
            "manual": 41, "guide": 41, "documentation": 41, "doc": 41,
            "template": 42, "format": 42, "example": 42,
            
            # Archive (50-59)
            "old": 51, "completed": 51, "finished": 51,
            "history": 52, "backup": 52, "archive": 52
        }
        
        # Check content and filename for keywords
        text_to_check = f"{content_lower} {file_name}"
        for keyword, suggested_category in keyword_suggestions.items():
            if keyword in text_to_check and suggested_category in self.categories:
                area = (suggested_category // 10) * 10
                return area, suggested_category, self.categories[suggested_category]
        
        # File extension based suggestions
        extension_suggestions = {
            # Documentation
            ".pdf": 41, ".doc": 41, ".docx": 41, ".txt": 41, ".md": 41,
            # Templates/Formats  
            ".xlsx": 42, ".xls": 42, ".pptx": 42, ".ppt": 42,
            # Code/Development
            ".py": 23, ".js": 23, ".html": 23, ".css": 23, ".json": 23,
            # Archives
            ".zip": 52, ".rar": 52, ".tar": 52, ".gz": 52
        }
        
        if file_ext in extension_suggestions:
            suggested_category = extension_suggestions[file_ext]
            if suggested_category in self.categories:
                area = (suggested_category // 10) * 10
                return area, suggested_category, self.categories[suggested_category]
        
        # Default to first category in first area
        first_area = min(self.areas.keys())
        area_categories = self.get_categories_for_area(first_area)
        if area_categories:
            first_category = min(area_categories.keys())
            return first_area, first_category, area_categories[first_category]
        
        # Fallback
        return 10, 11, "Uncategorized"

    def categorize_file(self, file_path: str, content_description: str = "", 
                       suggested_area: Optional[int] = None, 
                       suggested_category: Optional[int] = None) -> Tuple[int, int, str]:
        """
        Categorize a file into Johnny.Decimal system.
        
        Args:
            file_path: Path to the file
            content_description: AI-generated description of file content
            suggested_area: User-suggested area number (optional)
            suggested_category: User-suggested category number (optional)
            
        Returns:
            Tuple of (area_number, category_number, category_name)
        """
        # If user provided specific suggestions, use them
        if suggested_category and suggested_category in self.categories:
            area = (suggested_category // 10) * 10
            return area, suggested_category, self.categories[suggested_category]
        
        if suggested_area and suggested_area in self.areas:
            # Find first available category in suggested area
            area_categories = self.get_categories_for_area(suggested_area)
            if area_categories:
                first_category = min(area_categories.keys())
                return suggested_area, first_category, area_categories[first_category]
        
        # Otherwise use intelligent categorization
        return self.categorize_file_intelligently(file_path, content_description)

    def generate_johnny_decimal_path(self, file_path: str, content_description: str = "",
                                   item_counter: Dict[int, int] = None,
                                   suggested_area: Optional[int] = None,
                                   suggested_category: Optional[int] = None) -> Tuple[str, str]:
        """
        Generate Johnny.Decimal path for a file following official methodology.
        
        Args:
            file_path: Original file path
            content_description: AI-generated description of file content
            item_counter: Dictionary to track item numbers per category
            suggested_area: User-suggested area number (optional)
            suggested_category: User-suggested category number (optional)
            
        Returns:
            Tuple of (folder_path, new_filename)
        """
        if item_counter is None:
            item_counter = {}
            
        area, category, category_name = self.categorize_file(
            file_path, content_description, suggested_area, suggested_category)
        
        # Get or create item number for this category
        if category not in item_counter:
            item_counter[category] = 1
        else:
            item_counter[category] += 1
            
        # Ensure we don't exceed Johnny.Decimal limits
        if item_counter[category] > 99:
            raise ValueError(f"Category {category} has reached maximum of 99 items")
            
        item_number = f"{category}.{item_counter[category]:02d}"
        
        # Create folder structure following Johnny.Decimal methodology
        area_name = f"{area}-{area+9} {self.areas[area]}"
        category_folder = f"{category} {category_name}"
        
        folder_path = os.path.join(area_name, category_folder)
        
        # Generate filename with Johnny.Decimal number
        original_name = os.path.splitext(os.path.basename(file_path))[0]
        file_ext = os.path.splitext(file_path)[1]
        
        # Create meaningful filename based on content or original name
        if content_description:
            filename_base = sanitize_filename(content_description, max_words=3)
        else:
            filename_base = sanitize_filename(original_name, max_words=3)
            
        # Ensure we have a valid filename base
        if not filename_base or filename_base.strip() == "":
            filename_base = "item"
            
        new_filename = f"{item_number} {filename_base}{file_ext}"
        
        return folder_path, new_filename

    def print_system_overview(self):
        """Print an overview of the current Johnny.Decimal system setup."""
        print("Johnny.Decimal System Overview")
        print("=" * 40)
        print(f"Total Areas: {len(self.areas)}/10")
        print(f"Total Categories: {len(self.categories)}")
        print()
        
        for area_num in sorted(self.areas.keys()):
            area_name = self.areas[area_num]
            print(f"{area_num}-{area_num+9} {area_name}")
            
            area_categories = self.get_categories_for_area(area_num)
            for cat_num in sorted(area_categories.keys()):
                cat_name = area_categories[cat_num]
                print(f"  ├── {cat_num} {cat_name}")
                print(f"  │   └── {cat_num}.01-{cat_num}.99 (items)")
            print()


def process_files_johnny_decimal(file_paths: List[str], output_path: str, 
                                file_descriptions: Dict[str, str] = None,
                                custom_areas: Optional[Dict[int, str]] = None,
                                custom_categories: Optional[Dict[int, str]] = None,
                                dry_run: bool = False, silent: bool = False, 
                                log_file: str = None) -> List[Dict]:
    """
    Process files using Johnny.Decimal organization system.
    
    Args:
        file_paths: List of file paths to organize
        output_path: Base output directory
        file_descriptions: Optional dictionary of file_path -> description
        custom_areas: Optional custom area definitions
        custom_categories: Optional custom category definitions
        dry_run: If True, don't actually move files
        silent: If True, suppress output
        log_file: Optional log file path
        
    Returns:
        List of operation dictionaries
    """
    organizer = JohnnyDecimalOrganizer(custom_areas, custom_categories)
    operations = []
    item_counters = {}  # Track item numbers per category
    
    if file_descriptions is None:
        file_descriptions = {}
    
    # Print system overview if not in silent mode
    if not silent:
        print("\n" + "="*60)
        print("JOHNNY.DECIMAL SYSTEM ORGANIZATION")
        print("="*60)
        organizer.print_system_overview()
        print("Processing files...")
        print("="*60)
    
    for file_path in file_paths:
        # Skip hidden files
        if os.path.basename(file_path).startswith('.'):
            continue
            
        # Get content description if available
        content_description = file_descriptions.get(file_path, "")
        
        # Generate Johnny.Decimal path
        try:
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
                message = f"J.D: {os.path.basename(file_path)} → {folder_path}/{new_filename}"
                if log_file:
                    with open(log_file, 'a') as f:
                        f.write(message + '\n')
                else:
                    print(message)
                    
        except ValueError as e:
            error_msg = f"Error processing {file_path}: {e}"
            if not silent:
                print(f"WARNING: {error_msg}")
            if log_file:
                with open(log_file, 'a') as f:
                    f.write(f"ERROR: {error_msg}\n")
    
    if not silent:
        print("="*60)
        print(f"Johnny.Decimal organization complete. {len(operations)} files processed.")
        print("="*60)
    
    return operations