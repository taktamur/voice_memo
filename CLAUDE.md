# CLAUDE.md - Voice Memo Project Guidelines

## Commands
- `./voice_sync.sh` - Sync voice files from recorder to Mac

## Code Style Guidelines
- Shell scripts use bash shebang `#!/bin/bash` at the top
- Variables are in UPPERCASE for configuration/globals 
- Functions use snake_case
- Error handling: Exit with code 1 and informative message
- Comments in Japanese for user-facing messages, English for code explanation
- Always use double quotes for variables and paths with spaces
- Indentation: 4 spaces
- Include informative echo statements for user feedback
- Validate inputs/existence of resources before performing operations
- Always handle special characters in paths properly
- Functions should be focused on a single responsibility
- Use proper array handling with readarray when dealing with file lists

## Project Structure
- Source files from `/Volumes/NO NAME/VOICE`
- Destination files to `${HOME}/.voice_memo/`
- File naming convention: YYYYMMDD_HHMMSS.MP3