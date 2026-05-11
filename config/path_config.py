from pathlib import Path

PROJECT_ROOT =  Path(__file__).resolve().parents[1]
ASSETS_DIR = PROJECT_ROOT / "assets" / "images"
ACTION_DIR = PROJECT_ROOT / "actions"

CHAR_SHEET   = PROJECT_ROOT / "assets" / "images" / "characters" / "characters.png"
MAP_IMAGE    = PROJECT_ROOT / "assets" / "images" / "background" / "land" / "test-land.png"

# Path relative to this file
#_SHEET_PATH = os.path.join(os.path.dirname(__file__), "assets", "characters", "characters.png") #this is not the best way to locate file
#_SHEET_PATH = (Path(__file__).parent.parent / "assets"/ "characters"/ "characters.png") #this is the best way to locate file

'''
this is the way without path config
_SHEET_PATH = (Path(__file__).parent.      #in action
        parent                             #in project_root
        / "assets"   
        / "characters"
        / "characters.png")

'''