import os
import time
import shutil
import zipfile
from mockup import Mockup
from svg_converter import png2svg
import threading


downloads = "/Users/amitshachar/Downloads"
documents = "/Users/amitshachar/Documents"
etsy = f"{documents}/etsy/"


def create_dir():
    project_name = input("Enter Project Name: ")
    project_path = f"{etsy}/{project_name}"
    if not os.path.isdir(project_path):
        os.makedirs(project_path)
        os.makedirs(f"{project_path}/Stock")
        os.makedirs(f"{project_path}/Mockup")
        os.makedirs(f"{project_path}/Product")
    monitor_directory(downloads, project_path)


def sort_files(file, project_path):
    if "DALL" in file:
        time.sleep(2)
        shutil.copy(f"{downloads}/{file}", f"{project_path}/Stock/{file}")
        # create_pruduct(project_path, file)
        threading.Thread(target=create_pruduct, args=(project_path.replace("//", "/"), file)).start()


def create_pruduct(project_path, file):
    print("starting to generate product")
    png2svg(input_file=f"{project_path}/Stock/{file}", output_path=f"{project_path}/Product").file_to_svg()
    find_matching_files(f"{project_path}/Product/")
    num_files = len(os.listdir(f"{project_path}/product/"))
    if num_files > 11:
        print("starting generating mockups")
        Mockup("mockupa", f"{project_path}/product", output_path=f"{project_path}/Mockup/").create_mockup()

    # elif "Bundle" in file:
    #     shutil.copy(f"{downloads}/{file}/1.jpg", f"{project_path}/Mockup/4.jpg")
    #     shutil.copy(f"{downloads}/{file}/2.jpg", f"{project_path}/Mockup/3.jpg")
    #     shutil.copy(f"{downloads}/{file}/3.jpg", f"{project_path}/Mockup/2.jpg")
    #     shutil.copy(f"{downloads}/{file}/3.jpg", f"{project_path}/Mockup/1.jpg")
    #     shutil.copy(f"{downloads}\\{file}", f"{project_path}\\Product\\{file.replace('_', '')}")


def find_matching_files(directory):
    files = os.listdir(directory)
    base_names = set(os.path.splitext(file)[0] for file in files)
    matching_pairs = {}
    for base_name in base_names:
        matches = [file for file in files if file.startswith(base_name) and file != base_name]
        if len(matches) == 2:
            matching_pairs[base_name] = matches
    zip_files(directory, matching_pairs)


def zip_files(directory, file_pairs):
    os.listdir(directory)
    for base_name, files in file_pairs.items():
        zip_filename = os.path.join(directory, f"{base_name.replace('_', '')}.zip")
        if zip_filename not in files:
            with zipfile.ZipFile(zip_filename, 'w') as zipf:
                for file in files:
                    file_path = os.path.join(directory, file)
                    zipf.write(file_path, arcname=file)
            print(f"Created {zip_filename}")


def get_files_in_directory(directory):
    return set(os.listdir(directory))

def set_project_name(directory):
    filename = 1
    while True:
        if is_dir(f"{directory}/{str(len(os.listdir(directory)) + filename )}"):
            filename +=1
        else:
            return str(len(os.listdir(directory)) + filename )


def create_dirs():
    project_name = set_project_name(etsy)
    project_path = f"{etsy}/{project_name}"
    if not os.path.isdir(project_path):
        os.makedirs(project_path)
        os.makedirs(f"{project_path}/Stock")
        os.makedirs(f"{project_path}/Mockup")
        os.makedirs(f"{project_path}/Product")
    return project_path

def is_dir(dir):
    if os.path.isdir(dir):
        return True
    else:
        return False

def monitor_directory():
    project_path = create_dirs()
    print(f"Monitoring {downloads} for new files...")
    observed_files = get_files_in_directory(downloads)
    counter = 0
    try:
        while True:
            time.sleep(1)
            current_files = get_files_in_directory(downloads)
            new_files = current_files - observed_files
            if new_files and list(new_files)[0].split(".")[-1] != "download":
                counter += 1
                print(f"New file(s) detected: {new_files}")
                sort_files(list(new_files)[0], project_path)
                observed_files = current_files
                if counter == 4:
                    counter = 0
                    project_path = create_dirs()
    except KeyboardInterrupt:
        print("Stopping directory monitoring.")


monitor_directory()
