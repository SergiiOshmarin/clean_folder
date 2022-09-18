'''Importing os,shutil,sys library'''
import sys
import os
import shutil

''' Creating function "normalize"
It will check if any file name has Kyrylic letters or not latin letters or numbers.
If Kyrylic letters found, they will be changed to Latin. If others exept Latin letters or numbers,
Will be changed to "_"
Function taking as string and return formatted string, which will be used later in other function.'''
def normalize(string):
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
    lst=[]
    TRANS = {}
    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()
    for i in string:
        if ord(i) in range(48,58) or  ord(i) in range(65,91) or ord(i) in range(97,123) or i in range(10):
            lst.append(i)
        elif i in CYRILLIC_SYMBOLS:
            lst.append(i.translate(TRANS))
        elif i.isupper():
            if i.lower() in CYRILLIC_SYMBOLS:
                lst.append(i.lower().translate(TRANS).upper())
            else:
                lst.append("_")
        else:
            lst.append("_")
    new_string="".join(lst)
    return new_string

'''Creating function "sorting", which will take path to the folder which we are going to check.
With "for" we will path through all files and folders inside "path", and check if is it folder or file.
For folder we will check:
If it is empty we will delete it.
If in folder there are other items function will repeat itselve,
Except if folder name is not one of which we are creating .
For files, we will segregate them by folders and rename with "normalize" function.
Function taking as parameter string Path, and when completed print out that function is completed.'''

def sorting(path):
    imag="images"
    docum="documents"
    aud="audio"
    vid="video"
    arch="archives"
    oth="others"
    for filename in os.scandir(path):
        file_extension=os.path.splitext(filename)[1]
        format_name=normalize(os.path.splitext(os.path.basename(filename.path))[0])
        maindir=os.path.dirname(filename.path)
        if filename.is_file():
            if file_extension.upper() in ('.AVI', '.MP4', '.MOV', '.MKV'):
                os.renames(filename.path,os.path.join(maindir,vid,format_name+file_extension))
            elif file_extension.upper() in ('.BMP', '.JPEG', '.PNG', '.JPG', '.SVG','GIF'):
                os.renames(filename.path,os.path.join(maindir,imag,format_name+file_extension))
            elif file_extension.upper() in ('.DOC','.DOCX','.TXT','.PDF','.XLSX','.PPTX'):
                os.renames(filename.path,os.path.join(maindir,docum,format_name+file_extension))
            elif file_extension.upper() in ('.MP3','.OGG','.WAV','.AMR'):
                os.renames(filename.path,os.path.join(maindir,aud,format_name+file_extension))
            elif file_extension.upper() in ('.ZIP' or '.GZ' or '.TAR'):
                os.renames(filename.path,os.path.join(maindir,arch,format_name+file_extension))
                shutil.unpack_archive(os.path.join(maindir,arch,format_name+file_extension), os.path.join(maindir,arch,format_name))
            else:
                os.renames(filename.path,os.path.join(maindir,oth,os.path.basename(filename.path)))
        elif filename.is_dir():
            if filename.name not in (imag, docum, aud, vid, arch, oth):
                sorting(filename.path)
        else:
            os.renames(filename.path,os.path.join(maindir,oth,format_name+file_extension))
    for dirpath, dirnames, filenames in os.walk(path, topdown=False):
        if not dirnames and not filenames:
            os.rmdir(dirpath)
    
'''Taking system arguments and chechick if they can be used'''

def main():
    x = input('Enter path to folder which should be cleaned:')
    #if len(sys.argv) < 2:
        #print('Enter path to folder which should be cleaned')
        #exit()
    #way = sys.argv[1]
    if not (os.path.exists(x) and os.path.isdir(x)):
        print('Path incorrect. Try again')
        main()
    sorting(x)
    print("Everything done. Please cross check")
if __name__ == '__main__':
    exit(main())