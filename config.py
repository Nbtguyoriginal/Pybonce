# --------------------------
# Configuration for pyreader.py
# --------------------------
# Program by: Tcoder
# Free to use upgrade change or distribute with credit given to 
# Credit: https://github.com/Nbtguyoriginal/Pybonce

#---------------------------------------------------------------------------------------------------------------------------------------------
# OpenAI Configuration   
# OpenAI API Key
API_KEY = 'key here'

LINES_PER_API_CALL = 10  # Number of lines to send to OpenAI API in a single call

# UI Configuration
HIGHLIGHT_COLOR = '#FF33A1'  # Color used to highlight specific lines in the analysis log
SENDING_COLOR = '#FFA1A1'  # Light red
ANALYSIS_COLOR = '#83C1A1'  # Aquamarine
TITLE_COLOR = '#FFFFE0'     # lightyellow

# Logging Configuration
LOG_FILE = 'audit.txt'  
# File where the analysis log is saved

#use the first instance of the log name 
#ex "better_code": "Better_code", you use "beter_code" here--- CURRENT_LOG_TYPE = LOG_TYPES["beter_code"]
# this will return a log with  Suggestions for code improvements 
#be sure to change your log file name to refelct the type of log your makng for easy orginization 

# Define different types of logs
LOG_TYPES = {
    "default": "Default",  # General-purpose logs
    "modifications": "Possible_mods",  # Logs related to changes or modifications
    "General_notes": "General_notes",  # General remarks or observations
    "Detailed_notes": "Detailed_notes",  # In-depth remarks or observations
    "better_code": "Better_code",  # Suggestions for code improvements
    "error": "Error",  # Logs for error events
    "warning": "Warning",  # Logs for warning events
    "info": "Information",  # General informational logs
    "debug": "Debug",  # Logs used for debugging purposes
    "critical": "Critical",  # Logs for critical events
    "authentication": "Authentication",  # Logs related to user authentication
    "authorization": "Authorization",  # Logs related to user permissions
    "database": "Database",  # Logs related to database operations
    "network": "Network",  # Logs related to network operations
    "performance": "Performance",  # Logs related to performance metrics
    "audit": "Audit",  # Logs for auditing purposes
    "backup": "Backup",  # Logs related to data backups
    "maintenance": "Maintenance",  # Logs related to system maintenance
    "startup": "Startup",  # Logs generated at system startup
    "shutdown": "Shutdown",  # Logs generated at system shutdown
    "configuration": "Configuration",  # Logs related to system configurations
    "deprecation": "Deprecation",  # Logs related to deprecated features
    "migration": "Migration",  # Logs related to data migration
    "user_activity": "User_Activity",  # Logs related to user actions
    "system_activity": "System_Activity",  # Logs related to system actions
    "security": "Security",  # Logs related to security events
    "access": "Access",  # Logs related to resource access
    "transaction": "Transaction",  # Logs related to transactions
    "synchronization": "Synchronization",  # Logs related to data synchronization
    "communication": "Communication",  # Logs related to system communications
    "service": "Service",  # Logs related to services or daemons
    "resource": "Resource",  # Logs related to resource usage
    "cache": "Cache",  # Logs related to caching operations
    "schedule": "Schedule",  # Logs related to scheduled tasks
    "update": "Update",  # Logs related to updates or patches
    "deletion": "Deletion",  # Logs related to data deletion
    "creation": "Creation",  # Logs related to data creation
    "validation": "Validation"  # Logs related to data validation
}


# Set the current log type
CURRENT_LOG_TYPE = LOG_TYPES["audit"]

WARP_ITERATIONS = 3  # Number of times the warp process should iterate
WARP_RULES = "Your specific warp rules or criteria here"
#warp rules iterative generation 

# Specify the method to use: 'combine', 'sequential', or 'selective' -- explained below 
WARP_METHOD = 'sequential'  # Change this to your desired method


WARP_RULES_SET_1 = """
1. Identify any loops that can be optimized using list comprehensions or Python's built-in functions.
2. Highlight any hard-coded values and suggest moving them to constants or configuration files.
3. Check for the use of deprecated libraries or functions and recommend modern alternatives.
4. Point out any lack of error handling, especially around external API calls or file operations.
5. Suggest improvements for code readability, such as breaking long functions into smaller, more manageable pieces.
"""

WARP_RULES_SET_2 = """
1. Look for potential security vulnerabilities, especially in user input handling or database operations.
2. Recommend the use of logging for critical operations to aid in debugging and monitoring.
3. Identify areas where parallel processing or threading might speed up execution.
4. Check for consistent naming conventions and adherence to PEP 8 standards.
5. Highlight any potential memory leaks or resource-intensive operations.
"""

WARP_RULES_SET_3 = """
1. Assess the modularity of the code and suggest ways to improve code reusability.
2. Point out any missed opportunities for using object-oriented principles.
3. Recommend ways to improve the user experience, such as better prompts or error messages.
4. Check for potential race conditions or concurrency issues.
5. Suggest improvements in data structures used for better efficiency.
"""

WARP_RULES_SET_4 = """
1. Identify any potential bottlenecks in the code that could slow down execution.
2. Highlight areas where unit tests or integration tests might be beneficial.
3. Check for the use of magic numbers and suggest replacing them with named constants.
4. Assess the clarity of comments and suggest improvements where necessary.
5. Recommend ways to make the code more scalable and maintainable.
"""

