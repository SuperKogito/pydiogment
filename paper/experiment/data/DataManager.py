import os
import shutil


def manage(waves_folder, data_folder):
    """
    organise the emotions folder.
    """
    # define emotions list
    emotions_list = {"W": "anger", "L": "boredom", "E": "disgust",
                     "A": "fear", "F": "happiness", "T": "sadness",
                     "N": "neutral"}

    # create emotions folders
    for emotion in emotions_list.values():
        # create a folder for the data
        try:
            os.mkdir(data_folder + emotion)
            print(data_folder + emotion, "was created ...")
            os.mkdir(data_folder + emotion + "/wave")

        except BaseException:
            print("Ecxception raised: ", data_folder + emotion,
                  "could not be created ...")

    # get all filenames
    file_paths = [waves_folder + f for f in os.listdir(waves_folder)]

    for file_path in file_paths:
        file_name = file_path.split("/")[-1]
        emotion = emotions_list[file_name[-6]] + "/"
        # copy file to associcated destination
        shutil.copyfile(file_path, data_folder + emotion + "wave/" + file_name)

if __name__ == "__main__":
    manage("../download/wav/", "../data/")
