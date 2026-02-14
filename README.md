# Git Push Tool

A simple, cross-platform desktop application that makes Git commits and pushes as easy as clicking a button!

## Features

✨ **Simple Interface** - Select folder, write message, push  
🖥️ **Cross-Platform** - Works on Windows, Mac, and Linux  
📝 **Visual Output** - See exactly what Git is doing in real-time  
🎯 **One-Click Push** - Automatically runs `git add .`, `git commit`, and `git push`  

## What It Does

When you click "Push to GitHub", the tool automatically runs these three commands:

```bash
git add .
git commit -m "Your message here"
git push origin main
```

## Installation & Usage

### Option 1: Run from Python (Easiest for Development)

**Requirements:**
- Python 3.7 or higher
- Git installed on your system

**Steps:**

1. Download `git_push_tool.py`

2. Run the program:
   ```bash
   python git_push_tool.py
   ```
   
   Or on Mac/Linux:
   ```bash
   python3 git_push_tool.py
   ```

That's it! The program will open in a new window.

### Option 2: Create a Standalone Executable (No Python Required)

If you want to create an `.exe` (Windows) or `.app` (Mac) that you can double-click without needing Python installed:

**Steps:**

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Run the build script:
   ```bash
   python build_executable.py
   ```

3. Find your executable in the `dist` folder:
   - **Windows**: `dist/GitPushTool.exe`
   - **Mac**: `dist/GitPushTool.app`
   - **Linux**: `dist/GitPushTool`

4. Move the executable wherever you want and double-click to run!

### Building Manually (Alternative)

**For Windows:**
```bash
pyinstaller --onefile --windowed --name=GitPushTool git_push_tool.py
```

**For Mac:**
```bash
pyinstaller --onefile --windowed --name=GitPushTool git_push_tool.py
```

## How to Use

1. **Launch the Application**
   - Run the Python script or double-click the executable

2. **Select Your Repository Folder**
   - Click "📁 Select Folder"
   - Navigate to your Git repository
   - The tool will warn you if the folder isn't a Git repository

3. **Write Your Commit Message**
   - Enter a description of your changes
   - Default is "Updated project" but you should customize it!

4. **Push to GitHub**
   - Click "🚀 Push to GitHub"
   - Watch the output console to see what's happening
   - You'll get a success message when complete

## Prerequisites

Before using this tool, make sure you have:

1. **Git installed** on your computer
   - Download from: https://git-scm.com/downloads

2. **A Git repository** initialized in your folder
   ```bash
   git init
   ```

3. **A remote named 'origin'** added to your repository
   ```bash
   git remote add origin https://github.com/yourusername/yourrepo.git
   ```

4. **Git authentication** configured (HTTPS or SSH)
   - For HTTPS: You may need a Personal Access Token
   - For SSH: Set up SSH keys with GitHub

5. **A 'main' branch** (or modify the code to use 'master')
   ```bash
   git branch -M main
   ```

## Troubleshooting

### "The selected folder does not appear to be a Git repository"
- Make sure you run `git init` in the folder first
- Check that a `.git` folder exists

### "Error in git push"
- Verify you have a remote named 'origin': `git remote -v`
- Check your branch name (might be 'master' instead of 'main')
- Ensure you have authentication set up correctly
- Try running the commands manually first to debug

### "Nothing to commit"
- This is normal if you haven't made any changes since your last commit
- Make some changes to your files and try again

### Permission Denied (Mac)
- You may need to give the app permission to run
- Go to System Preferences → Security & Privacy
- Click "Open Anyway" for GitPushTool

## Customization

Want to use a different branch? Edit the `git_push_tool.py` file and change:

```python
git push origin main
```

to:

```python
git push origin master
```

or whatever branch name you use.

## Technical Details

- **Language**: Python 3
- **GUI Framework**: tkinter (built-in to Python)
- **Git Commands**: Executed via subprocess
- **Threading**: Git operations run in background thread to keep UI responsive

## File Structure

```
git_push_tool.py       # Main application
build_executable.py    # Script to create executables
README.md             # This file
```

## License

Free to use and modify as needed!

## Tips

- 💡 Use descriptive commit messages instead of generic ones
- 💡 Review your changes before pushing (use `git status` or `git diff`)
- 💡 Pull before you push to avoid conflicts
- 💡 Consider using branches for different features

## Screenshots

The application shows:
- Folder selection button and current path
- Commit message input field
- Push button
- Output console showing all Git operations in real-time

Enjoy easier Git pushing! 🚀