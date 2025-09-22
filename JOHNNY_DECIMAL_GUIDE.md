# Johnny.Decimal System Guide

## Overview

The Johnny.Decimal system is a file organization methodology that provides a **framework** for organizing information using a structured hierarchical numbering system. The key insight is that it's not about predefined categories, but about giving users a systematic way to organize their own information.

## Core Principles

### 1. **Everything has a number**
Every item in your system gets a unique Johnny.Decimal number that tells you exactly where it belongs.

### 2. **Everything has one place**
Nothing belongs in multiple places. Each item has exactly one correct location.

### 3. **Numbers never change**
Once you assign a number, it never changes. This creates stability and prevents organizational drift.

### 4. **Three levels maximum**
The system has exactly three levels - no more, no less:
- **Areas** (10-19, 20-29, etc.)
- **Categories** (11, 12, 13, etc.)
- **Items** (11.01, 11.02, etc.)

### 5. **Strict limits**
- Maximum 10 areas (10-19, 20-29, 30-39, 40-49, 50-59, 60-69, 70-79, 80-89, 90-99)
- Maximum 10 categories per area (11-19, 21-29, 31-39, etc.)
- Maximum 100 items per category (11.01-11.99, 12.01-12.99, etc.)

## How It Works

### Structure Levels

1. **Areas (10-19, 20-29, etc.)**
   - Broad, top-level categories that represent major areas of your life/work
   - Each area covers exactly 10 numbers
   - You define what each area represents based on YOUR needs

2. **Categories (11, 12, 13, etc.)**
   - Subcategories within each area
   - Two-digit numbers within each area range
   - You define what each category represents

3. **Items (11.01, 11.02, etc.)**
   - Individual files, documents, or things
   - Decimal notation with category prefix
   - These are your actual files and documents

### Example Structure (User-Defined)

Here's how someone might organize their personal system:

```
10-19 Life Admin
├── 11 Banking
│   ├── 11.01 Bank statements
│   ├── 11.02 Account setup documents
│   └── 11.03 Investment records
├── 12 Tax
│   ├── 12.01 Tax returns
│   ├── 12.02 Receipts
│   └── 12.03 Tax planning documents
└── 13 Insurance
    ├── 13.01 Car insurance
    ├── 13.02 Health insurance
    └── 13.03 Home insurance

20-29 Work
├── 21 Current Projects
│   ├── 21.01 Project Alpha documents
│   ├── 21.02 Project Beta files
│   └── 21.03 Project Gamma resources
├── 22 Administration
│   ├── 22.01 Timesheets
│   ├── 22.02 Expense reports
│   └── 22.03 HR documents
└── 23 Development
    ├── 23.01 Code repositories
    ├── 23.02 Technical documentation
    └── 23.03 Development tools
```

## Key Differences from Traditional Systems

### User-Defined Structure
Unlike other filing systems, Johnny.Decimal doesn't tell you what your categories should be. YOU decide:
- What your areas represent
- What categories go in each area
- How to organize your specific content

### Methodology Over Content
The system provides the **method** (the numbering structure and rules), not the **content** (specific categories for different types of files).

### Scalable but Limited
The limits (10 areas, 10 categories per area, 100 items per category) force you to think clearly about organization while providing room to grow.

## Usage in Local File Organizer

### Automatic Suggestions
The Local File Organizer implementation:
1. Provides a **default example structure** to get you started
2. Makes **intelligent suggestions** based on file content and types
3. Allows you to **customize** areas and categories for your needs
4. Follows **strict Johnny.Decimal rules** to maintain system integrity

### Customization
You can modify the areas and categories to match your specific needs:
- Change area names to reflect your life/work domains
- Add categories within areas as needed
- Let the system suggest placements based on file analysis

### Example Output Structure
```
organized_folder/
├── 10-19 Life Admin/
│   ├── 11 Banking/
│   │   ├── 11.01 bank_statement_december.pdf
│   │   └── 11.02 investment_portfolio.pdf
│   └── 12 Tax/
│       ├── 12.01 tax_return_2024.pdf
│       └── 12.02 receipts_business.pdf
├── 20-29 Work/
│   └── 21 Current Projects/
│       ├── 21.01 project_proposal.docx
│       └── 21.02 meeting_notes.txt
└── 40-49 Resources/
    └── 41 Documentation/
        ├── 41.01 system_manual.pdf
        └── 41.02 user_guide.pdf
```

## Benefits

### Mental Clarity
- Forces you to think about information architecture
- Prevents endless sub-folder hierarchies
- Creates clear boundaries and decisions

### Practical Organization
- Easy to remember where things are
- Quick to find specific items by number
- Scales without becoming unwieldy

### Long-term Stability
- Numbers don't change, so your system doesn't drift
- Works across different computer systems and platforms
- Future-proof organizational method

## Best Practices

### Starting Out
1. **Begin with broad areas** that represent major domains of your life/work
2. **Add categories gradually** as you identify natural groupings
3. **Don't pre-fill everything** - let categories emerge organically
4. **Use descriptive names** for areas and categories that make sense to you

### Maintaining the System
1. **Stick to the limits** - if you need more than 10 categories in an area, consider splitting the area
2. **Be consistent** with naming conventions
3. **Document your decisions** so you remember why you organized things a certain way
4. **Review periodically** but resist the urge to constantly reorganize

### Common Mistakes to Avoid
1. **Don't create deep hierarchies** - stick to exactly three levels
2. **Don't duplicate items** - everything has exactly one place
3. **Don't change numbers** once assigned
4. **Don't overthink it** - start simple and evolve

For more information about the official Johnny.Decimal methodology, visit: https://johnnydecimal.com/