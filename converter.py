import os
import zipfile
import shutil

def extract_name(file):
    path = file.split('/')
    return path[-1]

def extract_name_from_directory(file, loc):
    return file.split(loc)[1]

def scan_for_cbz_files(directory):
    path = os.getcwd() + directory
    files = [os.path.join(path, file) for file in os.listdir(path) if file.endswith('.cbz')]
    return files

def scan_for_zip_files(directory):
    path = os.getcwd() + directory
    files = [os.path.join(path, file) for file in os.listdir(path) if file.endswith('.zip')]
    return files

def cbz_to_zip(cbz_file_list):
    for file in cbz_file_list:
        actual_name = extract_name(file)         
        actual_name = actual_name.removesuffix('.cbz')

        location = os.getcwd() + '/zips/'

        os.rename(file, location + actual_name + '.zip');

def zip_to_cbz(path_to_zip_file):
    cwd = os.getcwd() + '/'
    actual_name = extract_name(path_to_zip_file)         
    actual_name = actual_name.split('.')[0]

    final_file_name = actual_name + '.cbz'
    os.rename(path_to_zip_file, final_file_name);
    shutil.move(cwd + final_file_name, cwd + 'compiledVolumes')

def unzip_files(zip_file_list):

    for file in zip_file_list:
        name = extract_name_from_directory(file, '/zips/')
        actual_name = name.removesuffix('.zip')

        unzip_path = os.getcwd() + '/unzipped/' + actual_name

        with zipfile.ZipFile(file, 'r') as zip_ref:
            zip_ref.extractall(unzip_path);

def copy_files(file_list, src, dest):

    for file in file_list:
        name = extract_name_from_directory(file, src);
        destination = os.getcwd() + dest + name
        shutil.copyfile(file, destination)

def get_list_of_directories(directory):
    list_of_dirs = [dir.name for dir in os.scandir(directory) if dir.is_dir()]
    list_of_dirs.sort()
    return list_of_dirs
    

def place_in_correct_order(folder_name, target_name):

    unzipped_directory = os.getcwd() + folder_name # represents the directory that all the unzipped folders are

    list_of_dirs = get_list_of_directories(unzipped_directory) # gets the names of all the unzipped chapters

    final_collection_of_pages = create_target_folder(target_name) #creates the folder needed to store the folder the pages will go to and be zipped

    pages_in_first_chapter = [file for file in os.listdir(unzipped_directory + list_of_dirs[0]) if file.endswith('.jpg')]
    pages_in_first_chapter.sort()

    last_page_number = len(pages_in_first_chapter)

    file_ext = '.' + pages_in_first_chapter[0].split('.')[1]

    for page in pages_in_first_chapter:
        old_name = unzipped_directory + list_of_dirs[0] + "/" + page
        new_name = os.getcwd() + "/compiledVolumes/" + target_name + "/" + page
        os.rename(old_name, new_name)

    for index in range(1, len(list_of_dirs)):
        
        pages_in_chapter = [file for file in os.listdir(unzipped_directory + list_of_dirs[index]) if file.endswith(file_ext)]
        pages_in_chapter.sort()

        for page in pages_in_chapter:
            last_page_number += 1
            old_name = unzipped_directory + list_of_dirs[index] + "/" + page
            new_name = os.getcwd() + "/compiledVolumes/" + target_name + "/" + str(last_page_number) + file_ext
            os.rename(old_name, new_name)

def create_target_folder(target_name): 
    cwd = os.getcwd() + "/";
    collection = cwd + "compiledVolumes/" + target_name + "/"
    if not os.path.exists(collection):
        os.makedirs(collection)

# may not need this funciton in final implementation
'''
def place_in_one_folder(folder_name, target_name):

    cwd = os.getcwd() + "/";
    collection = cwd + "compiledVolumes/" + target_name + "/"
    if not os.path.exists(collection):
        os.makedirs(collection)

    path = os.getcwd() + folder_name

    list_of_dirs = get_list_of_directories(path)

    for directory in list_of_dirs:
        list_of_chapter_pages = [page for page in os.listdir(path + directory) if page.endswith('.jpg')]
        list_of_chapter_pages.sort()
       

        for page in list_of_chapter_pages:
            shutil.move(cwd + '/unzipped/' + directory + "/" + page, collection)
'''

def zip_folder(folder_to_zip):
    cwd = os.getcwd() + "/"
    path = cwd + folder_to_zip
    
    new_name = folder_to_zip.split('/')[-1]
   
    shutil.make_archive(new_name, 'zip', path)
    shutil.move(cwd + new_name + ".zip", cwd + 'compiledVolumes')

def remove_temp_files():
    cwd = os.getcwd() + "/"
    list_of_zips = [file for file in os.listdir(cwd + "zips") if file.endswith(".zip")] 

    for file in list_of_zips:
        os.remove(cwd + "zips/" + file)

    list_of_leftover_folders = get_list_of_directories(cwd + "unzipped")

    for directory in list_of_leftover_folders:
        shutil.rmtree(cwd + "unzipped/" + directory)
