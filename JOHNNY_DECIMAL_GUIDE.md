# Johnny.Decimal System Guide

## Overview

The Johnny.Decimal system is a file organization methodology that uses a hierarchical numbering system to create structured, logical folder hierarchies. This implementation provides an optional organization mode in the Local File Organizer.

## How It Works

### Structure Levels

1. **Areas (10-19, 20-29, etc.)**
   - Broad, top-level categories
   - Each area covers 10 numbers (e.g., 10-19, 20-29)
   - Maximum of 10 areas per system

2. **Categories (11, 12, 13, etc.)**
   - Subcategories within each area
   - Two-digit numbers within each area range
   - Maximum of 10 categories per area

3. **Items (11.01, 11.02, etc.)**
   - Individual files or documents
   - Decimal notation with category prefix
   - Maximum of 100 items per category

### Predefined Areas

This implementation includes 9 predefined areas:

- **10-19 Personal Management**: Finance, Health, Education, Legal, Travel
- **20-29 Professional Work**: Projects, Reports, Presentations, Contracts
- **30-39 Creative Projects**: Photography, Writing, Design, Music, Video, Art
- **40-49 Reference Materials**: Documentation, Manuals, Research, Books
- **50-59 Media Collection**: Images, Audio, Video, Graphics
- **60-69 Technical Resources**: Code, Configurations, Databases, Software
- **70-79 Communication**: Emails, Messages, Social Media, Correspondence
- **80-89 Archives**: Old Projects, Backups, Historical Data
- **90-99 Miscellaneous**: Temporary, Downloads, Uncategorized

## Automatic Categorization

The system automatically categorizes files based on:

1. **Content Analysis**: AI-generated descriptions when available
2. **File Extensions**: Common file types mapped to appropriate categories
3. **Filename Keywords**: Recognizable terms in filenames
4. **Fallback Rules**: Default categories for unrecognized content

### Example Categorizations

| File Type | Example | Suggested Category |
|-----------|---------|-------------------|
| Bank statement | `bank_statement.pdf` | 11 Finance |
| Medical record | `health_report.pdf` | 12 Health |
| Photo | `vacation_photo.jpg` | 51 Images or 15 Travel |
| Code file | `script.py` | 61 Code |
| Presentation | `project.pptx` | 23 Presentations |

## Usage in Local File Organizer

1. Run the Local File Organizer application
2. Select mode **4. By Johnny.Decimal System**
3. The system will:
   - Analyze your files
   - Assign appropriate Johnny.Decimal numbers
   - Create the hierarchical folder structure
   - Generate meaningful filenames with numbers

## Benefits

- **Consistent Structure**: Every file has a logical place
- **Easy Navigation**: Hierarchical numbering makes finding files intuitive
- **Scalable**: System grows logically as you add more files
- **Cross-Platform**: Works on any operating system
- **Future-Proof**: Numbers don't change, maintaining organization over time

## Customization

The system can be customized by modifying the `johnny_decimal_processing.py` file:

- Add new areas or categories
- Modify keyword mappings
- Adjust file extension associations
- Change automatic categorization rules

## Best Practices

1. **Consistency**: Always use the same numbering system
2. **Meaningful Names**: Combine numbers with descriptive names
3. **Regular Review**: Periodically review and reorganize if needed
4. **Documentation**: Keep a reference of your area/category assignments
5. **Backup**: Always backup your organized files

For more information about the Johnny.Decimal system concept, visit: https://johnnydecimal.com/