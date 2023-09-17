import os 
import tkinter as tk 
 from tkinter import filedialog, Text, messagebox, simpledialog, ttk 
import openai 
import threading 
import config 
 from tkinter.ttk import Progressbar 
  
 openai.api_key = config.API_KEY 
  
 class AnalysisState: 
     def __init__(self): 
         self.current_thread = None 
         self.abort_event = threading.Event() 
         self.analyzed_files = set() 
  
 state = AnalysisState() 
  
 def setup_text_tags(): 
     analysis_text.tag_configure('sending', background=config.SENDING_COLOR, font=("Arial", 10)) 
     analysis_text.tag_configure('analysis', background=config.ANALYSIS_COLOR, font=("Arial", 10)) 
     analysis_text.tag_configure('title', background=config.TITLE_COLOR, font=("Arial", 10, 'bold')) 
     analysis_text.tag_configure('highlight', background=config.HIGHLIGHT_COLOR, font=("Arial", 10)) 
  
 def select_directory(): 
     folder_selected = filedialog.askdirectory() 
     if not folder_selected: 
         messagebox.showerror("Error", "No directory selected.") 
         return 
     load_treeview(folder_selected) 
  
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


    
 def start_analysis(): 
     directory = filedialog.askdirectory() 
     if not directory: 
         return 
     state.abort_event.clear() 
     state.current_thread = threading.Thread(target=process_directory, args=(directory,)) 
     state.current_thread.start() 
     abort_button.config(state=tk.DISABLED) 
  
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
    elif "MODIFICATION:" in context:
        write_log(context, log_type=config.LOG_TYPES["modifications"])
    else:
        write_log(context, log_type=config.LOG_TYPES["default"])

    return [context], highlighted_lines, tokens_used, estimated_cost


 def time_warp_analysis(directory):
    python_files = [f for f in os.listdir(directory) if f.endswith('.py')]
    warp_rules = config.WARP_RULES
    warp_updates_log = []

    for file in python_files:
        file_path = os.path.join(directory, file)
        with open(file_path, 'r') as f:
            lines = f.readlines()
            context = warp_analysis(lines, file, warp_rules)
            warp_updates_log.append((file, context))

    return warp_updates_log

def warp_analysis(lines, filename, warp_rules):
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
    return context

def apply_warp_updates(directory, warp_updates_log):
    warp_rules = config.WARP_RULES
    updated_code_list = []
    placements = []  # Log to store the details of the changes

    for file, context in warp_updates_log:
        file_path = os.path.join(directory, file)
        with open(file_path, 'r') as f:
            original_lines = f.readlines()

        # Extract the line number and change details from context
        # This is a placeholder and needs to be implemented based on the specific format of the context
        line_number, change_details = extract_line_and_change(context)

        # Pass the line and change details to ChatGPT with warp rules
        updated_line = get_updated_line(original_lines[line_number], change_details, warp_rules)
        
        # Save the updated line next to the original line
        updated_code_list.append((original_lines[line_number], updated_line))

        # Log the placement details
        placement_detail = {
            "file_path": file_path,
            "line_number": line_number,
            "original_code": original_lines[line_number],
            "updated_code": updated_line
        }
        placements.append(placement_detail)

    # Write the placements log to a file
    with open("placements_log.txt", "w") as log_file:
        for placement in placements:
            log_file.write(f"File: {placement['file_path']}\n")
            log_file.write(f"Line Number: {placement['line_number']}\n")
            log_file.write(f"Original Code: {placement['original_code']}\n")
            log_file.write(f"Updated Code: {placement['updated_code']}\n")
            log_file.write("-" * 50 + "\n")

    return updated_code_list


  
 def abort_analysis(): 
     if state.current_thread: 
         state.abort_event.set() 
         state.current_thread.join() 
         state.current_thread = None 
         abort_button.config(state=tk.NORMAL) 
         messagebox.showinfo("Info", "Analysis aborted.") 
  
 TOKEN_COST_PER_THOUSAND = 0.0015 #specified here https://openai.com/pricing 
  
  
  
 root = tk.Tk() 
 root.title("Pybonce"":" "The Python Pulse") 
 root.geometry("800x600") 
  
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

 time_warp_button = tk.Button(button_frame, text="Time Warp", padx=10, pady=5, fg="white", bg="#263D42", command=time_warp_analysis)
 time_warp_button.grid(row=0, column=3, padx=5)

  
 stats_label = tk.Label(root, text="Tokens Used: 0\nEstimated Cost: $0.00", bg="white", font=("Arial", 10)) 
 stats_label.pack(pady=10) 
  
 analysis_text = Text(root, wrap=tk.WORD) 
 analysis_text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10) 
  
 setup_text_tags() 
  
 root.mainloop()
