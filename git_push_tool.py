#!/usr/bin/env python3
"""
Git Push Tool - A simple GUI for committing and pushing Git changes
Works on Windows, Mac, and Linux
"""

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import subprocess
import os
import threading
from pathlib import Path


class GitPushTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Git Push Tool")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Selected folder path
        self.selected_folder = tk.StringVar()
        self.selected_folder.set("No folder selected")
        
        # Configure grid weights for responsive layout
        self.root.grid_rowconfigure(4, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        self.create_widgets()
        
    def create_widgets(self):
        # Header
        header = tk.Label(
            self.root,
            text="Git Push Tool",
            font=("Arial", 18, "bold"),
            pady=10
        )
        header.grid(row=0, column=0, columnspan=2, sticky="ew")
        
        # Folder selection section
        folder_frame = tk.Frame(self.root, pady=10, padx=20)
        folder_frame.grid(row=1, column=0, columnspan=2, sticky="ew")
        folder_frame.grid_columnconfigure(0, weight=1)
        
        tk.Label(
            folder_frame,
            text="Selected Repository:",
            font=("Arial", 10, "bold")
        ).grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        folder_label = tk.Label(
            folder_frame,
            textvariable=self.selected_folder,
            font=("Arial", 9),
            fg="blue",
            anchor="w",
            wraplength=500
        )
        folder_label.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        
        select_button = tk.Button(
            folder_frame,
            text="📁 Select Folder",
            command=self.select_folder,
            font=("Arial", 11),
            bg="#4CAF50",
            fg="white",
            padx=20,
            pady=8,
            cursor="hand2"
        )
        select_button.grid(row=2, column=0, pady=5)
        
        # Commit message section
        message_frame = tk.Frame(self.root, pady=10, padx=20)
        message_frame.grid(row=2, column=0, columnspan=2, sticky="ew")
        message_frame.grid_columnconfigure(0, weight=1)
        
        tk.Label(
            message_frame,
            text="Commit Message:",
            font=("Arial", 10, "bold")
        ).grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        self.commit_message = tk.Entry(
            message_frame,
            font=("Arial", 11),
            width=50
        )
        self.commit_message.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        self.commit_message.insert(0, "Updated project")
        
        # Push button
        self.push_button = tk.Button(
            message_frame,
            text="🚀 Push to GitHub",
            command=self.push_changes,
            font=("Arial", 12, "bold"),
            bg="#2196F3",
            fg="white",
            padx=30,
            pady=10,
            cursor="hand2"
        )
        self.push_button.grid(row=2, column=0, pady=10)
        
        # Output console section
        console_frame = tk.Frame(self.root, pady=10, padx=20)
        console_frame.grid(row=4, column=0, columnspan=2, sticky="nsew")
        console_frame.grid_rowconfigure(1, weight=1)
        console_frame.grid_columnconfigure(0, weight=1)
        
        tk.Label(
            console_frame,
            text="Output:",
            font=("Arial", 10, "bold")
        ).grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        self.output_text = scrolledtext.ScrolledText(
            console_frame,
            font=("Courier", 9),
            height=12,
            bg="#f5f5f5",
            wrap=tk.WORD
        )
        self.output_text.grid(row=1, column=0, sticky="nsew")
        
        # Clear button for output
        clear_button = tk.Button(
            console_frame,
            text="Clear Output",
            command=self.clear_output,
            font=("Arial", 9),
            cursor="hand2"
        )
        clear_button.grid(row=2, column=0, pady=5, sticky="e")
        
    def select_folder(self):
        folder = filedialog.askdirectory(title="Select Git Repository Folder")
        if folder:
            self.selected_folder.set(folder)
            self.log_output(f"Selected folder: {folder}\n", "blue")
            
            # Check if it's a git repository
            if not os.path.exists(os.path.join(folder, ".git")):
                messagebox.showwarning(
                    "Warning",
                    "The selected folder does not appear to be a Git repository.\n\n"
                    "Make sure you've initialized git with 'git init' and added a remote."
                )
    
    def log_output(self, message, color="black"):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, message)
        if color != "black":
            start_index = self.output_text.index(f"end-{len(message)}c")
            self.output_text.tag_add(color, start_index, tk.END)
            self.output_text.tag_config(color, foreground=color)
        self.output_text.see(tk.END)
        self.output_text.config(state=tk.DISABLED)
        self.root.update()
    
    def clear_output(self):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state=tk.DISABLED)
    
    def run_git_command(self, command, cwd):
        """Run a git command and return the result"""
        try:
            result = subprocess.run(
                command,
                cwd=cwd,
                capture_output=True,
                text=True,
                shell=True
            )
            return result.returncode, result.stdout, result.stderr
        except Exception as e:
            return -1, "", str(e)
    
    def push_changes(self):
        folder = self.selected_folder.get()
        
        if folder == "No folder selected":
            messagebox.showerror("Error", "Please select a folder first!")
            return
        
        commit_msg = self.commit_message.get().strip()
        if not commit_msg:
            messagebox.showerror("Error", "Please enter a commit message!")
            return
        
        # Disable button during operation
        self.push_button.config(state=tk.DISABLED, text="Processing...")
        
        # Run git commands in a separate thread to keep UI responsive
        thread = threading.Thread(
            target=self.execute_git_push,
            args=(folder, commit_msg),
            daemon=True
        )
        thread.start()
    
    def execute_git_push(self, folder, commit_msg):
        try:
            self.log_output("\n" + "="*60 + "\n", "black")
            self.log_output("Starting Git operations...\n\n", "blue")
            
            # Step 1: git add .
            self.log_output("Running: git add .\n", "black")
            code, stdout, stderr = self.run_git_command("git add .", folder)
            
            if code != 0:
                self.log_output(f"Error in git add:\n{stderr}\n", "red")
                self.enable_push_button()
                return
            
            self.log_output("✓ Successfully staged all changes\n\n", "green")
            
            # Step 2: git commit
            commit_command = f'git commit -m "{commit_msg}"'
            self.log_output(f"Running: git commit -m \"{commit_msg}\"\n", "black")
            code, stdout, stderr = self.run_git_command(commit_command, folder)
            
            if code != 0:
                # Check if it's just "nothing to commit"
                if "nothing to commit" in stdout or "nothing to commit" in stderr:
                    self.log_output("ℹ No changes to commit\n\n", "orange")
                else:
                    self.log_output(f"Error in git commit:\n{stderr}\n{stdout}\n", "red")
                    self.enable_push_button()
                    return
            else:
                self.log_output(f"✓ Successfully committed changes\n{stdout}\n", "green")
            
            # Step 3: git push
            self.log_output("Running: git push origin main\n", "black")
            code, stdout, stderr = self.run_git_command("git push origin main", folder)
            
            if code != 0:
                self.log_output(f"Error in git push:\n{stderr}\n", "red")
                self.log_output("\nTip: Make sure you have:\n", "orange")
                self.log_output("  • Set up a remote named 'origin'\n", "orange")
                self.log_output("  • A branch named 'main' (or change to 'master' if needed)\n", "orange")
                self.log_output("  • Proper authentication configured\n", "orange")
                self.enable_push_button()
                return
            
            self.log_output(f"✓ Successfully pushed to origin/main\n{stderr}\n", "green")
            self.log_output("\n" + "="*60 + "\n", "black")
            self.log_output("🎉 All operations completed successfully!\n", "green")
            
            messagebox.showinfo("Success", "Changes pushed to GitHub successfully!")
            
        except Exception as e:
            self.log_output(f"\nUnexpected error: {str(e)}\n", "red")
            messagebox.showerror("Error", f"An unexpected error occurred:\n{str(e)}")
        
        finally:
            self.enable_push_button()
    
    def enable_push_button(self):
        self.push_button.config(state=tk.NORMAL, text="🚀 Push to GitHub")


def main():
    root = tk.Tk()
    app = GitPushTool(root)
    root.mainloop()


if __name__ == "__main__":
    main()