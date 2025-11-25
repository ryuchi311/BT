# Scripts Directory

This directory contains utility scripts organized by purpose. These scripts are not part of the main application runtime but are used for database migrations, fixes, and utilities.

## Directory Structure

### migrations/
Database migration and initialization scripts. Run these when setting up or updating the database schema.

**Key files:**
- `init_db.py` - Initialize the database with tables
- `migrate_sqlite.py` - Main migration script for SQLite
- `migrate_telegram_lastname.py` - Add last_name field to users
- `migrate_onboarding.py` - Add onboarding fields
- Other migration scripts for specific features

**Usage:**
```bash
cd scripts/migrations
python migrate_sqlite.py
```

### fixes/
One-time fix and update scripts for UI improvements and feature additions. These were used during development to modify templates and add features.

**Categories:**
- `add_*.py` - Scripts that add new UI components or features
- `fix_*.py` - Scripts that fix bugs or issues
- `update_*.py` - Scripts that update existing features

**Note:** Most of these scripts have already been run and may not need to be executed again.

### utils/
Utility scripts for inspecting and checking the database state.

**Files:**
- `inspect_db.py` - Inspect database structure
- `check_quest_categories.py` - Check quest categories
- `check_rewards.py` - Check rewards data

**Usage:**
```bash
cd scripts/utils
python inspect_db.py
```

## Running Scripts

To run any script from the project root:
```bash
python scripts/migrations/migrate_sqlite.py
python scripts/utils/inspect_db.py
```

Or navigate to the specific directory first:
```bash
cd scripts/migrations
python migrate_sqlite.py
```
