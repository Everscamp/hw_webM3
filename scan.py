import sys
from threading import Thread
from pathlib import Path

images_files = []
docx_files = []
folders = []
audio_files = []
video_files = []
archives = []
other = []
unknown_extensions = set()
extensions = set()

known_extensions = {
    ('JPEG', 'PNG', 'JPG', 'SVG') : images_files,
    ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX', 'RTF'): docx_files,
    ('ZIP', 'GZ', 'TAR', 'WIN'): archives,
    ('MP3', 'OGG', 'WAV', 'AMR') : audio_files,
    ('AVI', 'MP4', 'MOV', 'MKV', 'WEBM') : video_files
}

def all_extentions() -> tuple: #returns tuple all known extentions
    keys = ()
    for key in known_extensions:
        keys+=key

    return keys

def get_extensions(file_name) -> str:
    return Path(file_name).suffix[1:].upper()

def scan(folder):
    threads = []

    for item in folder.iterdir():
        if item.is_dir():
            
            if item.name not in ('archives', 'video', 'audio', 'documents', 'images', 'other_files'):
                folders.append(item)
                scan(item)
            continue

        extension = get_extensions(file_name=item.name)
        new_name = folder/item.name
# Added Threads here
        th = Thread(target=inner_scan_helper, args=(extension, new_name))
        th.start()
        threads.append(th)

        [th.join() for th in threads]

# сreated solely to make it easier to add threads to scan function
def inner_scan_helper(extension, new_name):
    if not extension:
            other.append(new_name)
    if extension not in all_extentions():
        unknown_extensions.add(extension)
        other.append(new_name)
    else:
        for key in known_extensions:
            try: #not sure if try-except actualy needed here 
                if extension in key:
                    container = known_extensions[key]
                    extensions.add(extension)
                    container.append(new_name)
            except KeyError:
                unknown_extensions.add(extension)
                other.append(new_name)

#scans all folders, needed to create a result.txt after sorting
def simple_scan(folder):
    for item in folder.iterdir():
        if item.is_dir():
            folders.append(item)
            simple_scan(item)

        extension = get_extensions(file_name=item.name)
        new_name = folder/item.name

        if extension not in all_extentions() and not item.is_dir():
            if extension:
                unknown_extensions.add(extension)
                other.append(new_name)
            if not extension:
                unknown_extensions.add('unknown')
        else:
            for key in known_extensions:
                if extension in key:
                    container = known_extensions[key]
                    extensions.add(extension)
                    container.append(new_name)

#creates reault.txt after simple_scan
def write_results_to_file(path): 
    file = open(f"{path}/result.txt", "w")

    file.writelines([f'Images: \n{images_files}\n', 
    f'\nDocx: \n{docx_files}\n', 
    f'\nArchives: \n{archives}\n', 
    f'\nAudio: \n{audio_files}\n', 
    f'\nVideo: \n{video_files}\n', 
    f'\nOthers: \n{other}\n', 
    f'\nAll extensions: {extensions}\n', 
    f'\nUnknown extensions: {unknown_extensions}\n',])

    file.close()

if __name__ == '__main__':
    path = sys.argv[1]
    print(f"Start in {path}")

    folder = Path(path)
    
    scan(folder)
