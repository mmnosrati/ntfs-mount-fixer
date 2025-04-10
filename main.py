import subprocess
import tkinter as tk
from tkinter import messagebox, scrolledtext, simpledialog

def get_partitions():
    try:
        result = subprocess.run(
            ['lsblk', '-o', 'NAME,FSTYPE,SIZE', '-nr'],
            capture_output=True, text=True
        )
        lines = result.stdout.strip().split('\n')
        partition_list = []
        for line in lines:
            parts = line.split()
            if len(parts) == 3:
                name, fstype, size = parts
                full_path = f"/dev/{name}"
                formatted = f"{full_path:<15} {fstype:<8} {size:>6}"
                partition_list.append(formatted)
        return partition_list
    except Exception as e:
        messagebox.showerror("Error", f"Failed to get partitions:\n{e}")
        return []

def on_partition_select(event):
    selection = partition_listbox.curselection()
    if selection:
        selected = partition_listbox.get(selection[0])
        partition_path = selected.split()[0]  # First column
        entry_partition.delete(0, tk.END)
        entry_partition.insert(0, partition_path)
        entry_partition.config(fg='black')

def run_ntfsfix():
    partition = entry_partition.get().strip()
    if partition == placeholder_text or not partition:
        messagebox.showwarning("Warning", "Please select or enter a valid partition path.")
        return

    confirm = messagebox.askyesno("Confirm", f"Are you sure you want to run ntfsfix on {partition}?")
    if not confirm:
        return

    # Ask for root password
    password = simpledialog.askstring("Root Password", "Enter your root password:", show='*')
    if not password:
        return

    try:
        result = subprocess.run(
            ['sudo', '-S', 'ntfsfix', '--clear-dirty', partition],
            input=password + '\n',
            capture_output=True, text=True
        )

        output_text.delete('1.0', tk.END)

        success_msg = f"NTFS partition {partition} was processed successfully."
        combined_output = result.stdout + result.stderr

        if success_msg in combined_output:
            output_text.insert(tk.END, success_msg)
        else:
            output_text.insert(tk.END, combined_output)

        if result.returncode != 0:
            messagebox.showerror("ntfsfix failed", "ntfsfix could not run successfully.\nCheck the output below.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to run ntfsfix:\n{e}")



def on_entry_focus_in(event):
    if entry_partition.get() == placeholder_text:
        entry_partition.delete(0, tk.END)
        entry_partition.config(fg='black')

def on_entry_focus_out(event):
    if entry_partition.get().strip() == "":
        entry_partition.insert(0, placeholder_text)
        entry_partition.config(fg='gray')

# GUI setup
root = tk.Tk()
root.title("NTFS Mount Fixer")
root.geometry("600x550")

placeholder_text = "Enter partition name, example /dev/sdb1"

top_frame = tk.Frame(root)
top_frame.pack(pady=10)

label = tk.Label(top_frame, text="Select a partition:")
label.pack(anchor="w", padx=5)

# Listbox
partition_listbox = tk.Listbox(top_frame, width=60, height=10, font=('Courier', 10))
partition_listbox.pack(padx=10)
partition_listbox.bind('<<ListboxSelect>>', on_partition_select)

# Fill the list
partitions = get_partitions()
for p in partitions:
    partition_listbox.insert(tk.END, p)

# Entry and button
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

entry_partition = tk.Entry(input_frame, width=35, fg='gray')
entry_partition.grid(row=0, column=0, padx=10)
entry_partition.insert(0, placeholder_text)
entry_partition.bind("<FocusIn>", on_entry_focus_in)
entry_partition.bind("<FocusOut>", on_entry_focus_out)

btn_fix = tk.Button(input_frame, text="Run ntfsfix", command=run_ntfsfix, fg="white", bg="darkred")
btn_fix.grid(row=0, column=1, padx=10)

# Output area
output_text = scrolledtext.ScrolledText(root, width=75, height=20)
output_text.pack(padx=10, pady=10)

root.mainloop()
