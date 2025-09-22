"""
Johnny.Decimal System Implementation - Alternative Layout 1

Based on the Alternative Layout 1 proposal from:
https://forum.johnnydecimal.com/t/the-standard-zeros/1558/12

This implementation uses the alternative layout for standard zeros where:
- System area (00-09) contains system management and area management
- Area zeros (A0) are moved into categories 01-09 in the system area  
- No skipping of AC.10 IDs (uses .10-.99 instead of .11-.99)
- Provides 9 more categories and 891 more usable IDs (12.36% increase)

Key changes from the standard layout:
- Meta areas: 0 (system area only)
- Meta categories: 01-09 (area management)
- Meta IDs: .00-09 (system management)
- Usable areas: 10-90 (9 areas instead of 10)
- Usable categories: A0-A9 (instead of A1-A9)
- Usable IDs: .10-99 (instead of .11-99)

Core Principles (unchanged):
- Areas (10-19, 20-29, etc.): Broad areas of your life (max 9)
- Categories (10, 11, 12, etc.): Collections of similar things (max 10 per area)  
- IDs (10.10, 10.11, etc.): Individual items/projects (max 90 per category)
- The JDex (index): Central record of every ID - this IS your system
- Numbers never change once assigned
- Everything has exactly one place
- Limit choices to reduce decision fatigue

The goal: Find things quickly, with confidence, and less stress.

Official site: https://johnnydecimal.com/
Alt. 1 proposal: https://forum.johnnydecimal.com/t/the-standard-zeros/1558/12
"""

import os
import re
from typing import Dict, List, Tuple, Optional
from data_processing_common import sanitize_filename


