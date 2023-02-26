import os
from datetime import datetime
import requests
from win10toast import ToastNotifier

# Replace this with the link to the GitHub repository
github_repo_link = "YOUR GITHUB REPOSITORY LINK"

# Get the repository name and owner from the GitHub repository link
repo_name = github_repo_link.split("/")[-1]
owner_name = github_repo_link.split("/")[-2]

# Replace this with the folder name in %appdata% where the Mods should be stored
appdata_folder_name = ".minecraft\\mods"

# Get the list of Mods in the GitHub repository
response = requests.get(f"https://api.github.com/repos/{owner_name}/{repo_name}/contents")
Mod_names = [Mod["name"] for Mod in response.json()]

# Get the list of Mods in the appdata folder
appdata_folder_path = os.path.join(os.getenv('APPDATA'), appdata_folder_name)
appdata_Mod_names = os.listdir(appdata_folder_path)

# Delete Mods in the appdata folder that are not in the repository and end with .jar
removed_Mods = []
for Mod_name in appdata_Mod_names:
    if Mod_name.endswith(".jar") and Mod_name not in Mod_names:
        os.remove(os.path.join(appdata_folder_path, Mod_name))
        removed_Mods.append(Mod_name)

# Save the names of the removed Mods and the timestamp to a Mod
if removed_Mods:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("RemovedMods_LOG.txt", "a") as f:
        f.write(f"{timestamp}: {', '.join(removed_Mods)}\n")
        print(f"Removed Mods: {removed_Mods}")
        toast = ToastNotifier()
        toast.show_toast("Mods Removed", f"The following Mods have been Removed:\n{', '.join(removed_Mods)}")

# Check if all the Mods in the repository exist in the appdata folder
if set(Mod_names) == set(appdata_Mod_names):
    print("All Mods in the repository exist in the appdata folder")
else:
    missing_Mods = set(Mod_names) - set(appdata_Mod_names)
    if str(missing_Mods) == "set()":
        print(f"No mods Missing")
    else:
        print(f"The following Mods are missing from the appdata folder: {missing_Mods}")
        # Download the missing Mods from the GitHub repository
        downloaded_Mods = []
        for Mod_name in missing_Mods:
            download_url = f"https://raw.githubusercontent.com/{owner_name}/{repo_name}/main/{Mod_name}"
            response = requests.get(download_url)
            with open(os.path.join(appdata_folder_path, Mod_name), 'wb') as f:
                f.write(response.content)
            downloaded_Mods.append(Mod_name)
        print("Missing Mods downloaded successfully")
        # Save the names of the downloaded Mods and the timestamp to a Mod
        if downloaded_Mods:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open("DownloadedMods_LOG.txt", "a") as f:
                f.write(f"{timestamp}: {', '.join(downloaded_Mods)}\n")
            # Display a Windows toast notification with the names of the downloaded Mods
            toast = ToastNotifier()
            toast.show_toast("Mods downloaded", f"The following Mods have been downloaded:\n{', '.join(downloaded_Mods)}")
            
input("Press Enter to exit...")

