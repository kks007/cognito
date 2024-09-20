import tkinter as tk
from tkinter import filedialog, ttk
import os
import datetime
from document_summarization.summarizer import summarize_text, train_lda
from document_summarization.ocr import perform_ocr
from mail_summary.fetch_mails_formatted import getEmails

def browse_file(entry):
    filename = filedialog.askopenfilename()
    entry.delete(0, tk.END)
    entry.insert(0, filename)

def browse_directory(entry):
    directory = filedialog.askdirectory()
    entry.delete(0, tk.END)
    entry.insert(0, directory)

def main(text_summary, file_summary, ocr_file, num_sentences, summary_length, lda_train, mail_summary, time_interval=None):
    text = ""
    lda_model = None
    output = ""

    # Handle mail summary case
    if mail_summary:
         time_interval = int(time_interval)
         emails = getEmails(time_interval)
         for email in emails:

            no_words = (email['Message']).count(" ")
            if no_words > 80:
                no_words = no_words/3
            else:
                no_words = None
            email_summary = summarize_text(email['Message'], None, no_words)  # Summarize the email content 
            output += f"Subject: {email['Subject']}\n\nFrom: {email['From']}\n\nTime: {email['Time']} \n\nSummary: {email_summary}\n _____________________________________________________________________________ \n"

         return output

    # Handle LDA training
    if lda_train:
        documents = []
        for filename in os.listdir(lda_train):
            if filename.endswith(".txt"):
                with open(os.path.join(lda_train, filename), 'r') as f:
                    documents.append(f.read())
        lda_model = train_lda(documents)
        output = "LDA model trained successfully."
        return output

    # Validate input
    if not text_summary and not file_summary and not ocr_file:
        return "Please provide either --text-summary, --file-summary, or --ocr-file option."

    if (text_summary and file_summary) or (text_summary and ocr_file) or (file_summary and ocr_file):
        return "Please provide only one of --text-summary, --file-summary, or --ocr-file option."

    # Load input text
    if text_summary:
        text = text_summary
    elif file_summary:
        with open(file_summary, 'r') as f:
            text = f.read()
    elif ocr_file:
        result_text = perform_ocr(ocr_file)
        if result_text:
            return f"OCR Result:\n{result_text}\n"
        else:
            return "OCR failed. Please check the image file path and try again."

    # Summarize the text based on user input
    num_sentences = int(num_sentences) if num_sentences else None
    if num_sentences:
        summary = summarize_text(text, num_sentences=num_sentences, lda_model=lda_model)
        output = f"Summary ({num_sentences} sentences):\n{summary}"
    else:
        summary = summarize_text(text, summary_length=summary_length, lda_model=lda_model)
        output = f"Summary ({summary_length} words):\n{summary}"

    return output

def run_main():
    args = {
        'text_summary': text_summary_entry.get(),
        'file_summary': file_summary_entry.get(),
        'ocr_file': ocr_file_entry.get(),
        'num_sentences': num_sentences_entry.get() if num_sentences_entry.get() else None,
        'summary_length': int(summary_length_entry.get()) if summary_length_entry.get() else 50,  # Default to 50 words
        'lda_train': lda_train_entry.get(),
        'mail_summary': mail_summary_var.get(),
        'time_interval' : time_interval_slider.get()
    }

    # Call the main function with the arguments
    output = main(**args)
    
    # Display output in the text box
    output_text.delete('1.0', tk.END)
    output_text.insert(tk.END, output)

root = tk.Tk()

# Create a Notebook for the UI
notebook = ttk.Notebook(root)

# Create frames for each tab
summary_frame = ttk.Frame(notebook)
ocr_frame = ttk.Frame(notebook)
mail_frame = ttk.Frame(notebook)
lda_frame = ttk.Frame(notebook)

# Add frames to the Notebook (tabs)
notebook.add(summary_frame, text='Summary')
notebook.add(ocr_frame, text='OCR')
notebook.add(mail_frame, text='Mail')
notebook.add(lda_frame, text='LDA Training')

