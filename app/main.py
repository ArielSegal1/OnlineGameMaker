# # Install the necessary packages
# # pip install fastapi uvicorn pyinstaller
import shutil
#
from fastapi import FastAPI, HTTPException, Query, File, UploadFile, BackgroundTasks
from fastapi.responses import FileResponse

import subprocess
import os
from pathlib import Path
import re
import zipfile

app = FastAPI()


#
#

def handle_file(file: UploadFile = File(...)):
    with open(file.filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return file.filename


def modify(filepath, from_, to_):
    file = open(filepath, "r+")
    text = file.read()
    pattern = from_
    splitted_text = re.split(pattern, text)
    modified_text = to_.join(splitted_text)
    with open(filepath, 'w') as file:
        file.write(modified_text)


def move_to_directory(paths: list):
    directory_path = r"C:\Users\Ariel\Documents\StartupPython\OnlineGameMaker\temp_directory"
    os.mkdir(directory_path)
    for path in paths:
        shutil.move(rf"C:\Users\Ariel\Documents\StartupPython\OnlineGameMaker\dist", directory_path)


def clean(exe_file, script_stem, zip_file):
    if exe_file.exists():
        os.remove(exe_file)
    spec_file = Path(script_stem + ".spec")
    if spec_file.exists():
        os.remove(spec_file)
    build_dir = Path("build") / script_stem
    if build_dir.exists():
        shutil.rmtree(build_dir)
    z_f = Path(zip_file + ".zip")
    if z_f.exists():
        os.remove(z_f)


def clean_png(png_path):
    p_f = Path(png_path)
    if p_f.exists():
        os.remove(p_f)



@app.post("/convert-to-exe/")
async def convert_to_exe(speed: str, f: UploadFile = File(...)):
    # Define the path to the Python script within the project directory
    script_path = r"C:\Users\Ariel\Documents\StartupPython\OnlineGameMaker\miniGame.py"  # Adjust this path accordingly

    # Check if the script exists
    if not os.path.isfile(script_path):
        raise HTTPException(status_code=404, detail="Script file not found")

    with open(script_path, "r") as file:
        script_content = file.read()

    modified_script_path = "temp/modified_script.py"
    os.makedirs(os.path.dirname(modified_script_path), exist_ok=True)
    with open(modified_script_path, "w") as file:
        file.write(script_content)
    f_name = handle_file(f)
    modify(modified_script_path, "player_speed = 5", f"player_speed = {speed}")
    modify(modified_script_path, "player2.png",f_name)
    # modify(modified_script_path, 'original_player_image = pygame.image.load("player2.png)',
    #        f'original_player_image = pygame.image.load("{test(file)}")')

    # Run pyinstaller to create the executable
    exe_dir = "dist"
    script_stem = Path(modified_script_path).stem
    exe_file = Path(exe_dir) / (script_stem + ".exe")
    clean(exe_file, script_stem, "temp_output")
    # print(exe_file)

    subprocess.run(
        ["pyinstaller", "--onefile",
         "--add-data=" + rf"C:\Users\Ariel\Documents\StartupPython\OnlineGameMaker\{f_name};.",
         modified_script_path], check=True)

    # shutil.move(r"C:\Users\Ariel\Documents\StartupPython\GameManipulationsApiTests\player2.png",
    #             r"C:\Users\Ariel\Documents\StartupPython\OnlineGameMaker\dist\player2.png")

    # Check if exe file is created and return it
    if exe_file.exists():
        temp_dir = Path("temp_output")
        temp_dir.mkdir(exist_ok=True)

        shutil.copy(exe_file, temp_dir)
        shutil.copy(rf"C:\Users\Ariel\Documents\StartupPython\OnlineGameMaker\{f_name}", temp_dir)
        shutil.copy(rf"C:\Users\Ariel\Documents\StartupPython\OnlineGameMaker\{f_name}", exe_dir)
        clean_png(f_name)
        zip_path = Path("temp_output.zip")
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file in temp_dir.iterdir():
                zipf.write(file, file.name)
        shutil.rmtree(temp_dir)
        return FileResponse(zip_path, filename=zip_path.name)

    raise HTTPException(status_code=500, detail="Failed to create executable")
