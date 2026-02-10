from PIL import Image
from pikepdf import Pdf
from mutagen import File as MutagenFile
import shutil
from pathlib import Path


def remove_image_metadata(input_path, output_path):
    try:
        img = Image.open(input_path)

        data = list(img.getdata())
        clean_img = Image.new(img.mode, img.size)
        clean_img.putdata(data)
        
        if img.format == 'JPEG':
            clean_img.save(output_path, 'JPEG', quality=95, optimize=True)
        elif img.format == 'PNG':
            clean_img.save(output_path, 'PNG', optimize=True)
        elif img.format == 'GIF':
            clean_img.save(output_path, 'GIF')
        else:
            try:
                clean_img.save(output_path, img.format)
            except:
                clean_img.save(output_path, 'PNG')
        
        print(f"Image metadata removed: {Path(input_path).name}")
        return True
        
    except Exception as e:
        print(f"Error removing image metadata from {Path(input_path).name}: {e}")
        return False


def remove_pdf_metadata(input_path, output_path):
    try:
        pdf = Pdf.open(input_path)
        
        with pdf.open_metadata() as meta:
            meta.clear()
        
        if '/Info' in pdf.trailer:
            del pdf.trailer['/Info']
        
        pdf.save(output_path)
        
        print(f"PDF metadata removed: {Path(input_path).name}")
        return True
        
    except Exception as e:
        print(f"Error removing PDF metadata from {Path(input_path).name}: {e}")
        return False


def remove_audio_video_metadata(input_path, output_path):
    try:
        shutil.copy2(input_path, output_path)
        
        audio = MutagenFile(output_path)
        
        if audio is None:
            print(f"Unsupported audio/video format: {Path(input_path).name}")
            return False
        
        audio.delete()
        audio.save()
        
        print(f"Audio/Video metadata removed: {Path(input_path).name}")
        return True
        
    except Exception as e:
        print(f"Error removing audio/video metadata from {Path(input_path).name}: {e}")
        return False


def remove_metadata(input_path, output_path):
    ext = Path(input_path).suffix.lower()
    
    if ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.heic', '.webp']:
        return remove_image_metadata(input_path, output_path)
    
    elif ext == '.pdf':
        return remove_pdf_metadata(input_path, output_path)
    
    elif ext in ['.mp3', '.mp4', '.m4a', '.flac', '.ogg', '.wav', '.aac']:
        return remove_audio_video_metadata(input_path, output_path)
    
    else:
        print(f"Unsupported file type: {ext}")
        return False


def get_supported_formats():
    return {
        'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.heic', '.webp'],
        'PDFs': ['.pdf'],
        'Audio/Video': ['.mp3', '.mp4', '.m4a', '.flac', '.ogg', '.wav', '.aac']
    }

if __name__ == "__main__":
    print("Metadata Remover Module")
    print("=" * 50)
    print("\nSupported formats:")
    for category, formats in get_supported_formats().items():
        print(f"\n{category}:")
        print(f"  {', '.join(formats)}")
    print("\n" + "=" * 50)
    print("Module loaded successfully!")
    print("\nUsage:")
    print("  from metadata_remover import remove_metadata")
    print("  remove_metadata('input.jpg', 'output.jpg')")