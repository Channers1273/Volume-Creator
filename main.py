from converter import *
import sys

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print("Incorrect Usage")

    else:
        argc = len(sys.argv)

        target_name = sys.argv[1]

        for index in range (2, argc):
            target_name += (" " + sys.argv[index])



        # copy chapters into zips folder
        chapter_list = scan_for_cbz_files('/chapters')
        copy_files(chapter_list, '/chapters', '/zips')

        # get files that will be extracted and extract to 'unzipped'
    
        to_be_converted = scan_for_cbz_files('/zips')
        cbz_to_zip(to_be_converted)
    
        to_be_unzipped = scan_for_zip_files('/zips')
        unzip_files(to_be_unzipped)
    
        place_in_correct_order('/unzipped/', target_name)

        zip_folder("compiledVolumes/" + target_name)

        zip_to_cbz("compiledVolumes/" + target_name + ".zip")
        remove_temp_files()
