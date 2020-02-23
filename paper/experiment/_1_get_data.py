# -*- coding: utf-8 -*-
import io
import os
import shutil
import zipfile
import requests
import subprocess


def download_and_extract_zip(zip_url):
    r = requests.get(zip_url)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall()


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
            os.mkdir(data_folder + emotion)

        except BaseException:
            print("Ecxception raised: ", data_folder + emotion,
                  "could not be created ...")

    # get all filenames
    file_paths = [waves_folder + f for f in os.listdir(waves_folder)]

    for file_path in file_paths:
        file_name = file_path.split("/")[-1]
        emotion = emotions_list[file_name[-6]] + "/"
        # copy file to associcated destination
        shutil.copyfile(file_path, data_folder + emotion + file_name)


def prepare_data(zip_url = "http://emodb.bilderbar.info/download/download.zip"):
    # download and extract data
    download_and_extract_zip(zip_url)

    # remove un-needed folders and files
    _ = subprocess.Popen(["rm", "-rf", "lablaut", "labsilb", "silb"],
                          stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE)
    _ = subprocess.Popen(["rm", "-f", "erklaerung.txt", "erkennung.txt"],
                      stdin=subprocess.PIPE,
                      stdout=subprocess.PIPE,
                      stderr=subprocess.PIPE)
    # organize data
    if not os.path.exists("data/waves/") :
        os.mkdir("data/waves/")
    manage("wav/", "data/waves/")
    _ = subprocess.Popen(["rm", "-rf", "wav"], stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
