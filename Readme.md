The Great Eye
The Great Eye is an AI-driven image management suite for macOS. It transforms how you interact with your local photo library by using state-of-the-art vision models to make images searchable by their actual content, rather than just filenames.

The project offers two distinct workflows:

Semantic Vector Search (App): A GUI for complex, conceptual searches.

Automated Metadata Tagging (CLI): A background daemon that "injects" AI descriptions into your files for native macOS search.

📂 Project Structure
Plaintext
The_Great_Eye/
├── App/                # The GUI Application (PyQt5)
│   ├── main.py         # App entry point
│   ├── gui/            # UI components (Grid, Clickable Labels)
│   └── core/           # CLIP Embedding & FAISS Indexing
├── image_descriptor.py # BLIP-based captioning logic
├── manager.py          # AppleScript & File I/O orchestration
├── runner.py           # CLI execution entry point
├── config.json         # User-defined paths for SSD monitoring
└── com.watched.ssd.plist # macOS LaunchDaemon configuration
🚀 How It Works
1. The App: Semantic Vector Search

The App version is designed for deep discovery and visual browsing.

The Model: Uses CLIP (Contrastive Language-Image Pre-training). This model understands images and text in a shared "vector space."

The Process: 
1. Indexing: The app scans your chosen folders and converts every image into a numerical vector (512 dimensional vector). 
2. Storage: These vectors are stored in a FAISS (Facebook AI Similarity Search) index for near-instant retrieval. 3. Searching: When you type "A cozy rainy afternoon," the app converts your text into a vector and finds the images whose numerical "addresses" are closest to it.

Result: You can find images based on abstract concepts, moods, or specific color palettes without any manual tagging.

2. The CLI: Automated Spotlight Integration

The CLI version is a "set it and forget it" utility that makes your images natively searchable in macOS.

The Model: Uses BLIP (Bootstrapping Language-Image Pre-training) to generate human-like text descriptions from images.

The Process:

Sensing: A background LaunchDaemon monitors your Mac for external SSD connections.

Targeting: It looks at config.json to identify specific "flat" folders to process.

Captioning: BLIP "reads" the image and creates a caption (e.g., "A golden retriever playing in a park with a red ball").

Injection: The script uses AppleScript to write this caption directly into the Finder Comment metadata of the file.

Result: You don't need to open any app to search. Simply use macOS Spotlight (Cmd + Space) or the Finder search bar. Your AI-generated captions are now part of the file itself.

🛠️ Setup & Installation
Prerequisites

macOS: Highly optimized for Apple Silicon (M1/M2/M3) using MPS acceleration.

Permissions: For the CLI to work, your Terminal or IDE must have Full Disk Access and Accessibility permissions in System Settings.

Installation

A standalone macOS application (available as .app) for Semantic Vector Search.

Model: CLIP (OpenAI).

Tech: PyQt5, FAISS, SQLite.

Function: Indexes your images into a high-dimensional vector space. Allows you to search for concepts like "atmospheric lighting" or "lonely mountain" even if those words aren't in a caption.

Usage: Open The Great Eye.app or run python App/main.py.

Bash
# Install core dependencies
pip install torch torchvision transformers PyQt5 faiss-cpu pillow numpy
Deploying the SSD Monitor (CLI)

To enable the automatic SSD sensing:

Update config.json with your target image folder paths.

CLI Configuration

Update your config.json with the paths you want to monitor:

JSON
{
  "watched_paths": [
    "/Volumes/MySSD/Photos/2024/Forest_Trip",
    "/Volumes/MySSD/Photos/Family/Portraits"
  ]
}

Load the daemon:
Bash
cp com.watched.ssd.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.watched.ssd.plist

🧠 Comparison: Which one to use?
Feature	App 					(GUI)													CLI (Background)
Search Method					Vector Similarity (Concept)								Keyword Matching (Text)
Primary Model					CLIP													BLIP
Best For						"Find photos with a specific vibe"						"Search my SSD in Finder"
User Effort						Manual Search											Zero (Automated)

⚠️ Known Issues & Workarounds
OpenMP Conflict: The project sets os.environ['KMP_DUPLICATE_LIB_OK'] = 'True' to resolve library collisions on macOS.

Folder Depth: The CLI version currently requires "flat" folder paths in config.json. Ensure you specify the exact folder containing the images.