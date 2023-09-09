# --------------------------
# Configuration for pyreader.py
# --------------------------

# OpenAI Configuration
API_KEY = ''  # OpenAI API Key
LINES_PER_API_CALL = 20  # Number of lines to send to OpenAI API in a single call # 1 is a 1 to 1 conversion of lines to tokens 

# UI Configuration
HIGHLIGHT_COLOR = '#FF33A1'  # Color used to highlight specific lines in the analysis log Different colors in Color_codes.txt
SENDING_COLOR = '#FFA1A1' #- Light red
ANALYSIS_COLOR = '#83C1A1'  # Aquamarine
TITLE_COLOR = '#FFFFE0'     # lightyellow


# Logging Configuration
LOG_FILE = 'Oompa_loompa.txt'  # File where the analysis log is saved


# setting the "lines_per_api_call" any lower then "10" is not advised unless your code is very compact or you have a very small script

# the Default ammount for best functions is "10" but adjust this number if you find your code is not well described in the log enough or gui
# Feel free to fork this reposstitory and add other Functions as i coded this pretty quick