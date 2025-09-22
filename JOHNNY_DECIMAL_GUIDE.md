# Johnny.Decimal System Guide - Alternative Layout 1

## Overview

This implementation uses the **Alternative Layout 1** for the Johnny.Decimal system's standard zeros, as proposed in the official forum. The Johnny.Decimal system is designed to help you **find things quickly, with more confidence, and less stress**. It's not just about organizing files - it's about organizing everything in your life.

Based on the Alternative Layout 1 proposal from: https://forum.johnnydecimal.com/t/the-standard-zeros/1558/12

## Alternative Layout 1 Changes

This implementation differs from the standard Johnny.Decimal layout by implementing the **Alternative Layout 1 proposal**, which provides significant improvements:

### Key Changes
- **System area (00-09)**: Contains both system management (00) and area management (01-09)
- **Area management**: Moved from A0 categories to 01-09 in the system area
- **Category numbering**: Uses A0-A9 instead of A1-A9 for regular categories
- **ID numbering**: Uses .10-.99 instead of .11-.99 (no skipping of AC.10)

### Benefits
- **9 more categories** available for use
- **891 more IDs** available (12.36% increase in capacity)
- **No wasted AC.10 IDs** 
- **Cleaner area management** consolidated in system area

## Core Philosophy

**"A system to organise your life"**

The Johnny.Decimal system helps you organize:
- Computer files and folders
- Email and messages  
- Notes and documents
- Physical items
- Digital accounts and subscriptions
- Anything that needs organizing

The goal is always the same: **find things quickly, with confidence, and less stress**.

## How Alternative Layout 1 Works

### The Three Levels

Johnny.Decimal has exactly three levels of organization:

1. **System Area (00-09)** - NEW in Alt. 1
   - Contains system management (00) and area management (01-09)
   - Category 01 manages area 10-19, category 02 manages 20-29, etc.

2. **Areas (10-19, 20-29, etc.)**
   - Broad areas of your life
   - Maximum 9 areas total (instead of 10)
   - Think "life admin", "work", "hobbies"

3. **Categories (10, 11, 12, etc.)** - CHANGED in Alt. 1
   - Collections of similar things within each area
   - Now uses A0-A9 pattern instead of A1-A9
   - Maximum 10 categories per area
   - This is where you work - categories are the most important concept

4. **IDs (10.10, 10.11, etc.)** - CHANGED in Alt. 1
   - Individual items, projects, or things
   - Now uses .10-.99 instead of .11-.99 (no skipping AC.10)
   - Maximum 90 items per regular category (.10-.99)
   - System categories can use .00-.99 (100 items)

### Example Structure (Alternative Layout 1)

```
00-09 System
├── 00 System management
│   ├── 00.00 System index
│   ├── 00.01 System inbox
│   └── 00.02 System work in progress
├── 01 Life admin management  
│   ├── 01.00 Life admin index
│   ├── 01.01 Life admin inbox
│   └── 01.02 Life admin work in progress
├── 02 Work management
│   └── 02.01 Work inbox
└── 03 Projects management
    └── 03.01 Projects inbox

10-19 Life admin
├── 10 Me                    [Note: A0 instead of A1]
│   ├── 10.10 Passport renewal     [Note: .10 instead of .11]
│   ├── 10.11 Health insurance
│   └── 10.12 Gym membership
├── 11 House                 [Note: A1 instead of A2]
│   ├── 11.10 Mortgage documents
│   ├── 11.11 Utilities setup
│   └── 11.12 Home insurance
└── 14 Travel               [Note: A4 instead of A5]
    ├── 14.10 Trip to Japan
    ├── 14.11 Weekend in Paris
    └── 14.12 Summer vacation

20-29 Work
├── 20 Current work         [Note: A0 instead of A1]
│   ├── 20.10 Project Alpha
│   └── 20.11 Project Beta
└── 21 Admin               [Note: A1 instead of A2]
    └── 21.10 Quarterly reports

30-39 Projects
└── 30 Active              [Note: A0 instead of A1]
    ├── 30.10 Learning guitar
    └── 30.11 Home automation
```

## Comparison: Standard vs Alternative Layout 1

### Standard Layout
- **Usable areas**: 10 (10-19, 20-29, ..., 90-99)
- **Categories**: A1-A9 (e.g., 11-19, 21-29, etc.)
- **IDs**: .11-.99 (skips AC.10)
- **Area management**: A0 categories (10, 20, 30, etc.)
- **Total usable IDs**: 7,209 (72.09% of total)

### Alternative Layout 1
- **Usable areas**: 9 (10-19, 20-29, ..., 80-89)
- **Categories**: A0-A9 (e.g., 10-19, 20-29, etc.)
- **IDs**: .10-.99 (no skipping)
- **Area management**: 01-09 in system area
- **Total usable IDs**: 8,100 (81.00% of total)

**Result**: 9 more categories and 891 more IDs available!

## The JDex (Index) - The Heart of the System

**The index IS your Johnny.Decimal system.**

The JDex is a central record of every ID in your system, kept in a notes app like:
- Bear (recommended for Apple users)
- Obsidian (cross-platform favorite)
- Simplenote (simple option)
- Apple Notes

### Why You Need a JDex

1. **Prevents duplicate IDs** - Always know what numbers are taken
2. **Records locations** - Track where things are across your digital life
3. **Enables search** - Find anything by searching your notes
4. **System memory** - Document decisions and track everything
5. **Note-taking** - Each ID becomes a place for notes and thoughts

