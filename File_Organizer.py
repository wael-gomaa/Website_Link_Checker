import os
import shutil
from datetime import datetime


def create_folders(folder_path):
    
    folders = ["Images" , "Videos" , "Audio" , "Documents" , "PDFs" , "ZIP Files" , "Python Files" , "CSV Files" , "JSON Files" , "Others"]
    folders_dict = {}

    for folder in folders:

        full_folder_path = os.path.join(folder_path , folder)
        os.makedirs(full_folder_path , exist_ok=True)

        folders_dict[folder] = full_folder_path 

    return folders_dict



def move_files(folder_path , files_report , others_folder , folder):

    files = os.listdir(folder_path)
    total_files = 0


    for file in files:

        file_path = os.path.join(folder_path , file)

        if os.path.isdir(file_path):
            continue

        name , extension = os.path.splitext(file)

        if "report.txt" in file:
            continue
        
        total_files += 1

        extensions = {
            ".jpg" : folder["Images"],
            ".jpeg" : folder["Images"],
            ".png"  : folder["Images"],
            ".pdf" : folder["PDFs"],
            ".txt" : folder["Documents"],
            ".mp3" : folder["Audio"],
            ".mp4" : folder["Videos"],
            ".zip" : folder["ZIP Files"],
            ".py" : folder["Python Files"],
            ".csv" : folder["CSV Files"],
            ".json" : folder["JSON Files"]
        }

        
        found = False

        for ext , file_folder in extensions.items():

            destination = os.path.join(file_folder , file)

            if os.path.exists(destination):
                found = True
                continue

            if extension == ext:

                shutil.move(file_path , file_folder)
                found = True
                files_report[file]= os.path.basename(file_folder)
                
        
        if not found:

            others_destination = os.path.join(others_folder , file)
            

            if os.path.exists(others_destination):
                continue

            else:
                shutil.move(file_path , others_folder)
                files_report[file] = os.path.basename(others_folder)

    
    return files_report , total_files



def create_report(report_file_path , files_report , total_files):

     with open(f"{report_file_path}" , "w" , encoding="utf-8") as file:

        images_count = 0
        pdfs_count = 0
        text_count = 0
        audio_count = 0
        video_count = 0
        zip_count = 0
        python_count = 0
        csv_count = 0
        json_count = 0
        others_count = 0


        for file_name in files_report:

            file_str = str(file_name)
            
            if file_str.endswith((".jpg" , ".jpeg" , ".png")):
                images_count += 1

            elif file_str.endswith(".pdf"):
                pdfs_count += 1

            elif file_str.endswith(".txt"):
                text_count += 1

            elif file_str.endswith(".mp3"):
                audio_count += 1

            elif file_str.endswith(".mp4"):
                video_count += 1

            elif file_str.endswith(".zip"):
                zip_count += 1

            elif file_str.endswith(".py"):
                python_count += 1

            elif file_str.endswith(".csv"):
                csv_count += 1

            elif file_str.endswith(".json"):
                json_count += 1
            
            else:
                others_count += 1

        
        file.write(f"Total files : {total_files}\n\n")
        file.write(f"{images_count} Files Moved to Images folder\n")
        file.write(f"{pdfs_count} Files Moved to PDFs folder\n")
        file.write(f"{text_count} Files Moved to Documents folder\n")
        file.write(f"{audio_count} Files Moved to Audio folder\n")
        file.write(f"{video_count} Files Moved to Videos folder\n")
        file.write(f"{zip_count} Files Moved to ZIP Files folder\n")
        file.write(f"{python_count} Files Moved to Python Files folder\n")
        file.write(f"{csv_count} Files Moved to CSV Files folder\n")
        file.write(f"{json_count} Files Moved to JSON Files folder\n")
        file.write(f"{others_count} Files Moved to Others folder\n\n")

        operation_time = datetime.now().replace(microsecond=0)
        file.write(f"Report created: {operation_time}")



def main():

    folder_path = input("Enter the full folder path : ")

    if os.path.isdir(folder_path):

        REPORT_FILE_PATH = os.path.join(folder_path , "report.txt")

        files_report = {}

        folder = create_folders(folder_path)
        others_folder = folder["Others"]

        files_report , total_files = move_files(folder_path , files_report , others_folder , folder)

        create_report(REPORT_FILE_PATH , files_report , total_files)

    else:
        print("Folder path not found")

if __name__ == "__main__":
    main()