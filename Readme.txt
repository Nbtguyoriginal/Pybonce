# --------------------------
# README for pyreader
# --------------------------

# Overview:
# pyreader.py is a Python script analyzer. It leverages OpenAI's API to review Python code, 
# providing insights on performance, style, security, and functionality. The analysis results 
# are presented in a user-friendly GUI. Thats Highlighted in a way to define the area of context

# Use Cases:
# - Code Review: Quickly get feedback on Python scripts without manual review.
# - Learning: Understand best practices and potential pitfalls in Python code.
# - Security Audits: Identify potential security vulnerabilities in your Python scripts.
# - Codebase Audits: Get an overview of the quality and potential issues in a large codebase.
Dont message me for help unless you read this and it sitll did not work!

# Installation:
# 1. Ensure you have Python 3.x installed.
# 2. Clone or download the repository to your local machine.
# 3. Navigate to the directory and install the required packages using `pip install -r requirements.txt`.
# 4. Update the `config.py` file with your OpenAI API key.
# 5. Run the script using `python pyreader.py`.

# Features:
# - Directory Selection: Users can select a directory containing Python files. The directory's 
#   tree structure is displayed in the GUI, but individual Python files only appear after selection.
# - Code Analysis: On clicking "Start Analysis", the program sends the code to OpenAI for review. 
#   The feedback is then displayed in the GUI.
# - Abort Option: Users can abort the analysis process if needed.
# - Logging: All analysis results are also saved to a specified log file for future reference.

# Configuration Details:
# - API_KEY: Key for authenticating with OpenAI's API.
# - LINES_PER_API_CALL: Specifies how many lines of a Python file are sent to OpenAI in one API call.
# - HIGHLIGHT_COLOR: Defines the color used to highlight specific lines in the analysis log.
# - LOG_FILE: Specifies the name of the file where the analysis log is saved.

# Usage:
# 1. Run pyreader.py.
# 2. Use the GUI to select a directory containing Python files. The tree view will populate post-selection.
# 3. Click "Start Analysis" to initiate the code review. The results will be displayed in the GUI and saved to the log file.

# Cost Implications:
# Each API call incurs a cost based on the number of tokens processed. Given that codebases can be extensive, 
# and the specified number in "LINES_PER_API_CALL" can lead to multiple API calls, costs can accumulate. 
# It's recommended to group API calls to encompass entire functions and keep the line count below 50. 
# Remember, the script also requires some completion space to analyze the code and provide comprehensive feedback.
# The pyreader script has built in functions for recursion prevention as well as a system for self improvement of code 