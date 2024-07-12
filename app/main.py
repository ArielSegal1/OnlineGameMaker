# Install the necessary packages
# pip install fastapi uvicorn pyinstaller
import shutil

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import subprocess
import os
from pathlib import Path
import re

app = FastAPI()


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


def clean(exe_file, script_stem):
    if exe_file.exists():
        os.remove(exe_file)
    spec_file = Path(script_stem + ".spec")
    if spec_file.exists():
        os.remove(spec_file)
    build_dir = Path("build") / script_stem
    if build_dir.exists():
        shutil.rmtree(build_dir)


@app.get("/convert-to-exe/")
async def convert_to_exe(speed: str):
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
    modify(modified_script_path, "player_speed = 5", f"player_speed = {speed}")

    # Run pyinstaller to create the executable
    exe_dir = "dist"
    script_stem = Path(modified_script_path).stem
    exe_file = Path(exe_dir) / (script_stem + ".exe")
    clean(exe_file, script_stem)
    # print(exe_file)

    subprocess.run(["pyinstaller", "--onefile", modified_script_path], check=True)

    # Check if exe file is created and return it
    if exe_file.exists():
        file_respond = FileResponse(exe_file, filename=exe_file.name)
        return file_respond

    raise HTTPException(status_code=500, detail="Failed to create executable")
