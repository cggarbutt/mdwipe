# MDWipe - Metadata Removal Tool

A free, open-source desktop application for removing metadata from your files. Everything runs locally on your computer. No cloud services, no data collection, no cost.

## The Problem

Every photo you take, every PDF you create, and every audio file you edit contains hidden metadata. This metadata can include your location, camera model, software used, creation date, and sometimes even your name. When you share files online, you may be sharing more information than you realize.

Commercial metadata removal tools exist, but they often charge subscription fees or upload your files to their servers. This creates both a financial barrier and a privacy concern.

## The Solution

MDWipe is completely free software that removes metadata from your files without ever sending them anywhere. The application runs entirely on your computer. Your files remain private.

The software preserves your original files by renaming them with an "_original" suffix and creates cleaned versions with the same filename. This ensures you never lose data while giving you metadata-free files ready to share.

## Supported File Types

Images: JPG, JPEG, PNG, GIF, BMP, HEIC, WebP
Documents: PDF
Audio/Video: MP3, MP4, M4A, FLAC, OGG, WAV, AAC

## How It Works

Select the files you want to clean. Click the "Wipe Metadata" button. The application creates cleaned versions of your files in the same directory as the originals. Your original files are automatically renamed with "_original" appended to preserve them.

For example, if you process "photo.jpg", you will end up with:
- photo_original.jpg (your untouched original)
- photo.jpg (cleaned version with no metadata)

## Technical Details

MDWipe uses established open-source libraries to handle metadata removal:
- Pillow for image processing
- pikepdf for PDF manipulation  
- mutagen for audio and video files

The core metadata removal logic is written specifically for this project. The application uses these libraries as tools but implements its own approach to ensure thorough metadata removal across different file formats.

## Installation

### For End Users (No Python Required)

Download the installer from the Releases page. Run MDWipe_Setup.exe. The application will be installed like any other Windows program with a desktop shortcut and start menu entry.

### For Developers

Requirements: Python 3.8 or higher

Install dependencies:
```
pip install -r requirements.txt
```

Run the application:
```
python metadata_wiper.py
```

Build standalone executable:
```
pip install pyinstaller
python build.py
```

## Privacy Commitment

MDWipe does not connect to the internet. All file processing happens on your local machine. No telemetry, no analytics, no data collection of any kind. The source code is available for review.

## Project Philosophy

This project exists because privacy tools should be accessible to everyone without cost. Metadata removal is a basic privacy protection that should not require a subscription or trust in a third-party service.

The software is built ethically. It uses open-source libraries as tools but does not simply wrap existing executables. The core logic is original work. All dependencies are properly licensed and attributed.

This is free software in both senses: free to use and free to examine, modify, and distribute under the MIT license.

## Development Status

Version 1.0 is feature-complete and functional. The application successfully removes metadata from all supported file types. Current development focuses on testing across different file variations and edge cases.

Future considerations include support for additional file formats and potential batch processing optimizations for large file sets.

## Contributing

This project welcomes contributions. If you encounter bugs, please report them with details about the file type and error message. If you want to add support for new file formats, submit a pull request with your implementation.

Code contributions should maintain the project's core principles: local processing only, no external dependencies beyond the specified libraries, and clear code that can be audited.

## License

MDWipe is released under the MIT License. See LICENSE.txt for full details including third-party library attributions.

The software is provided as-is without warranty. Users are responsible for verifying that metadata has been removed to their satisfaction and for ensuring they have the right to modify their files.

## Acknowledgments

This project builds on work by:
- The Pillow team for image processing capabilities
- James R. Barlow for pikepdf
- The mutagen developers for audio/video tag handling

These libraries made it possible to create accessible metadata removal software without reinventing low-level file format parsing.

---

Created by Colin Garbutt. Maintained as free software for anyone who needs it.