notebook.pack(fill='both', expand=True)

# Summary Tab UI
text_summary_label = ttk.Label(summary_frame, text="Text to summarize")
text_summary_label.pack(padx=10, pady=10)
text_summary_entry = ttk.Entry(summary_frame)
text_summary_entry.pack(padx=10, pady=10)

file_summary_label = ttk.Label(summary_frame, text="File to summarize")
file_summary_label.pack(padx=10, pady=10)
file_summary_entry = ttk.Entry(summary_frame)
file_summary_entry.pack(padx=10, pady=10)
file_summary_button = ttk.Button(summary_frame, text="Browse", command=lambda: browse_file(file_summary_entry))
file_summary_button.pack(padx=10, pady=10)

num_sentences_label = ttk.Label(summary_frame, text="Number of sentences")
num_sentences_label.pack(padx=10, pady=10)
num_sentences_entry = ttk.Entry(summary_frame)
num_sentences_entry.pack(padx=10, pady=10)

summary_length_label = ttk.Label(summary_frame, text="Length in words")
summary_length_label.pack(padx=10, pady=10)
summary_length_entry = ttk.Entry(summary_frame)
summary_length_entry.pack(padx=10, pady=10)

# OCR Tab UI
ocr_file_label = ttk.Label(ocr_frame, text="File for OCR")
ocr_file_label.pack(padx=10, pady=10)
ocr_file_entry = ttk.Entry(ocr_frame)
ocr_file_entry.pack(padx=10, pady=10)
ocr_file_button = ttk.Button(ocr_frame, text="Browse", command=lambda: browse_file(ocr_file_entry))
ocr_file_button.pack(padx=10, pady=10)

# Mail Tab UI
mail_summary_label = ttk.Label(mail_frame, text="Fetch and summarize emails")
mail_summary_label.pack(padx=10, pady=10)
mail_summary_var = tk.IntVar()
mail_summary_checkbutton = ttk.Checkbutton(mail_frame, variable=mail_summary_var)
mail_summary_checkbutton.pack(padx=10, pady=10)

# Add a slider for the time interval
time_interval_label = ttk.Label(mail_frame, text="Time interval (hours)")
time_interval_label.pack(padx=10, pady=0)
time_interval_slider = ttk.Scale(mail_frame, from_=1, to=24, length=500, orient='horizontal')
time_interval_slider.pack(padx=10, pady=10)
# Create a canvas for the labels
canvas = tk.Canvas(mail_frame, width=500, height=30)
canvas.pack(padx=10, pady=0)
# Draw the labels on the canvas
for i in [1, 5, 10, 15, 20, 24]:
    x = 20.5 * i  # Adjust this value to position the labels correctly
    canvas.create_text(x, 15, text=str(i))


# LDA Training Tab UI
lda_train_label = ttk.Label(lda_frame, text="Directory for LDA training files")
lda_train_label.pack(padx=10, pady=10)
lda_train_entry = ttk.Entry(lda_frame)
lda_train_entry.pack(padx=10, pady=10)
lda_train_button = ttk.Button(lda_frame, text="Browse", command=lambda: browse_directory(lda_train_entry))
lda_train_button.pack(padx=10, pady=10)

# Clear inputs when changing tabs
def clear_inputs(event):
    text_summary_entry.delete(0, tk.END)
    file_summary_entry.delete(0, tk.END)
    num_sentences_entry.delete(0, tk.END)
    summary_length_entry.delete(0, tk.END)
    ocr_file_entry.delete(0, tk.END)
    mail_summary_var.set(0)
    time_interval_slider.set(1)
    lda_train_entry.delete(0, tk.END)

notebook.bind('<<NotebookTabChanged>>', clear_inputs)

# Run Button
run_button = ttk.Button(root, text="Run", command=run_main)
run_button.pack(padx=10, pady=10)

# Output Text Box
output_text = tk.Text(root)
output_text.pack(padx=10, pady=10)

root.mainloop()
