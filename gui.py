import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from utils import load_text, calculate_match
import os

def choose_job_description():
    path = filedialog.askopenfilename(title="Select Job Description", filetypes=[("Text/PDF/Word files", "*.txt *.pdf *.docx")])
    if path:
        jd_path_var.set(path)

def choose_cv_files():
    files = filedialog.askopenfilenames(title="Select CV Files", filetypes=[("Text/PDF/Word files", "*.txt *.pdf *.docx")])
    if files:
        cv_paths_var.set(files)
        cv_listbox.delete(0, tk.END)
        for path in files:
            cv_listbox.insert(tk.END, path)


def run_matching():
    jd_path = jd_path_var.get()
    cv_paths = cv_paths_var.get()

    if not jd_path or not cv_paths:
        messagebox.showwarning("Missing Files", "Please select both a job description and CV files.")
        return

    try:
        jd_text = load_text(jd_path)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load job description:\n{e}")
        return

    results_box.delete("1.0", tk.END)

    for cv_file in cv_paths:
        try:
            cv_text = load_text(cv_file)
            score = calculate_match(cv_text, jd_text)
            results_box.insert(tk.END, f"{os.path.basename(cv_file)} → Match Score: {score:.2f}%\n")
        except Exception as e:
            results_box.insert(tk.END, f"{os.path.basename(cv_file)} → Error: {str(e)}\n")

# GUI setup
root = tk.Tk()
root.title("CV Matcher")
root.geometry("600x500")

jd_path_var = tk.StringVar()
cv_paths_var = tk.Variable()

tk.Label(root, text="Job Description:").pack(pady=(10, 0))
tk.Entry(root, textvariable=jd_path_var, width=60).pack()
tk.Button(root, text="Browse Job Description", command=choose_job_description).pack()


tk.Label(root, text="CV Files:").pack(pady=(10, 0))
tk.Button(root, text="Select CV Files", command=choose_cv_files).pack()

cv_listbox = tk.Listbox(root, width=80, height=5)
cv_listbox.pack(pady=(5, 10))

tk.Button(root, text="Compare", command=run_matching, bg="green", fg="white").pack(pady=10)

results_box = scrolledtext.ScrolledText(root, width=70, height=20)
results_box.pack(pady=10)

root.mainloop()
