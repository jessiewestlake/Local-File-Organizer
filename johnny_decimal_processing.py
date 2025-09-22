"""
Johnny.Decimal System Implementation for Local File Organizer

Based on the official Johnny.Decimal methodology from https://johnnydecimal.com/

The Johnny.Decimal system is designed to help you find things quickly, 
with more confidence, and less stress. It's not just about files - it's 
about organizing everything in your life.

Core Principles:
- Areas (10-19, 20-29, etc.): Broad areas of your life (max 10)
- Categories (11, 12, 13, etc.): Collections of similar things (max 10 per area)  
- IDs (11.01, 11.02, etc.): Individual items/projects (max 100 per category)
- The JDex (index): Central record of every ID - this IS your system
- Numbers never change once assigned
- Everything has exactly one place
- Limit choices to reduce decision fatigue

The goal: Find things quickly, with confidence, and less stress.

Official site: https://johnnydecimal.com/
"""

import os
import re
from typing import Dict, List, Tuple, Optional
from data_processing_common import sanitize_filename


class JohnnyDecimalOrganizer:
    """
    Johnny.Decimal system organizer implementing the official methodology.
    
    This system helps you organize your entire life, not just files.
    The index (JDex) is the central component that makes everything work.
    """
    
    def __init__(self, custom_areas: Optional[Dict[int, str]] = None, 
                 custom_categories: Optional[Dict[int, str]] = None):
        """
        Initialize with minimal example structure that users should customize.
        
        Args:
            custom_areas: Dict of area_number -> area_name (10, 20, 30, etc.)
            custom_categories: Dict of category_number -> category_name (11, 12, etc.)
        """
        # Start with minimal example areas - users should customize these
        self.areas = custom_areas or {
            10: "Life admin",      # The stuff we all manage day-to-day
            20: "Work",            # Professional activities  
            30: "Projects",        # Active projects and interests
        }
        
        # Validate areas follow Johnny.Decimal rules
        self._validate_areas()
        
        # Minimal example categories - users should add their own
        self.categories = custom_categories or {
            # Life admin (10-19)
            11: "Me",              # Personal documents, health, etc.
            12: "House",           # Home-related stuff
            13: "Money",           # Financial matters
            14: "Online",          # Digital accounts, subscriptions
            15: "Travel",          # Trips and travel documents
            
            # Work (20-29) 
            21: "Current work",    # Active work projects
            22: "Admin",           # Work administration
            
            # Projects (30-39)
            31: "Active",          # Current personal projects
        }
        
        # Track IDs to prevent duplicates (like a simple JDex)
        self.assigned_ids = set()
        
    def _validate_areas(self):
        """Validate that areas follow Johnny.Decimal rules."""
        if len(self.areas) > 10:
            raise ValueError("Johnny.Decimal system allows maximum 10 areas")
        
        for area_num in self.areas.keys():
            if area_num % 10 != 0 or area_num < 10 or area_num > 90:
                raise ValueError(f"Area number {area_num} invalid. Must be 10, 20, 30, ..., 90")
    
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

    def suggest_categorization(self, file_path: str, content_description: str = "") -> Tuple[int, int, str]:
        """
        Suggest categorization based on content, but user should decide.
        
        This follows the Johnny.Decimal philosophy that categorization requires
        thought and consideration - automation shouldn't make all the decisions.
        """
        file_name = os.path.basename(file_path).lower()
        file_ext = os.path.splitext(file_path)[1].lower()
        content_lower = content_description.lower()
        
        # Simple suggestions based on common patterns
        suggestions = {
            # Life admin suggestions
            "bank": 13, "money": 13, "finance": 13, "tax": 13, "insurance": 13,
            "health": 11, "medical": 11, "passport": 11, "personal": 11,
            "house": 12, "home": 12, "utilities": 12, "mortgage": 12,
            "travel": 15, "trip": 15, "vacation": 15, "flight": 15, "hotel": 15,
            "subscription": 14, "account": 14, "login": 14, "online": 14,
            
            # Work suggestions
            "work": 21, "project": 21, "meeting": 22, "admin": 22,
            
            # Personal projects
            "hobby": 31, "learning": 31, "creative": 31, "side": 31,
        }
        
        # Check content and filename for keywords
        text_to_check = f"{content_lower} {file_name}"
        for keyword, suggested_category in suggestions.items():
            if keyword in text_to_check and suggested_category in self.categories:
                area = (suggested_category // 10) * 10
                return area, suggested_category, self.categories[suggested_category]
        
        # Default to first available category
        if self.categories:
            first_category = min(self.categories.keys())
            area = (first_category // 10) * 10
            return area, first_category, self.categories[first_category]
        
        # Ultimate fallback
        return 10, 11, "Me"

    def get_next_available_id(self, category: int) -> str:
        """
        Get the next available ID in a category.
        In a real system, this would consult the JDex.
        """
        # Find highest existing ID in this category
        max_id = 0
        for assigned_id in self.assigned_ids:
            if assigned_id.startswith(f"{category}."):
                try:
                    id_num = int(assigned_id.split('.')[1])
                    max_id = max(max_id, id_num)
                except (ValueError, IndexError):
                    continue
        
        next_id = max_id + 1
        if next_id > 99:
            raise ValueError(f"Category {category} has reached maximum of 99 items")
        
        return f"{category}.{next_id:02d}"

    def assign_id(self, file_path: str, content_description: str = "",
                  suggested_category: Optional[int] = None) -> Tuple[str, str, str]:
        """
        Assign a Johnny.Decimal ID to a file.
        
        In the official system, you would:
        1. Open your JDex (index) in your notes app
        2. Find the right category
        3. Create a new note with the next ID
        4. Then create the file/folder
        
        Returns: (id, folder_path, description)
        """
        if suggested_category and suggested_category in self.categories:
            category = suggested_category
            area = (category // 10) * 10
            category_name = self.categories[category]
        else:
            area, category, category_name = self.suggest_categorization(file_path, content_description)
        
        # Get next available ID
        new_id = self.get_next_available_id(category)
        self.assigned_ids.add(new_id)
        
        # Create folder structure following official methodology
        area_name = f"{area}-{area+9} {self.areas[area]}"
        category_folder = f"{category} {category_name}"
        folder_path = os.path.join(area_name, category_folder)
        
        # Create meaningful description
        if content_description:
            description = sanitize_filename(content_description, max_words=4)
        else:
            original_name = os.path.splitext(os.path.basename(file_path))[0]
            description = sanitize_filename(original_name, max_words=4)
        
        if not description:
            description = "item"
            
        return new_id, folder_path, description

    def generate_jdex_entry(self, id: str, description: str, file_path: str) -> Dict[str, str]:
        """
        Generate a JDex (index) entry for this ID.
        
        In the official system, this would be a note in Bear, Obsidian, etc.
        The JDex IS your Johnny.Decimal system.
        """
        return {
            'id': id,
            'title': f"{id} {description}",
            'location': f"File system: {file_path}",
            'description': description,
            'created': 'Today',  # In real system, would be actual date
            'notes': 'Add any additional notes about this item here.'
        }

    def print_system_overview(self):
        """Print an overview of the current Johnny.Decimal system setup."""
        print("Johnny.Decimal System Overview")
        print("=" * 40)
        print("Goal: Find things quickly, with confidence, and less stress")
        print()
        print(f"Areas: {len(self.areas)}/10 (broad areas of your life)")
        print(f"Categories: {len(self.categories)} (collections of similar things)")  
        print(f"Assigned IDs: {len(self.assigned_ids)} (individual items)")
        print()
        print("Structure:")
        
        for area_num in sorted(self.areas.keys()):
            area_name = self.areas[area_num]
            print(f"{area_num}-{area_num+9} {area_name}")
            
            area_categories = self.get_categories_for_area(area_num)
            for cat_num in sorted(area_categories.keys()):
                cat_name = area_categories[cat_num]
                print(f"  ├── {cat_num} {cat_name}")
                
                # Show assigned IDs in this category
                category_ids = [id for id in self.assigned_ids if id.startswith(f"{cat_num}.")]
                if category_ids:
                    for assigned_id in sorted(category_ids):
                        print(f"  │   ├── {assigned_id}")
                else:
                    print(f"  │   └── (No IDs assigned yet)")
            print()
        
        print("Remember: The JDex (index) in your notes app is the central")
        print("record of your system. It tracks where everything is across")
        print("your entire digital life - files, emails, notes, everything!")


def process_files_johnny_decimal(file_paths: List[str], output_path: str, 
                                file_descriptions: Dict[str, str] = None,
                                custom_areas: Optional[Dict[int, str]] = None,
                                custom_categories: Optional[Dict[int, str]] = None,
                                dry_run: bool = False, silent: bool = False, 
                                log_file: str = None) -> List[Dict]:
    """
    Process files using official Johnny.Decimal methodology.
    
    Note: In the real Johnny.Decimal system, you would:
    1. First create entries in your JDex (notes app)
    2. Then create the file/folder structure
    
    This implementation focuses on the file organization aspect.
    """
    organizer = JohnnyDecimalOrganizer(custom_areas, custom_categories)
    operations = []
    
    if file_descriptions is None:
        file_descriptions = {}
    
    # Print system overview if not in silent mode
    if not silent:
        print("\n" + "="*60)
        print("JOHNNY.DECIMAL FILE ORGANIZATION")
        print("Based on the official methodology from johnnydecimal.com")
        print("="*60)
        organizer.print_system_overview()
        print("\nProcessing files...")
        print("Note: In a real Johnny.Decimal system, you would create")
        print("these IDs in your JDex (notes app) first, then organize files.")
        print("="*60)
    
    for file_path in file_paths:
        # Skip hidden files
        if os.path.basename(file_path).startswith('.'):
            continue
            
        # Get content description if available
        content_description = file_descriptions.get(file_path, "")
        
        try:
            # Assign Johnny.Decimal ID
            jd_id, folder_path, description = organizer.assign_id(file_path, content_description)
            
            # Create filename with proper Johnny.Decimal format
            file_ext = os.path.splitext(file_path)[1]
            new_filename = f"{jd_id} {description}{file_ext}"
            
            # Create full destination path
            full_folder_path = os.path.join(output_path, folder_path)
            destination_path = os.path.join(full_folder_path, new_filename)
            
            # Generate JDex entry for reference
            jdex_entry = organizer.generate_jdex_entry(jd_id, description, destination_path)
            
            # Create operation record
            operation = {
                'source': file_path,
                'destination': destination_path,
                'link_type': 'hardlink',
                'folder_name': folder_path,
                'new_file_name': new_filename,
                'jd_id': jd_id,
                'jdex_entry': jdex_entry
            }
            
            operations.append(operation)
            
            # Log operation if not silent
            if not silent:
                message = f"J.D: {os.path.basename(file_path)} → {jd_id} {description}"
                if log_file:
                    with open(log_file, 'a') as f:
                        f.write(message + '\n')
                        f.write(f"JDex: {jdex_entry['title']}\n")
                        f.write(f"Location: {jdex_entry['location']}\n\n")
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
        print(f"Johnny.Decimal file organization complete!")
        print(f"Processed {len(operations)} files into Johnny.Decimal structure.")
        print()
        print("NEXT STEPS:")
        print("1. Create a JDex (index) in your notes app (Bear, Obsidian, etc.)")
        print("2. Add an entry for each ID to track locations across your digital life")
        print("3. The JDex becomes your system's memory and search interface")
        print("="*60)
    
    return operations