import os
import shutil
from pathlib import Path

# Configuration
DOWNLOADS_FOLDER = Path(r'C:\Users\hello\Downloads')

SORTING_RULES = {
    'Music': {
        'extensions': ['.mp3', '.wav', '.flac'],
        'destination': Path(r'D:\Vault\My files\@audio')
    },
    'Videos': {
        'extensions': ['.mp4', '.avi', '.mkv'],
        'destination': Path(r'D:\Vault\My files\@videos')
    },
    'Images': {
        'extensions': ['.jpg', '.jpeg', '.png', '.gif'],
        'destination': Path(r'D:\Vault\My files\@dump\2024')
    },
    'Documents': {
        'extensions': ['.pdf', '.docx', '.xlsx', '.pptx', '.txt'],
        'destination': Path(r'D:\Vault\My files\@documents')
    },
    'Executables': {
        'extensions': ['.exe', '.msi'],
        'destination': Path(r'D:\Vault\My files\@exe')
    },
    'Archives': {
        'extensions': ['.zip', '.rar', '.7z', '.tar', '.gz'],
        'destination': Path(r'D:\Vault\My files\@archives')
    },
    'Others': {
        'extensions': [],
        'destination': Path(r'D:\Vault\My files\@others')
    }
}

FOLDERS_DESTINATION = Path(r'D:\Vault\My files\@folders')

def create_folders(rules, folders_destination):
    # Create folders for file types
    for folder_info in rules.values():
        destination_folder = folder_info['destination']
        if not destination_folder.exists():
            destination_folder.mkdir(parents=True, exist_ok=True)
            print(f"Created folder: {destination_folder}")

    # Create folder for directories
    if not folders_destination.exists():
        folders_destination.mkdir(parents=True, exist_ok=True)
        print(f"Created folder: {folders_destination}")

def get_destination_folder(extension, rules):
    for folder, folder_info in rules.items():
        if extension in folder_info['extensions']:
            return folder_info['destination']
    return rules['Others']['destination']

def sort_files_and_folders(source_folder, rules, folders_destination):
    for item in source_folder.iterdir():
        if item.is_file():
            extension = item.suffix.lower()
            destination_folder = get_destination_folder(extension, rules)
            destination_path = destination_folder / item.name
            print(f"Moving file {item} to {destination_path}")
            shutil.move(str(item), str(destination_path))
        elif item.is_dir():
            try:
                # Create zip archive of the folder
                archive_name = folders_destination / item.name
                shutil.make_archive(str(archive_name), 'zip', str(item))
                print(f"Created zip archive {archive_name}.zip")

                # Move the zip archive to the destination
                archive_path = folders_destination / f"{item.name}.zip"
                print(f"Moving zip archive {archive_path} to {folders_destination}")
                shutil.move(str(archive_path), str(folders_destination))

            except Exception as e:
                print(f"Failed to process folder {item}: {e}")
            finally:
                # Remove the original folder
                shutil.rmtree(str(item))
                print(f"Removed original folder {item}")

if __name__ == "__main__":
    create_folders(SORTING_RULES, FOLDERS_DESTINATION)
    sort_files_and_folders(DOWNLOADS_FOLDER, SORTING_RULES, FOLDERS_DESTINATION)
    print("Sorting completed.")
