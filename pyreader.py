import os
import tkinter as tk
from tkinter import filedialog, Text, messagebox, simpledialog, ttk
import openai
import threading
import config
from tkinter.ttk import Progressbar
import webbrowser
import shutil
from PyCells import Brain_matter


openai.api_key = config.API_KEY
brain_matter = Brain_matter()


class AnalysisState:
    def __init__(self):
        self.current_thread = None
        self.abort_event = threading.Event()
        self.analyzed_files = set()


state = AnalysisState()

def start_time_warp_analysis_in_thread():
    directory = filedialog.askdirectory()
    if directory:  # Check if a directory was selected
        threading.Thread(target=time_warp_analysis, args=(directory,)).start()
    # Save a memory when Time Warp function is triggered
    memory.save_memory("Time Warp analysis started for directory: " + directory)
    
def setup_text_tags():
    analysis_text.tag_configure('sending', background=config.SENDING_COLOR, font=("Arial", 10))
    # Save a memory for 'sending' tag configuration
    memory.save_memory("Configured 'sending' tag with background color: " + config.SENDING_COLOR)

    analysis_text.tag_configure('analysis', background=config.ANALYSIS_COLOR, font=("Arial", 10))
    # Save a memory for 'analysis' tag configuration
    memory.save_memory("Configured 'analysis' tag with background color: " + config.ANALYSIS_COLOR)

    analysis_text.tag_configure('title', background=config.TITLE_COLOR, font=("Arial", 10, 'bold'))
    # Save a memory for 'title' tag configuration
    memory.save_memory("Configured 'title' tag with background color: " + config.TITLE_COLOR)

    analysis_text.tag_configure('highlight', background=config.HIGHLIGHT_COLOR, font=("Arial", 10))
    # Save a memory for 'highlight' tag configuration
    memory.save_memory("Configured 'highlight' tag with background color: " + config.HIGHLIGHT_COLOR)



def select_directory():
    folder_selected = filedialog.askdirectory()
    if not folder_selected:
        messagebox.showerror("Error", "No directory selected.")
        # Save a memory for the error when no directory is selected
        memory.save_memory("User attempted to select a directory but did not choose any.")
        return
    load_treeview(folder_selected)
    # Save a memory for the successful directory selection
    memory.save_memory(f"User successfully selected the directory: {folder_selected}")



def load_treeview(directory):
    for i in tree.get_children():
        tree.delete(i)
    populate_tree(tree, directory)


def populate_tree(tree, parent_path, parent=""):
    for entry in os.scandir(parent_path):
        oid = tree.insert(parent, "end", text=entry.name, open=False)
        if entry.is_dir():
            populate_tree(tree, entry.path, oid)


def write_log(content, log_type=config.LOG_TYPES["default"]):
    if log_type == config.LOG_TYPES["default"]:
        log_filename = config.LOG_FILE
    else:
        log_filename = f"{log_type}_log.txt"

    with open(log_filename, "a") as log_file:
        log_file.write(content + "\n\n")
        
    # Save a memory for the log entry written
    memory.save_memory(f"Log entry written to {log_filename}. Content: {content[:50]}...")  # Saving only the first 50 characters for brevity
    # Save a memory for the type of log written
    memory.save_memory(f"Log type used: {log_type}")