WARP_RULES_SET_5 = """
1. Point out any areas where exception handling is too broad or too specific.
2. Suggest the use of design patterns where they might be beneficial.
3. Check for any potential issues with data integrity or persistence.
4. Recommend ways to improve user input validation and sanitation.
5. Highlight any areas where the code might not be cross-platform compatible.
"""

WARP_RULES_SET_6 = """
1. Assess the efficiency of database queries and suggest optimizations.
2. Point out any potential issues with file handling, especially regarding file permissions or file locks.
3. Recommend the use of environment variables for sensitive information instead of hard-coding.
4. Check for any potential issues with third-party library versions or dependencies.
5. Suggest ways to make the code more readable for new developers.
"""

WARP_RULES_SET_7 = """
1. Highlight areas where the code might benefit from lazy loading or caching.
2. Check for the correct use of global variables and suggest alternatives.
3. Assess the potential for code injection attacks and recommend preventative measures.
4. Recommend ways to improve the structure of the codebase, such as directory structure or module organization.
5. Point out any areas where the code might be over-engineered or too complex.
"""

WARP_RULES_SET_8 = """
1. Suggest improvements for better integration with other systems or APIs.
2. Check for the correct handling of date and time operations, considering time zones.
3. Highlight any potential issues with multithreading or multiprocessing.
4. Assess the clarity and usefulness of debug messages or logs.
5. Recommend ways to improve the efficiency of data processing operations.
"""

WARP_RULES_SET_9 = """
1. Point out any potential issues with Unicode or character encoding.
2. Suggest improvements for better error recovery or graceful degradation.
3. Check for the potential misuse of recursion or potential for stack overflow.
4. Highlight any areas where the code might be making unnecessary computations.
5. Recommend ways to improve the user interface or user experience.
"""

WARP_RULES_SET_10 = """
1. Assess the potential for floating-point errors or precision issues.
2. Point out any areas where the code might be vulnerable to denial-of-service attacks.
3. Check for the correct handling of network operations, considering timeouts and retries.
4. Suggest improvements for better documentation or code comments.
5. Highlight any potential issues with backward compatibility or versioning.
"""
# If using the 'selective' method, specify which sets to use
SELECTED_WARP_SETS = [WARP_RULES_SET_1, WARP_RULES_SET_2]
#----------------------------------------------------------------------------------------------------------------------------------------------

# ==================== USER INFORMATION ====================
# Do not modify anything below this point. This section is for user information only.

# ------------------- API Call Configuration -------------------
# It's recommended to set "/lines_per_api_call/" to a minimum of "10" for optimal results.
# If your code isn't well described in the log or GUI, consider adjusting this value.
# However, setting it below "10" is not advised for compact code or small scripts.
#setting bellow 10 can break the script or cost hundreds of dollars for very small code bases 

# ------------------- WARP_METHOD Configuration -------------------
# This setting determines how the warp rules are applied during code analysis:
# - 'combine': Merges all specified warp rule sets for a comprehensive analysis. -- this can result in huge rule sets depending on your usage 
# - 'sequential': Applies each warp rule set one after the other in their listed order. -- typically the most user friendly but also the most cost intensive 
# - 'selective': Uses only the specific warp rule set assigned to WARP_RULES. -- fine graind control over deliverd rules 
# To choose a method, set WARP_METHOD to 'combine', 'sequential', or 'selective'.

# ------------------- Warp Rules Overview -------------------
# Warp rules offer precise line-by-line code analysis. Using a single set provides fine-grained control, 
# while multiple sets enhance analysis depth and precision. Each rule set should be centered around a guiding question for consistency.

# Guiding Questions for Each Rule Set:
# WARP_RULES_SET_1: "How can we optimize the code for performance and readability?"
# WARP_RULES_SET_2: "What measures enhance the code's security and efficiency?"
# WARP_RULES_SET_3: "How can we improve code modularity and user experience?"
# WARP_RULES_SET_4: "What ensures the code is maintainable and scalable?"
# WARP_RULES_SET_5: "How to ensure robustness and cross-platform compatibility?"
# WARP_RULES_SET_6: "Best practices for database interactions and readability?"
# WARP_RULES_SET_7: "Optimizing code structure and reducing complexity?"
# WARP_RULES_SET_8: "Improving code integration capabilities and data processing?"
# WARP_RULES_SET_9: "Enhancing code resilience and user interface?"
# WARP_RULES_SET_10: "Ensuring precision and compatibility in the code?"

# Adjust the rules and guiding questions to fit your specific needs and context.

# --------------------------
# Configuration notes for pyreader.py
# --------------------------



# Note: setting the "lines_per_api_call" any lower than "10" is not advised unless your code is very compact or you have a very small script.

# The default amount for best functions is "10", but adjust this number if you find your code is not well described in the log or GUI.
# Feel free to fork this repository and add other functions as it was coded quickly.


# setting the "lines_per_api_call" any lower then "10" is not advised unless your code is very compact or you have a very small script

# the Default ammount for best functions is "10" but adjust this number if you find your code is not well described in the log enough or gui

# Feel free to fork this reposstitory and add other Functions as I coded this pretty quick
