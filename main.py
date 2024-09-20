import os
import click
import datetime
from document_summarization.summarizer import summarize_text, train_lda
from document_summarization.ocr import perform_ocr
from mail_summary.fetch_mails_formatted import getEmails

@click.command()
@click.option('--text-summary', help='Text to summarize')
@click.option('--file-summary', type=click.Path(exists=True), help='File to summarize')
@click.option('--ocr-file', type=click.Path(exists=True), help='File to perform OCR')
@click.option('--num-sentences', default=None, help='Number of sentences in the summary')
@click.option('--summary-length', default=50, help='Desired length of the summary in words')
@click.option('--lda-train', type=click.Path(exists=True), help='Directory of files to train the LDA model')
@click.option('--mail-summary', is_flag=True, help='Fetch and summarize emails')
@click.option('--time-interval', default=None, type=int, help='Time interval (in hours) for fetching emails')

def main(text_summary, file_summary, ocr_file, num_sentences, summary_length, lda_train, mail_summary, time_interval):
    text = ""
    lda_model = None

    if mail_summary:
        emails = getEmails(time_interval)
        for email in emails:
            no_words = (email['Message']).count(" ")
            if no_words > 80:
                no_words = no_words/3
            else:
                no_words = None
    
            email_summary = summarize_text(email['Message'], None, no_words)  # Summarize the email content
            print(f"Subject: {email['Subject']}")
            print(f"From: {email['From']}")
            print(f"Received: {email['Time']}")
            print(f"Summary: {email_summary}\n")
        return

    if lda_train:
        documents = [open(os.path.join(lda_train, f), 'r').read() for f in os.listdir(lda_train) if f.endswith(".txt")]
        lda_model = train_lda(documents)
        click.echo("LDA model trained successfully.")
        return

    if not text_summary and not file_summary and not ocr_file:
        click.echo("Please provide either --text-summary, --file-summary, or --ocr-file option.")
        return

    if (text_summary and file_summary) or (text_summary and ocr_file) or (file_summary and ocr_file):
        click.echo("Please provide only one of --text-summary, --file-summary, or --ocr-file option.")
        return

    if num_sentences and summary_length:
        click.echo("Please provide only one of --num-sentences or --summary-length option.")
        return

    if text_summary:
        text = text_summary
    elif file_summary:
        with open(file_summary, 'r') as f:
            text = f.read()
    elif ocr_file:
        result_text = perform_ocr(ocr_file)
        if result_text:
            text = result_text
        else:
            click.echo("OCR failed. Please check the image file path and try again.")
            return

    if not text:
        click.echo("No text provided to summarize.")
        return

    num_sentences = int(num_sentences) if num_sentences else None
    summary = summarize_text(text, num_sentences, summary_length, lda_model=lda_model)

    if num_sentences:
        click.echo(f"Summary ({num_sentences} sentences):\n{summary}")
    else:
        click.echo(f"Summary ({summary_length} words):\n{summary}")

if __name__ == '__main__':
    main()