def create_help_button(parent):
    def open_discord_invite():
        webbrowser.open('https://discord.gg/RxUAFDmubs')

    def open_help_menu():
        # Create a new window for the help menu
        help_window = tk.Toplevel(parent)
        help_window.title("Help Menu")
        
        # Function to display information when a tab is clicked
        def display_info(tab_number):
            info = {
                1: 'Pybonce is an intuitive Python code analysis tool designed to enhance the quality and efficiency of your scripts. By leveraging advanced AI capabilities, Pybonce offers in-depth insights into your code\'s performance, style, security, and functionality. With its user-friendly GUI, Pybonce allows users to easily select directories for analysis, view detailed feedback, and even apply specialized "warp rules" for customized code evaluations. Whether you\'re a seasoned developer or just starting out, Pybonce provides valuable feedback to elevate your coding skills and produce optimal Python scripts.', 
                2: 'simple explanation: In Pybonce, users select a directory with Python scripts for analysis, then the tool reads the scripts, sending code segments to an advanced AI model which evaluates the code on criteria like performance, style, security, and functionality, providing detailed feedback; users can further refine this analysis using "warp rules" for a tailored experience, and the resulting feedback is displayed in the GUI, highlighting key areas and insights, all while tracking the number of tokens processed by the AI to inform users of the computational cost. -Your code ---> pybonce agent--internal analysis-->external analysis---returned info---> visual log---->physical log ',
                3: 'Warp rules, integral to Pybonce\'s analytical capabilities, are meticulously crafted guidelines designed to facilitate a granular examination of code. By enabling users to zoom in on distinct facets of their scripts, be it performance optimization, security vulnerabilities, coding style, or functionality enhancements, these rules offer a bespoke analysis experience. The astute implementation of warp rules is paramount. When thoughtfully configured, they not only streamline the evaluation process but also ensure that the feedback generated is both pertinent and actionable. Instead of inundating users with generic or overly broad recommendations, a well-implemented warp rule system provides insights that directly align with a coder\'s unique objectives and priorities, making it an invaluable tool for refining and perfecting code.',
                4: 'Logging features in Pybonce serve as a comprehensive record-keeping mechanism, meticulously documenting every facet of the code analysis journey. These features capture the AI\'s feedback, segmenting it into distinct categories such as notes, modifications, and general observations. By maintaining a detailed chronicle of the AI\'s evaluations, users can effortlessly trace back to specific recommendations, understand the rationale behind them, and gauge the evolution of their code over time. Moreover, the logging system is not just a passive recorder; it\'s an active tool that aids in debugging, offers insights into recurring issues, and provides a structured format for future reference. When utilized effectively, these logging capabilities transform the ephemeral nature of feedback into a lasting resource, ensuring that users can continually leverage past insights to inform future coding decisions.',
                # ... add more tabs as needed
            }
            messagebox.showinfo(f"Information Tab {tab_number}", info[tab_number])


        # Add clickable information tabs
        tk.Button(help_window, text="Pybonce", command=lambda: display_info(1)).pack(pady=10)
        tk.Button(help_window, text="How Pybonce works", command=lambda: display_info(2)).pack(pady=10)
        tk.Button(help_window, text="Warp rules", command=lambda: display_info(2)).pack(pady=10)
        tk.Button(help_window, text="Logs and stuff", command=lambda: display_info(2)).pack(pady=10)
        # ... add more tabs as needed

    # Create the help button
    help_button = tk.Menubutton(parent, text="Help", relief=tk.RAISED)
    help_button.grid(row=0, column=4, padx=10, pady=10)

    # Create the dropdown menu
    help_menu = tk.Menu(help_button, tearoff=0)
    help_button.configure(menu=help_menu)

    # Add options to the dropdown menu
    help_menu.add_command(label="Get Socials", command=open_discord_invite)
    help_menu.add_command(label="Help Menu", command=open_help_menu)

    return help_button

def start_analysis():
    directory = filedialog.askdirectory()
    if not directory:
        return
    state.abort_event.clear()
    state.current_thread = threading.Thread(target=process_directory, args=(directory,))
    state.current_thread.start()
    abort_button.config(state=tk.DISABLED)
    # Save a memory when analysis starts
    memory.save_memory("Analysis started for directory: " + directory)



