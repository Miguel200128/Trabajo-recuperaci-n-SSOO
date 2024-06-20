import tkinter as tk
from tkinter import ttk, messagebox
import os
import random
import datetime


class CustomTerminal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Custom Terminal")
        self.geometry("600x450")

        self.create_menu()
        self.create_buttons()
        self.create_terminal()

        self.current_directory = os.getcwd()
        self.update_prompt()

    def create_menu(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="About", command=self.show_about)
        file_menu.add_command(label="Version", command=self.show_version)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)

    def create_buttons(self):
        button_frame = tk.Frame(self)
        button_frame.pack(fill=tk.X, padx=5, pady=5)

        about_button = ttk.Button(button_frame, text="About", command=self.show_about)
        about_button.pack(side=tk.LEFT, padx=5)

        version_button = ttk.Button(button_frame, text="Version", command=self.show_version)
        version_button.pack(side=tk.LEFT, padx=5)

    def create_terminal(self):
        self.terminal = tk.Text(self, bg="black", fg="lime", insertbackground="white")
        self.terminal.pack(expand=True, fill="both")
        self.terminal.bind("<Return>", self.process_command)

    def update_prompt(self):
        self.prompt = f"\n[{self.current_directory}]$ "
        self.terminal.insert(tk.END, self.prompt)
        self.terminal.see(tk.END)

    def process_command(self, event):
        command = self.terminal.get("insert linestart", "insert lineend").strip()
        command = command.replace(self.prompt.strip(), "").strip()

        if command:
            self.terminal.insert(tk.END, "\n")
            self.execute_command(command)

        self.update_prompt()
        return "break"

    def execute_command(self, command):
        parts = command.split()
        cmd = parts[0]
        args = parts[1:]

        commands = {
            "cd": self.change_directory,
            "mkdir": self.make_directory,
            "touch": self.create_file,
            "rm": self.remove_file,
            "rmdir": self.remove_directory,
            "pwd": self.print_working_directory,
            "ls": self.list_directory,
            "cat": self.cat_file,
            "echo": self.echo,
            "clear": self.clear_terminal,
            "fortune": self.fortune,
            "ascii_art": self.ascii_art,
            "date": self.show_date
        }

        if cmd in commands:
            commands[cmd](args)
        else:
            self.terminal.insert(tk.END, f"Command not found: {cmd}\n")

    def change_directory(self, args):
        if not args:
            self.terminal.insert(tk.END, "cd: missing argument\n")
            return
        try:
            os.chdir(args[0])
            self.current_directory = os.getcwd()
        except FileNotFoundError:
            self.terminal.insert(tk.END, f"cd: {args[0]}: No such file or directory\n")

    def make_directory(self, args):
        if not args:
            self.terminal.insert(tk.END, "mkdir: missing operand\n")
            return
        try:
            os.mkdir(args[0])
            self.terminal.insert(tk.END, f"Directory created: {args[0]}\n")
        except FileExistsError:
            self.terminal.insert(tk.END, f"mkdir: cannot create directory '{args[0]}': File exists\n")

    def create_file(self, args):
        if not args:
            self.terminal.insert(tk.END, "touch: missing file operand\n")
            return
        open(args[0], 'a').close()
        self.terminal.insert(tk.END, f"File created: {args[0]}\n")

    def remove_file(self, args):
        if not args:
            self.terminal.insert(tk.END, "rm: missing operand\n")
            return
        try:
            os.remove(args[0])
            self.terminal.insert(tk.END, f"File removed: {args[0]}\n")
        except FileNotFoundError:
            self.terminal.insert(tk.END, f"rm: cannot remove '{args[0]}': No such file or directory\n")

    def remove_directory(self, args):
        if not args:
            self.terminal.insert(tk.END, "rmdir: missing operand\n")
            return
        try:
            os.rmdir(args[0])
            self.terminal.insert(tk.END, f"Directory removed: {args[0]}\n")
        except FileNotFoundError:
            self.terminal.insert(tk.END, f"rmdir: failed to remove '{args[0]}': No such file or directory\n")
        except OSError:
            self.terminal.insert(tk.END, f"rmdir: failed to remove '{args[0]}': Directory not empty\n")

    def print_working_directory(self, args):
        self.terminal.insert(tk.END, f"{self.current_directory}\n")

    def list_directory(self, args):
        try:
            files = os.listdir('.' if not args else args[0])
            for file in files:
                self.terminal.insert(tk.END, f"{file}\n")
        except FileNotFoundError:
            self.terminal.insert(tk.END, f"ls: cannot access '{args[0]}': No such file or directory\n")

    def cat_file(self, args):
        if not args:
            self.terminal.insert(tk.END, "cat: missing file operand\n")
            return
        try:
            with open(args[0], 'r') as file:
                content = file.read()
                self.terminal.insert(tk.END, f"{content}\n")
        except FileNotFoundError:
            self.terminal.insert(tk.END, f"cat: {args[0]}: No such file or directory\n")

    def echo(self, args):
        self.terminal.insert(tk.END, f"{' '.join(args)}\n")

    def clear_terminal(self, args):
        self.terminal.delete(1.0, tk.END)

    def fortune(self, args):
        fortunes = [
            "You will have a great day!",
            "A surprise awaits you.",
            "Your hard work will pay off soon.",
            "A journey of a thousand miles begins with a single step.",
            "Your creativity will shine today."
        ]
        self.terminal.insert(tk.END, f"{random.choice(fortunes)}\n")

    def ascii_art(self, args):
        art = """
         /\\_/\\
        ( o.o )
         > ^ <
        """
        self.terminal.insert(tk.END, art + "\n")

    def show_date(self, args):
        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.terminal.insert(tk.END, f"Current date and time: {current_date}\n")

    def show_about(self):
        about_window = tk.Toplevel(self)
        about_window.title("About")
        about_window.geometry("300x200")

        label = tk.Label(about_window, text="Custom Terminal\n\nCreated by: Your Miguel Angel\nEmail: "
                                            "your.email@example.com")
        label.pack(expand=True)

    def show_version(self):
        version_window = tk.Toplevel(self)
        version_window.title("Version")
        version_window.geometry("300x200")

        label = tk.Label(version_window, text="Custom Terminal v1.0\nRelease Date: 2009-01-01")
        label.pack(expand=True)


if __name__ == "__main__":
    app = CustomTerminal()
    app.mainloop()