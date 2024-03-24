import sys
import scan
import shutil
import normalize
from pathlib import Path
from threading import Thread

def handle_file(path, root_folder, dist):
    target_folder = root_folder/dist
    target_folder.mkdir(exist_ok=True)
    path.replace(target_folder/normalize.normalize(path.name))

def handle_archive(path, root_folder, dist):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)

    suffix = Path(path.name).suffix
    new_name = normalize.normalize(path.name).replace(suffix, '')

    archive_folder = target_folder / new_name
    archive_folder.mkdir(exist_ok=True)

    try:
        shutil.unpack_archive(str(path.resolve()), str(archive_folder.resolve()))
    except shutil.ReadError:
        archive_folder.rmdir()
        return
    except FileNotFoundError:
        archive_folder.rmdir()
        return
    path.unlink()

def remove_empty_folders(path):
    for item in path.iterdir():
        if item.is_dir():
            remove_empty_folders(item)
            try:
                item.rmdir()
            except OSError:
                pass

def main(folder_path):
    print(folder_path)

    scan.scan(folder_path)

    # I also though of adding thread here where I use handle_file function, bu decided not to
    # threads = []
    for file in scan.other:
        handle_file(file, folder_path, "others")
    #     th = Thread(target=handle_file, args=(file, folder_path, "others"))
    #     th.start()
    #     threads.append(th)

    # [th.join() for th in threads]

    for file in scan.images_files:
        handle_file(file, folder_path, "images")

    for file in scan.docx_files:
        handle_file(file, folder_path, "documents")

    for file in scan.audio_files:
        handle_file(file, folder_path, "audio")

    for file in scan.video_files:
        handle_file(file, folder_path, "video")

    for file in scan.archives:
        handle_archive(file, folder_path, "archives")

    remove_empty_folders(folder_path)

#aftersorting scan
    scan.simple_scan(folder_path) 
#creates txt file with all files and extentions
    scan.write_results_to_file(folder_path) 

    
if __name__ == '__main__':
    path = sys.argv[1]
    print(f'Start in {path}')

    folder = Path(path)
    main(folder.resolve())

#not really needed here becouse of created result.txt
    print(f"Images: {len(scan.images_files)}")
    print(f"Docx: {len(scan.docx_files)}")
    print(f"Audio: {len(scan.audio_files)}")
    print(f"Video: {len(scan.video_files)}")
    print(f"Others: {len(scan.other)}")
    print(f"All known extensions: {scan.extensions}")
    print(f"Unknown extensions: {scan.unknown_extensions}")
    print(f'For a more detailed report, look at this file {path}/result.txt')