def process_directory(directory):
    python_files = [f for f in os.listdir(directory) if f.endswith('.py')]

    total_tokens_used = 0
    total_estimated_cost = 0.0

    # Initialize the progress bar
    progress_var = tk.DoubleVar()
    progress_bar = Progressbar(root, variable=progress_var, maximum=len(python_files))
    progress_bar.pack(fill=tk.X, padx=10, pady=5)

    for index, file in enumerate(python_files):
        if state.abort_event.is_set():
            break
        file_path = os.path.join(directory, file)
        if file_path in state.analyzed_files:
            continue
        with open(file_path, 'r') as f:
            lines_buffer = []
            for line in f:
                lines_buffer.append(line)
                if len(lines_buffer) >= config.LINES_PER_API_CALL:
                    # Display the lines being sent with 'sending' tag
                    analysis_text.insert(tk.END, f"Sending lines for analysis from {file}:\n", 'title')
                    analysis_text.insert(tk.END, ''.join(lines_buffer) + "\n\n", 'sending')

                    context, highlighted_lines, tokens_used, estimated_cost = establish_context(lines_buffer, file)

                    # Display the analysis with 'analysis' tag
                    analysis_text.insert(tk.END, f"Analysis for {file}:\n", 'title')
                    analysis_text.insert(tk.END, ''.join(context) + "\n\n", 'analysis')

                    total_tokens_used += tokens_used
                    total_estimated_cost += estimated_cost
                    stats_label.config(text=f"Tokens Used: {total_tokens_used}\nEstimated Cost: ${total_estimated_cost:.2f}")

                    lines_buffer = []
            # Process any remaining lines in the buffer
            if lines_buffer:
                # Display the lines being sent with 'sending' tag
                analysis_text.insert(tk.END, f"Sending lines for analysis from {file}:\n", 'title')
                analysis_text.insert(tk.END, ''.join(lines_buffer) + "\n\n", 'sending')

                context, highlighted_lines, tokens_used, estimated_cost = establish_context(lines_buffer, file)

                # Display the analysis with 'analysis' tag
                analysis_text.insert(tk.END, f"Analysis for {file}:\n", 'title')
                analysis_text.insert(tk.END, ''.join(context) + "\n\n", 'analysis')

                total_tokens_used += tokens_used
                total_estimated_cost += estimated_cost
                stats_label.config(text=f"Tokens Used: {total_tokens_used}\nEstimated Cost: ${total_estimated_cost:.2f}")
        state.analyzed_files.add(file_path)

        # Update the progress bar
        progress_var.set(index + 1)
        root.update_idletasks()

    progress_bar.pack_forget()


def establish_context(lines, filename):
    prompt = (f"Thoroughly analyze the Python script named '{filename}' as if you are a seasoned Python and Windows expert. "
              "For each section or line of code, provide detailed feedback segmented into the following categories:\n"
              "- **Performance**: Are there any inefficiencies? How can they be optimized?\n"
              "- **Style**: Does the code follow best practices for readability and Pythonic style? How can it be made clearer?\n"
              "- **Security**: Are there potential vulnerabilities or unsafe practices?\n"
              "- **Functionality**: Are there potential bugs or areas of improvement in the logic?\n"
              "For each suggestion, explain the reasoning behind it. If a section is already optimal, acknowledge it. "
              "For place holders in .py files show best possible viable code based on previous suggestions"
              "Ensure a comprehensive review.\n\n"
              "After the analysis, provide a section titled 'MODIFICATIONS' where you list all the specific changes to be made to the code. "
              "Begin the analysis:\n\n" + "".join(lines))
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant with skills as if you are a seasoned Python and Windows expert."},
            {"role": "user", "content": prompt}
        ]
    )

    tokens_used = response['usage']['total_tokens']
    estimated_cost = (tokens_used / 1000) * TOKEN_COST_PER_THOUSAND

    context = response.choices[0].message['content'].strip()
    highlighted_lines = [context]

    # Log the analysis results based on content type
    if "NOTE:" in context:
        write_log(context, log_type=config.LOG_TYPES["notes"])
        # Save a memory for the type of feedback
        memory.save_memory(f"Feedback type: NOTE for script {filename}.")
    elif "MODIFICATION:" in context:
        write_log(context, log_type=config.LOG_TYPES["modifications"])
        # Save a memory for the type of feedback
        memory.save_memory(f"Feedback type: MODIFICATION for script {filename}.")
    else:
        write_log(context, log_type=config.LOG_TYPES["default"])

    # Save a memory for the script analysis
    memory.save_memory(f"Analyzed script: {filename}. Tokens used: {tokens_used}. Estimated cost: ${estimated_cost:.2f}.")
    # Save a memory for the estimated cost of the analysis
    memory.save_memory(f"Estimated cost for analyzing {filename}: ${estimated_cost:.2f}.")

    return [context], highlighted_lines, tokens_used, estimated_cost