### How to Use the JDex

1. **One note per ID** - Create a note titled "14.10 Travel insurance"
2. **Location tracking** - Record where the item actually is
3. **Search first** - Always check your JDex before creating new IDs
4. **Add context** - Include keywords, dates, and relevant details

Example JDex entry:
```
14.10 Travel insurance

Location: Email folder, Google Drive
Keywords: insurance, travel, policy, claims
Notes: Policy number ABC123, expires Dec 2025
Claim form saved in email "Insurance claims" folder
```

## Core Principles (Unchanged)

### 1. Everything Has One Place
Each item gets exactly one Johnny.Decimal number and lives in exactly one place.

### 2. Numbers Never Change
Once you assign 14.10, it's always 14.10. This creates stability and reliability.

### 3. Limit Your Choices
Maximum 10 at each level forces you to think clearly and avoid overwhelm.

### 4. Categories Are Where You Work
When you sit down to do something, you go to a category. This is where your work happens.

### 5. A Little Friction Is Good
Creating new areas and categories should require thought and consideration.

## Benefits of Alternative Layout 1

### Efficiency Improvements
- **12.36% more usable IDs** (891 additional IDs)
- **9 more categories** available for organization
- **No wasted AC.10 IDs** 
- **Better resource utilization**

### Organizational Benefits
- **Centralized area management** in system area (00-09)
- **Cleaner separation** between system and content
- **More granular organization** with additional categories
- **Consistent with Johnny.Decimal principles**

### Same Core Benefits
- Never more than 10 choices at any level
- Clear hierarchy prevents getting lost
- Numbers provide consistent ordering
- Easy communication with short, memorable numbers
- Cross-platform organization that works everywhere
- Memory and search through the JDex

## Getting Started with Alternative Layout 1

### 1. Design Your Areas (Maximum 9)
Start with 3-5 broad areas of your life:
- 10-19 Life admin
- 20-29 Work  
- 30-39 Hobbies/Projects

### 2. Set Up System Management
The system area (00-09) is automatically created with:
- 00 System management (overall system)
- 01 Area 10-19 management
- 02 Area 20-29 management  
- 03 Area 30-39 management

### 3. Add Categories As Needed (A0-A9)
Don't pre-plan everything. Add categories when you need them:
- 10 Me (personal documents) - Note: A0 position
- 11 House (home-related stuff) - Note: A1 position
- 12 Money (financial matters) - Note: A2 position

### 4. Assign IDs (.10-.99)
Create IDs starting from .10 instead of .11:
- 10.10 Passport renewal
- 10.11 Health insurance
- 10.12 Gym membership

### 5. Create Your JDex
Set up a notes app and start creating entries for each ID.

## Advanced Concepts

### Standard Zeros in Alt. 1
Some users implement standard patterns across categories:
- xx.00 Index (system categories only)
- xx.01 Inbox
- xx.02 Work in progress  
- xx.03 Templates
- xx.04 Links
- xx.08 Someday
- xx.09 Archive

### Multiple Systems
If you have completely separate domains (like work vs. personal), you might need multiple systems with identifiers like:
- SYS.AC.ID (e.g., WORK.14.10)

### The Librarian
Someone who maintains the system and keeps it organized. This could be you or a team member.

## Best Practices for Alt. 1

### For Areas
- Keep them broad - "Life admin" not "Insurance"
- Think about major domains of your life
- Remember you have 9 areas instead of 10
- Don't worry about using all 9 areas

### For Categories  
- This is where you work
- Prefer fewer, broader categories
- "Money" instead of "Budget", "Savings", "Investments"
- Remember you now have A0-A9 instead of A1-A9
- Let them emerge naturally

### For IDs
- Start from .10 instead of .11
- Create meaningful descriptions
- Use dates in subfolders (2024-12-15 format)
- One subfolder level is okay, more is chaos
- Start in your JDex, then create files

### For the JDex
- Search your notes before creating new IDs
- Record locations across your digital life
- Add keywords to help future searches
- Include context and decisions

## Common Mistakes to Avoid

1. **Creating too many areas** - Start small, grow gradually (max 9)
2. **Over-categorizing** - Broader categories are usually better  
3. **Skipping the JDex** - This is the heart of the system
4. **Pre-planning everything** - Let the system grow organically
5. **Going too deep** - Stick to exactly three levels
6. **Forgetting about .10** - Don't skip AC.10 like in standard layout

## Why Alternative Layout 1 Works Better

The Alternative Layout 1 works because it:
- **Provides more capacity** through efficient use of numbering
- **Eliminates waste** by not skipping AC.10 IDs
- **Centralizes management** in a logical system area
- **Maintains all core benefits** of the original system
- **Reduces decision fatigue** through clear limits
- **Provides structure** without being rigid
- **Scales with your life** from simple to complex
- **Works everywhere** across all platforms
- **Gets better with use** as you learn the numbers

The key insight: It's not about the perfect filing system. It's about reducing the stress and time spent looking for things, so you can focus on what matters - while making better use of the available numbering space.

## Learn More

- Original proposal: [Alternative Layout 1](https://forum.johnnydecimal.com/t/the-standard-zeros/1558/12)
- Official website: [johnnydecimal.com](https://johnnydecimal.com/)
- Community forum: [forum.johnnydecimal.com](https://forum.johnnydecimal.com/)
- Discord: Available through the website

The system is free to use and the concepts work at home, work, or anywhere you need organization.