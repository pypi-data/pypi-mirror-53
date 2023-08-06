import os
import shutil
import my_package

DESKTOP_FOLDER = get_special_folder_path("CSIDL_DESKTOPDIRECTORY")
NAME = "Mangrove"

if sys.argv[1] == '-install':
	create_shortcut(
		target=os.path.join(sys.prefix, 'python.exe') + " " + os.path.join(os.path.dirname(my_package.__file__), "mgvUI.py"),
		description="Mangrove UI",
		filename=NAME,
		workdir=DESKTOP_FOLDER,
		iconpath=os.path.join(os.path.dirname(my_package.__file__),"icons","mgv.ico")

	shutil.move(os.path.join(os.getcwd(), NAME), os.path.join(DESKTOP_FOLDER, NAME))
	file_created(os.path.join(DESKTOP_FOLDER, NAME))

if sys.argv[1] == '-remove':
    pass