def clone_directory(source_directory):
    if not os.path.exists(source_directory):
        error_message = f"Source directory '{source_directory}' does not exist."
        memory.save_memory(f"Error encountered: {error_message}")
        raise ValueError(error_message)
    
    cloned_directory = source_directory + '_cloned'
    
    if os.path.exists(cloned_directory):
        error_message = f"Destination directory '{cloned_directory}' already exists."
        memory.save_memory(f"Error encountered: {error_message}")
        raise ValueError(error_message)
    
    shutil.copytree(source_directory, cloned_directory)
    
    # Save a memory for the directory cloning
    memory.save_memory(f"Cloned directory from '{source_directory}' to '{cloned_directory}'.")
    
    return cloned_directory


def time_warp_analysis(directory):
    memory.save_memory(f"Started time warp analysis for directory: {directory}.")
    
    cloned_directory = clone_directory(directory)
    load_treeview(cloned_directory)
    python_files = [f for f in os.listdir(cloned_directory) if f.endswith('.py')]
    warp_rules = config.WARP_RULES
    warp_updates_log = []
    code_log = []
    modifications_log = []
    warp_manifest_log = []

    for file in python_files:
        memory.save_memory(f"Analyzing file: {file} using warp rules.")
        
        file_path = os.path.join(cloned_directory, file)
        with open(file_path, 'r') as f:
            lines = f.readlines()
            context = warp_analysis(lines, file, warp_rules)
            warp_updates_log.append((file, context))
            code_log.append(context)
            modifications_log.append(context)
            warp_manifest_log.append(context)

    with open(os.path.join(cloned_directory, "code.txt"), "w") as f:
        f.write("\n".join(code_log))
    with open(os.path.join(cloned_directory, "modifications.txt"), "w") as f:
        f.write("\n".join(modifications_log))
    with open(os.path.join(cloned_directory, "warp_manifest.txt"), "w") as f:
        f.write("\n".join(warp_manifest_log))

    for log in warp_updates_log:
        write_log(log[1])

    memory.save_memory(f"Completed time warp analysis for directory: {directory}.")
    
    return warp_updates_log


def warp_analysis(lines, filename, warp_rules):
    memory.save_memory(f"Started warp analysis for file: {filename} using warp rules: {warp_rules}.")
    
    prompt = (f"Analyze the Python script named '{filename}' based on the warp rules: '{warp_rules}'. "
              "Provide detailed notes about improvements, specifying the line number and the exact change required. "
              "Begin the analysis:\n\n" + "".join(lines))

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant with skills as if you are a seasoned Python and Windows expert."},
            {"role": "user", "content": prompt}
        ]
    )

    context = response.choices[0].message['content'].strip()
    
    memory.save_memory(f"Completed warp analysis for file: {filename}. Results: {context[:100]}...")  # Saving a snippet of the results for brevity.
    
    return context
def apply_warp_updates(directory, warp_updates_log):
    warp_rules = config.WARP_RULES
    updated_code_list = []
    placements = []  # Log to store the details of the changes

    for file, context in warp_updates_log:
        file_path = os.path.join(directory, file)
        memory.save_memory(f"Applying warp updates for file: {file_path}.")
        
        with open(file_path, 'r') as f:
            original_lines = f.readlines()

        # Extract the line number and change details from context
        # This is a placeholder and needs to be implemented based on the specific format of the context
        line_number, change_details = extract_line_and_change(context)

        # Pass the line and change details to ChatGPT with warp rules
        updated_line = get_updated_line(original_lines[line_number], change_details, warp_rules)

        # Save the updated line next to the original line
        updated_code_list.append((original_lines[line_number], updated_line))
        memory.save_memory(f"Original line: {original_lines[line_number]}. Updated line: {updated_line}.")

        # Log the placement details
        placement_detail = {
            "file_path": file_path,
            "line_number": line_number,
            "original_code": original_lines[line_number],
            "updated_code": updated_line
        }
        placements.append(placement_detail)
        memory.save_memory(f"Placement details for file: {file_path}. Line number: {line_number}. Original code: {original_lines[line_number]}. Updated code: {updated_line}.")

    # Write the placements log to a file
    with open("placements_log.txt", "w") as log_file:
        for placement in placements:
            log_file.write(f"File: {placement['file_path']}\n")
            log_file.write(f"Line Number: {placement['line_number']}\n")
            log_file.write(f"Original Code: {placement['original_code']}\n")
            log_file.write(f"Updated Code: {placement['updated_code']}\n")
            log_file.write("-" * 50 + "\n")
    memory.save_memory(f"Placements log written to placements_log.txt.")

    return updated_code_list