class JohnnyDecimalOrganizer:
    """
    Johnny.Decimal system organizer implementing the Alternative Layout 1 proposal.
    
    This implementation uses the alternative layout for standard zeros where:
    - System area (00-09) contains system management and area management
    - Area zeros (A0) are moved into categories 01-09 in the system area
    - No skipping of AC.10 IDs (uses .10-.99 instead of .11-.99)
    - Provides 9 more categories and 891 more usable IDs
    
    Based on: https://forum.johnnydecimal.com/t/the-standard-zeros/1558/12
    """
    
    def __init__(self, custom_areas: Optional[Dict[int, str]] = None, 
                 custom_categories: Optional[Dict[int, str]] = None):
        """
        Initialize with Alternative Layout 1 structure.
        
        Args:
            custom_areas: Dict of area_number -> area_name (10, 20, 30, etc.)
            custom_categories: Dict of category_number -> category_name
        """
        # System area (00-09) with system and area management
        self.system_area = 0
        
        # Start with minimal example areas - users should customize these
        self.areas = custom_areas or {
            10: "Life admin",      # The stuff we all manage day-to-day
            20: "Work",            # Professional activities  
            30: "Projects",        # Active projects and interests
        }
        
        # Validate areas follow Johnny.Decimal rules
        self._validate_areas()
        
        # Alternative Layout 1: categories include system management and area management
        self.categories = custom_categories or {
            # System area (00-09) management categories
            0: "System management",    # System-wide management (replaces 00)
            1: "Life admin management", # Management for area 10-19 (replaces A0 pattern)
            2: "Work management",      # Management for area 20-29
            3: "Projects management",  # Management for area 30-39
            
            # Life admin (10-19) - now uses A0-A9 instead of A1-A9
            10: "Me",              # Personal documents, health, etc.
            11: "House",           # Home-related stuff
            12: "Money",           # Financial matters
            13: "Online",          # Digital accounts, subscriptions
            14: "Travel",          # Trips and travel documents
            15: "Health",          # Health records, fitness
            
            # Work (20-29) - now uses A0-A9 
            20: "Current work",    # Active work projects
            21: "Admin",           # Work administration
            22: "Clients",         # Client management
            
            # Projects (30-39) - now uses A0-A9
            30: "Active",          # Current personal projects
            31: "Learning",        # Educational projects
        }
        
        # Track IDs to prevent duplicates (like a simple JDex)
        self.assigned_ids = set()
        
    def _validate_areas(self):
        """Validate that areas follow Johnny.Decimal rules for Alt. 1 layout."""
        if len(self.areas) > 9:  # Alt. 1 allows 9 usable areas (10-90)
            raise ValueError("Alternative Layout 1 allows maximum 9 areas (10-90)")
        
        for area_num in self.areas.keys():
            if area_num % 10 != 0 or area_num < 10 or area_num > 90:
                raise ValueError(f"Area number {area_num} invalid. Must be 10, 20, 30, ..., 90")
    
    def get_available_areas(self) -> Dict[int, str]:
        """Get all available usable areas (excludes system area 00-09)."""
        return self.areas.copy()
    
    def get_system_categories(self) -> Dict[int, str]:
        """Get system area management categories (00-09)."""
        return {cat_num: name for cat_num, name in self.categories.items() 
                if 0 <= cat_num <= 9}
    
    def get_categories_for_area(self, area_number: int) -> Dict[int, str]:
        """Get all categories for a specific area (A0-A9 instead of A1-A9)."""
        if area_number == 0:
            return self.get_system_categories()
        
        area_start = area_number
        area_end = area_number + 9
        return {cat_num: name for cat_num, name in self.categories.items() 
                if area_start <= cat_num <= area_end}
    
    def get_area_management_category(self, area_number: int) -> Optional[int]:
        """Get the management category for a specific area in the system area."""
        if area_number < 10 or area_number > 90 or area_number % 10 != 0:
            return None
        
        # Area 10-19 -> category 1, Area 20-29 -> category 2, etc.
        management_category = area_number // 10
        if management_category in self.categories:
            return management_category
        return None
    
    def add_category(self, category_number: int, category_name: str):
        """Add a new category to the system."""
        if 0 <= category_number <= 9:
            # System area category (including area management)
            self.categories[category_number] = category_name
        else:
            # Regular area category
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
            # Life admin suggestions (area 10-19, now using A0-A9)
            "bank": 12, "money": 12, "finance": 12, "tax": 12, "insurance": 12,
            "health": 15, "medical": 15, "fitness": 15, "doctor": 15,
            "passport": 10, "personal": 10, "identity": 10,
            "house": 11, "home": 11, "utilities": 11, "mortgage": 11,
            "travel": 14, "trip": 14, "vacation": 14, "flight": 14, "hotel": 14,
            "subscription": 13, "account": 13, "login": 13, "online": 13,
            
            # Work suggestions (area 20-29, now using A0-A9)
            "work": 20, "project": 20, "client": 22, "meeting": 21, "admin": 21,
            
            # Personal projects (area 30-39, now using A0-A9)
            "hobby": 30, "learning": 31, "creative": 30, "side": 30,
        }
        
        # Check content and filename for keywords
        text_to_check = f"{content_lower} {file_name}"
        for keyword, suggested_category in suggestions.items():
            if keyword in text_to_check and suggested_category in self.categories:
                area = (suggested_category // 10) * 10 if suggested_category >= 10 else 0
                return area, suggested_category, self.categories[suggested_category]
        
        # Default to first available category in first area
        if self.categories:
            regular_categories = {k: v for k, v in self.categories.items() if k >= 10}
            if regular_categories:
                first_category = min(regular_categories.keys())
                area = (first_category // 10) * 10
                return area, first_category, regular_categories[first_category]
        
        # Ultimate fallback
        return 10, 10, "Me"

    def get_next_available_id(self, category: int) -> str:
        """
        Get the next available ID in a category.
        Alt. 1: Uses .10-.99 (no skipping of AC.10 IDs)
        
        In a real system, this would consult the JDex.
        """
        # Alt. 1: Start from 10 instead of 11 (no skipping AC.10)
        min_id = 10
        
        # For system categories (0-9), we can use .00-.09 for standard zeros
        if 0 <= category <= 9:
            min_id = 0
        
        # Find highest existing ID in this category
        max_id = min_id - 1
        for assigned_id in self.assigned_ids:
            if assigned_id.startswith(f"{category}."):
                try:
                    id_num = int(assigned_id.split('.')[1])
                    max_id = max(max_id, id_num)
                except (ValueError, IndexError):
                    continue
        
        next_id = max_id + 1
        
        # Validate ID ranges
        if 0 <= category <= 9:
            # System categories can use .00-.99
            if next_id > 99:
                raise ValueError(f"System category {category} has reached maximum of 99 items")
        else:
            # Regular categories use .10-.99 (Alt. 1: no skipping)
            if next_id < 10:
                next_id = 10
            if next_id > 99:
                raise ValueError(f"Category {category} has reached maximum of 90 items (.10-.99)")
        
        return f"{category}.{next_id:02d}"

    def assign_id(self, file_path: str, content_description: str = "",
                  suggested_category: Optional[int] = None) -> Tuple[str, str, str]:
        """
        Assign a Johnny.Decimal ID to a file using Alt. 1 layout.
        
        In the official system, you would:
        1. Open your JDex (index) in your notes app
        2. Find the right category
        3. Create a new note with the next ID
        4. Then create the file/folder
        
        Returns: (id, folder_path, description)
        """
        if suggested_category is not None and suggested_category in self.categories:
            category = suggested_category
            if category >= 10:
                area = (category // 10) * 10
            else:
                area = 0  # System area
            category_name = self.categories[category]
        else:
            area, category, category_name = self.suggest_categorization(file_path, content_description)
        
        # Get next available ID
        new_id = self.get_next_available_id(category)
        self.assigned_ids.add(new_id)
        
        # Create folder structure following Alt. 1 methodology
        if area == 0:
            # System area
            area_name = f"00-09 System"
            category_folder = f"{category:02d} {category_name}"
        else:
            # Regular areas
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
        """Print an overview of the Alternative Layout 1 Johnny.Decimal system setup."""
        print("Johnny.Decimal System Overview - Alternative Layout 1")
        print("=" * 50)
        print("Goal: Find things quickly, with confidence, and less stress")
        print()
        print("Alternative Layout 1 Features:")
        print("• Area management moved to system area (00-09)")
        print("• Categories use A0-A9 (instead of A1-A9)")
        print("• IDs use .10-.99 (no skipping of AC.10)")
        print("• Provides 9 more categories and 891 more IDs")
        print()
        print(f"System area: 00-09 (management categories)")
        print(f"Usable areas: {len(self.areas)}/9 (broad areas of your life)")
        print(f"Categories: {len(self.categories)} (collections of similar things)")  
        print(f"Assigned IDs: {len(self.assigned_ids)} (individual items)")
        print()
        print("Structure:")
        
        # Show system area first
        print("00-09 System")
        system_categories = self.get_system_categories()
        for cat_num in sorted(system_categories.keys()):
            cat_name = system_categories[cat_num]
            print(f"  ├── {cat_num:02d} {cat_name}")
            
            # Show assigned IDs in this category
            category_ids = [id for id in self.assigned_ids if id.startswith(f"{cat_num}.")]
            if category_ids:
                for assigned_id in sorted(category_ids):
                    print(f"  │   ├── {assigned_id}")
            else:
                print(f"  │   └── (No IDs assigned yet)")
        print()
        
        # Show regular areas
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
        
        print("Alternative Layout 1 Benefits:")
        print("• 9 more categories available for use")
        print("• 891 more IDs available (12.36% increase)")
        print("• No wasted AC.10 IDs")
        print("• Cleaner area management in system area")
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
    Process files using Johnny.Decimal Alternative Layout 1 methodology.
    
    This implementation uses the alternative layout for standard zeros where:
    - System area (00-09) contains system and area management
    - Area zeros moved to categories 01-09 in system area  
    - No skipping of AC.10 IDs (uses .10-.99 instead of .11-.99)
    - Provides 9 more categories and 891 more usable IDs
    
    Note: In the real Johnny.Decimal system, you would:
    1. First create entries in your JDex (notes app)
    2. Then create the file/folder structure
    
    This implementation focuses on the file organization aspect.
    
    Based on: https://forum.johnnydecimal.com/t/the-standard-zeros/1558/12
    """
    organizer = JohnnyDecimalOrganizer(custom_areas, custom_categories)
    operations = []
    
    if file_descriptions is None:
        file_descriptions = {}
    
    # Print system overview if not in silent mode
    if not silent:
        print("\n" + "="*70)
        print("JOHNNY.DECIMAL FILE ORGANIZATION - ALTERNATIVE LAYOUT 1")
        print("Based on Alt. 1 proposal from forum.johnnydecimal.com")
        print("="*70)
        organizer.print_system_overview()
        print("\nProcessing files...")
        print("Note: In a real Johnny.Decimal system, you would create")
        print("these IDs in your JDex (notes app) first, then organize files.")
        print("="*70)
    
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
        print("="*70)
        print(f"Johnny.Decimal Alternative Layout 1 organization complete!")
        print(f"Processed {len(operations)} files into the enhanced structure.")
        print()
        print("ALTERNATIVE LAYOUT 1 BENEFITS:")
        print("• 9 more categories available for use")
        print("• 891 more IDs available (12.36% increase)")
        print("• No wasted AC.10 IDs")
        print("• Cleaner area management in system area")
        print()
        print("NEXT STEPS:")
        print("1. Create a JDex (index) in your notes app (Bear, Obsidian, etc.)")
        print("2. Add an entry for each ID to track locations across your digital life")
        print("3. The JDex becomes your system's memory and search interface")
        print("="*70)
    
    return operations