import os
import shutil
import sys

folders = [
    'зображення', ' відео файли', 'документи', "музика", "архіви"
]
path_to_files = []

dir_list = ['images', 'documents', 'audio', 'video', 'archives']
image_extensions = ('.jpeg', '.png', '.jpg', '.svg')
video_extensions = ('.avi', '.mp4', '.mov', '.mkv')
document_extensions = ('.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx')
music_extensions = ('.mp3', '.ogg', '.wav', '.amr')
archive_extensions = ('.zip', '.gz', '.tar')


def find_files(path):
    for file in os.listdir(path):
        new_path = os.path.join(path, file)

        if os.path.isdir(new_path):
            find_files(new_path)
        else:
            path_to_files.append(new_path)
    return path_to_files


def sort_by_type():
    image, video, documents, music, archive, unknown = [], [], [], [], [], []

    files = find_files(path)

    for file in files:
        full_name = os.path.basename(file)
        name, extension = os.path.splitext(file)
        if extension.lower() in image_extensions:
            image.append(full_name)
        elif extension.lower() in video_extensions:
            video.append(full_name)
        elif extension.lower() in document_extensions:
            documents.append(full_name)
        elif extension.lower() in music_extensions:
            music.append(full_name)
        elif extension.lower() in archive_extensions:
            archive.append(full_name)
        else:
            unknown.append(full_name)
    print("Список зображень:", image)
    print("Список відеофайлів:", video)
    print("Список документів:", documents)
    print("Список музичних файлів:", music)
    print("Список архівів:", archive)
    print("Список файлів з невідомим розширенням:", unknown)


def normalize(data):
    cyrillic_to_latin_map = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
        'е': 'e', 'є': 'ie', 'ж': 'zh', 'з': 'z', 'и': 'y',
        'і': 'i', 'ї': 'i', 'й': 'i', 'к': 'k', 'л': 'l',
        'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
        'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh',
        'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ь': "'",
        'ю': 'iu', 'я': 'ia',
    }

    normalized_str = ''
    for char in data:
        char_lower = char.lower()
        if char_lower in cyrillic_to_latin_map:
            if char.isupper():
                normalized_str += cyrillic_to_latin_map[char_lower].capitalize()
            else:
                normalized_str += cyrillic_to_latin_map[char_lower]
        elif char.isalnum():
            normalized_str += char
        else:
            normalized_str += '_'

    return normalized_str


def rename_files():
    files = find_files(path)
    main_folder = os.path.basename(path)
    for file in files:
        filename, extension = os.path.splitext(os.path.basename(file))

        new_filename = normalize(filename)
        if extension.lower() in image_extensions:
            new_filename = os.path.join(main_folder, 'images', new_filename)
        elif extension.lower() in video_extensions:
            new_filename = os.path.join(main_folder, 'videos', new_filename)
        elif extension.lower() in document_extensions:
            new_filename = os.path.join(main_folder, 'documents', new_filename)
        elif extension.lower() in music_extensions:
            new_filename = os.path.join(main_folder, 'audio', new_filename)
        elif extension.lower() in archive_extensions:
            shutil.unpack_archive(file, os.path.join('.', 'archives', new_filename))
            new_filename = os.path.join(main_folder, 'archives', new_filename)
        else:
            continue

        if os.path.exists(file):
            os.rename(file, new_filename + extension)


def delete_empty_folders():
    for root, dirs, files in os.walk(path):
        for folder in dirs:
            if folder in dir_list:
                continue
            folder_path = os.path.join(root, folder)
            if not os.listdir(folder_path):
                os.rmdir(folder_path)
    return


def sort():
    for dir in dir_list:
        dir_path = os.path.join(path, dir)
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
    sort_by_type()
    rename_files()
    delete_empty_folders()


if __name__ == '__main__':
    path = sys.argv[1]
    sort()
