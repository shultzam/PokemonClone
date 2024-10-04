import requests
import re
import os
import os.path

# This script will download all files from the URLs/URLs.txt and put them in Downloads directory
downloadDir = "downloads/"

ReDownloadOnlyCorruptedFiles = None
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


def Download(FileName, url, response):
    with open(FileName, "wb") as file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)
        print("Downloaded: " + url)


def download_from_list(file_path: str, output_dir: str):
    # Make sure the destination dir exists.
    os.makedirs(os.path.dirname(output_dir), exist_ok=True)

    # Read in the URL list.
    f = open(file_path, "r")
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
            fileToDownload = output_dir + id + ".png"
            response = requests.get(url, stream=True)
            if not ReDownloadOnlyCorruptedFiles:
                Download(fileToDownload, url, response)  # (Re-)Download all files unconditionally
            elif os.path.exists(fileToDownload):
                file_stat = os.stat(fileToDownload)
                if file_stat.st_size < 1000:
                    Download(fileToDownload, url, response)  # Re-download only corrupted files
            else:
                Download(fileToDownload, url, response)  # Download new file
        except AttributeError:
            print("An Error Occured for URL: {}".format(url))

# Try to download all of the URL lists. Other than URLs.txt, which is updated via the ImageScrapper, the other lists are wildly outdated.
download_from_list(file_path="URLs/URLs.txt", output_dir="downloads/URLs/")
download_from_list(file_path="URLs/FormURLs.txt", output_dir="downloads/forms/")
download_from_list(file_path="URLs/ExceptionalURLs.txt", output_dir="downloads/exceptional_urls/")