def apply_warp_rules(directory, memory_system):
    method = config.WARP_METHOD
    warp_sets = [config.WARP_RULES_SET_1, config.WARP_RULES_SET_2, config.WARP_RULES_SET_3, config.WARP_RULES_SET_4, config.WARP_RULES_SET_5,
                 config.WARP_RULES_SET_6, config.WARP_RULES_SET_7, config.WARP_RULES_SET_8, config.WARP_RULES_SET_9, config.WARP_RULES_SET_10]
    warp_updates_log = []

    # Store the initial information about warp rule application
    memory_system.store_memory(f"Starting warp rule application using method: {method}", "warp_rules")

    if method == 'combine':
        combined_rules = "\n".join(warp_sets)
        config.WARP_RULES = combined_rules

        # Store information about combining warp sets
        memory_system.store_memory(f"Combining all warp sets into one set. Applying combined rules.", "warp_rules")
        
        warp_updates_log.extend(time_warp_analysis(directory))

    elif method == 'sequential':
        # Store information about applying warp sets sequentially
        memory_system.store_memory(f"Applying warp sets sequentially.", "warp_rules")
        
        for warp_set in warp_sets:
            config.WARP_RULES = warp_set

            # Store information about applying a specific warp set
            memory_system.store_memory(f"Applying warp set: {warp_set}.", "warp_rules")
            
            warp_updates_log.extend(time_warp_analysis(directory))

    elif method == 'selective':
        # Store information about applying selected warp sets
        memory_system.store_memory(f"Applying selected warp sets.", "warp_rules")
        
        for warp_set in config.SELECTED_WARP_SETS:
            config.WARP_RULES = warp_set

            # Store information about applying a selected warp set
            memory_system.store_memory(f"Applying selected warp set: {warp_set}.", "warp_rules")
            
            warp_updates_log.extend(time_warp_analysis(directory))

    else:
        # Store information about an invalid method
        memory_system.store_memory(f"Invalid method detected: {method}.", "warp_rules")
        raise ValueError(f"Invalid method: {method}. Choose from 'combine', 'sequential', or 'selective'.")

    return warp_updates_log



def abort_analysis():
    if state.current_thread:
        state.abort_event.set()
        state.current_thread.join()
        state.current_thread = None
        abort_button.config(state=tk.NORMAL)
        messagebox.showinfo("Info", "Analysis aborted.")
        # Save a memory when analysis is aborted
        memory.save_memory("Analysis aborted.")

TOKEN_COST_PER_THOUSAND = 0.0010

root = tk.Tk()
root.title("Pybonce: The Python Pulse")
root.geometry("1000x600")

button_frame = tk.Frame(root, bg="white")
button_frame.pack(fill=tk.X, padx=10, pady=5)

open_button = tk.Button(button_frame, text="Select Directory", padx=10, pady=5, fg="white", bg="#263D42", command=select_directory)
open_button.grid(row=0, column=0, padx=5)

start_button = tk.Button(button_frame, text="Start Analysis", padx=10, pady=5, fg="white", bg="#263D42", command=start_analysis)
start_button.grid(row=0, column=1, padx=5)

abort_button = tk.Button(button_frame, text="Abort Analysis", padx=10, pady=5, fg="white", bg="#263D42", command=abort_analysis)
abort_button.grid(row=0, column=2, padx=5)

tree = ttk.Treeview(root)
tree.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

time_warp_button = tk.Button(button_frame, text="Time Warp Function is a (Wip) and will probably freeze the gui or break programs", padx=10, pady=5, fg="#33FFA1", bg="white", state=tk.DISABLED)
time_warp_button.grid(row=0, column=3, padx=5)

time_warp_button = tk.Button(button_frame, text="Time Warp", padx=10, pady=5, fg="white", bg="#263D42", command=start_time_warp_analysis_in_thread)
time_warp_button.grid(row=1, column=3, padx=5)

stats_label = tk.Label(root, text="Tokens Used: 0\nEstimated Cost: $0.00", bg="white", font=("Arial", 10))
stats_label.pack(pady=10)

analysis_text = Text(root, wrap=tk.WORD)
analysis_text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

create_help_button(button_frame)

setup_text_tags()

root.mainloop()
