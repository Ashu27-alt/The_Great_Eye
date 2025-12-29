import subprocess
import os

def write_finder_comment(image_path, description):
    """
    Write comment that actually appears in Finder's Get Info
    and is properly indexed by Spotlight
    """
    # Make path absolute
    abs_path = os.path.abspath(image_path)
    
    # Escape special characters for AppleScript
    description_escaped = description.replace('"', '\\"').replace('\\', '\\\\')
    
    applescript = f'''
    tell application "Finder"
        set theFile to POSIX file "{abs_path}" as alias
        set comment of theFile to "{description_escaped}"
    end tell
    '''
    
    try:
        result = subprocess.run(
            ['osascript', '-e', applescript],
            check=True,
            capture_output=True,
            text=True
        )
        print(f"Set Finder comment for: {os.path.basename(image_path)}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error: {e.stderr}")
        return False
