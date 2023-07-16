import subprocess

# Path to the Blender's Python interpreter
#blender_executable_path= "C:\\Program Files\\Blender Foundation\\Blender 3.6\\blender.exe"

# Path to the Python script you want to run
script_path = "conversion3.py"

# Run the subprocess command
subprocess.run(["blender", "--background", "--python", script_path])
