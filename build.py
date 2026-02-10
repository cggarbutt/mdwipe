import os
import shutil
import subprocess
import sys

def build_executable():
    """Build standalone executable for MDWipe"""
    
    print("Building MDWipe executable...")
    print("-" * 50)
    
    import platform
    separator = ';' if platform.system() == 'Windows' else ':'
    
    cmd = [
        'pyinstaller',
        '--onefile',                 
        '--windowed',                 
        '--name=MDWipe',               
        '--icon=MDWipe.ico',             
        f'--add-data=MDWipe.ico{separator}.',
        'metadata_wiper.py'
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("\nBuild successful!")
        print(f"Executable location: dist/MDWipe.exe")
        print("\nNext steps:")
        print("1. Test the executable in dist/MDWipe.exe")
        print("2. Create installer using Inno Setup (see INSTALLER.md)")
    except subprocess.CalledProcessError as e:
        print(f"\nBuild failed: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("\nPyInstaller not found. Install it with:")
        print("   pip install pyinstaller")
        sys.exit(1)

if __name__ == "__main__":
    build_executable()
