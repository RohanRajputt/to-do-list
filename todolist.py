import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
from PIL import Image, ImageTk

class TodoAppGUI:
    def __init__(self, root):
        self.tasks = []
        self.root = root
        self.root.title("To-Do List Application")
        self.root.geometry("700x500")
        self.root.config(bg='#f0f0f0')

        # Load and set background image
        self.bg_image = Image.open("background.png")
        self.bg_image = self.bg_image.resize((700, 500), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = tk.Label(root, image=self.bg_photo)
        self.bg_label.place(relwidth=1, relheight=1)

        # Frame for task entry and buttons
        self.top_frame = tk.Frame(root, bg="#ffffff", bd=2, relief=tk.GROOVE, padx=10, pady=10)
        self.top_frame.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.2)

        # Task entry field
        self.task_entry = tk.Entry(self.top_frame, font=("Helvetica", 14), bd=2, relief=tk.SUNKEN)
        self.task_entry.place(relx=0.02, rely=0.2, relwidth=0.68, relheight=0.5)

        # Load button icons
        self.add_icon = ImageTk.PhotoImage(Image.open("add.png").resize((20, 20), Image.Resampling.LANCZOS))
        self.update_icon = ImageTk.PhotoImage(Image.open("update.png").resize((20, 20), Image.Resampling.LANCZOS))
        self.remove_icon = ImageTk.PhotoImage(Image.open("remove.png").resize((20, 20), Image.Resampling.LANCZOS))
        self.complete_icon = ImageTk.PhotoImage(Image.open("complete.png").resize((20, 20), Image.Resampling.LANCZOS))
        self.display_icon = ImageTk.PhotoImage(Image.open("display.png").resize((20, 20), Image.Resampling.LANCZOS))

        # Buttons for actions
        self.add_button = tk.Button(self.top_frame, text="Add", image=self.add_icon, compound=tk.LEFT, font=("Helvetica", 12), command=self.add_task, bg="#4CAF50", fg="white")
        self.add_button.place(relx=0.72, rely=0.2, relwidth=0.25, relheight=0.5)

        self.update_button = tk.Button(self.top_frame, text="Update", image=self.update_icon, compound=tk.LEFT, font=("Helvetica", 12), command=self.update_task, bg="#2196F3", fg="white")
        self.update_button.place(relx=0.02, rely=0.75, relwidth=0.25, relheight=0.5)

        self.remove_button = tk.Button(self.top_frame, text="Remove", image=self.remove_icon, compound=tk.LEFT, font=("Helvetica", 12), command=self.remove_task, bg="#F44336", fg="white")
        self.remove_button.place(relx=0.28, rely=0.75, relwidth=0.25, relheight=0.5)

        self.complete_button = tk.Button(self.top_frame, text="Complete", image=self.complete_icon, compound=tk.LEFT, font=("Helvetica", 12), command=self.complete_task, bg="#FF9800", fg="white")
        self.complete_button.place(relx=0.54, rely=0.75, relwidth=0.25, relheight=0.5)

        self.display_button = tk.Button(self.top_frame, text="Display", image=self.display_icon, compound=tk.LEFT, font=("Helvetica", 12), command=self.display_tasks, bg="#9C27B0", fg="white")
        self.display_button.place(relx=0.8, rely=0.75, relwidth=0.25, relheight=0.5)

        # Task List Frame
        self.task_frame = tk.Frame(root, bg="#ffffff", bd=2, relief=tk.GROOVE)
        self.task_frame.place(relx=0.05, rely=0.3, relwidth=0.9, relheight=0.65)

        # Treeview for displaying tasks
        self.task_tree = ttk.Treeview(self.task_frame, columns=("Task", "Status"), show='headings')
        self.task_tree.heading("Task", text="Task")
        self.task_tree.heading("Status", text="Status")
        self.task_tree.column("Task", width=500, anchor="w")
        self.task_tree.column("Status", width=150, anchor="center")
        self.task_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar for Treeview
        self.scrollbar = ttk.Scrollbar(self.task_frame, orient="vertical", command=self.task_tree.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.task_tree.config(yscrollcommand=self.scrollbar.set)

    def add_task(self):
        task = self.task_entry.get().strip()
        if task:
            self.tasks.append({"task": task, "status": "Incomplete"})
            self.task_tree.insert("", tk.END, values=(task, "Incomplete"))
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Task cannot be empty!")

    def update_task(self):
        selected_item = self.task_tree.selection()
        if selected_item:
            current_task = self.task_tree.item(selected_item)["values"][0]
            new_task = simpledialog.askstring("Update Task", "Enter new task:", initialvalue=current_task)
            if new_task:
                self.task_tree.item(selected_item, values=(new_task, "Incomplete"))
                index = self.tasks.index(next(filter(lambda x: x["task"] == current_task, self.tasks)))
                self.tasks[index]["task"] = new_task
            else:
                messagebox.showwarning("Input Error", "Task cannot be empty!")
        else:
            messagebox.showwarning("Selection Error", "Please select a task to update!")

    def remove_task(self):
        selected_item = self.task_tree.selection()
        if selected_item:
            task_to_remove = self.task_tree.item(selected_item)["values"][0]
            self.tasks = [task for task in self.tasks if task["task"] != task_to_remove]
            self.task_tree.delete(selected_item)
        else:
            messagebox.showwarning("Selection Error", "Please select a task to remove!")

    def complete_task(self):
        selected_item = self.task_tree.selection()
        if selected_item:
            task_to_complete = self.task_tree.item(selected_item)["values"][0]
            index = self.tasks.index(next(filter(lambda x: x["task"] == task_to_complete, self.tasks)))
            self.tasks[index]["status"] = "Completed"
            self.task_tree.item(selected_item, values=(task_to_complete, "Completed"))
        else:
            messagebox.showwarning("Selection Error", "Please select a task to mark as complete!")

    def display_tasks(self):
        messagebox.showinfo("Tasks", "\n".join([f"{task['task']} - {task['status']}" for task in self.tasks]) if self.tasks else "No tasks available.")

if __name__ == "__main__":
    root = tk.Tk()
    gui_app = TodoAppGUI(root)
    root.mainloop()
