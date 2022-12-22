import os
import zipfile
import sys
import datetime

GAME_CONFIG = {
    "high-on-life": {
        # "deck_directory": "/home/deck/.steam/steam/steamapps/compatdata/2952202951/pfx/drive_c/users/steamuser/AppData/Local/Oregon/Saved/SavedGames",
        "deck_directory": "/Users/hong-gyulee/Projects/testdata",
        "pc_directory": "C:\\Users\\hongg\\AppData\\Local\\Oregon\\Saved\\SavedGames"
    },
}

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, _, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))


def uploadSaves(game, save_location, system):
    repo_dir = os.path.join('saves', game)
    if not os.path.exists(repo_dir):
        os.mkdir(repo_dir)

    # get the current time
    now = datetime.datetime.now()

    # get the files in the directory and create a zip file
    now_string = now.strftime(f"%Y-%m-%d_%H-%M-%S_{system}")
    # create a new directory with the current time as the name
    os.mkdir(os.path.join(repo_dir, now_string))
    
    zip_name = os.path.join(repo_dir, now_string, 'backup.zip')

    print(f"creating zip file {zip_name}")
    zipf = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)
    zipdir(save_location, zipf)
    zipf.close()

    # get the current time
    now = datetime.datetime.now()
    
    # commit the changes to git and push
    os.system("git add .")
    os.system(f"git commit -m 'backup from deck at {now_string}'")
    os.system("git push")

def downloadSaves(game, save_location):
    # pull the repo
    print("getting latest saves...")
    os.system("git pull")

    # get the latest zip file from game dir
    repo_dir = os.path.join('saves', game)
    latest_zip = os.path.join(repo_dir, sorted(os.listdir(repo_dir))[-1], 'backup.zip')
    print(f"getting latest save file: {latest_zip}")

    # unzip the file and replace the files in the directory
    print(f"extracting to {save_location}")
    with zipfile.ZipFile(latest_zip, 'r') as zip_ref:
        zip_ref.extractall(save_location)

    print("done")

if __name__ == "__main__":
    # usage: python3 save_manager.py [deck/pc] [upload/download] [game]
    system = sys.argv[1]
    action = sys.argv[2]
    game = sys.argv[3]

    save_location = None
    if system == "deck":
        save_location = GAME_CONFIG[game]["deck_directory"]
    elif system == "pc":
        save_location = GAME_CONFIG[game]["pc_directory"]
    else:
        print("System not found")
        sys.exit(1)
    
    if game not in GAME_CONFIG:
        print("Game not found")
        sys.exit(1)
    
    if action == "upload":
        uploadSaves(game, save_location, system)
    elif action == "download":
        downloadSaves(game, save_location)
    else:
        print("Action not found")
        sys.exit(1)






