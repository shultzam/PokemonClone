import requests
import re
import os.path

# This script will download all files from the URLs/URLs.txt and put them in Downloads directory
downloadDir = "downloads/"

while True:
    response = input("Redownload All files ?(Y,N): ")
    if response in ["Y", "y"]:
        ReDownloadOnlyCorruptedFiles = False
        break
    if response in ["n", "n"]:
        ReDownloadOnlyCorruptedFiles = True
        # Re-download only corrupted files (sometimes <1kb corrupted files are downloaded from Bulbapedia)
        print("Only new/ corrupted files will be downloaded")
        break


def Download(FileName):
    with open(FileName, "wb") as file:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)
        print("Downloaded: " + url)


f = open("URLs/URLs.txt", "r")
Lines = f.readlines()
URLs = []
for line in Lines:
    URLs.append(line.strip())  # Stripping the newline character
f.close()

# Downloading
for url in URLs:
    try:
        id = re.search(r"/\d\d\d\d", url).group(0)
        id = id[1:]
        fileToDownload = downloadDir + id + ".png"
        r = requests.get(url, stream=True)
        if not ReDownloadOnlyCorruptedFiles:
            Download(fileToDownload)  # (Re-)Download all files unconditionally
        elif os.path.exists(fileToDownload):
            file_stat = os.stat(fileToDownload)
            if file_stat.st_size < 1000:
                Download(fileToDownload)  # Re-download only corrupted files
        else:
            Download(fileToDownload)  # Download new file
    except AttributeError:
        print("An Error Occured for: " + id)
