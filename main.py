import os
import click
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


def main(text_summary, file_summary, ocr_file, num_sentences, summary_length, lda_train, mail_summary):
    # rest of the code...
    text = ""
    lda_model = None

    if mail_summary:
      # Call the function and store the emails in a variable
        emails = getEmails()

        # Print the emails
        for email in emails:
            print("Subject: ", email['Subject'])
            print("From: ", email['From'])
            print("Time: ", email['Time'])
            print("Message: ", email['Message'])
            print('\n')
        return
    
    if lda_train:
        documents = []
        for filename in os.listdir(lda_train):
            if filename.endswith(".txt"):
                with open(os.path.join(lda_train, filename), 'r') as f:
                    documents.append(f.read())
        lda_model = train_lda(documents)
        click.echo("LDA model trained successfully.")
        return

    if not text_summary and not file_summary and not ocr_file:
        click.echo("Please provide either --text-summary, --file-summary, or --ocr-file option.")
        return

    if (text_summary and file_summary) or (text_summary and ocr_file) or (file_summary and ocr_file):
        click.echo("Please provide only one of --text-summary, --file-summary, or --ocr-file option.")
        return

    if text_summary:
        text = text_summary
    elif file_summary:
        with open(file_summary, 'r') as f:
            text = f.read()
    elif ocr_file:
        result_text = perform_ocr(ocr_file)
        if result_text:
            click.echo(f"OCR Result:\n{result_text}\n")
            return
        else:
            click.echo("OCR failed. Please check the image file path and try again.")
            return

    num_sentences = int(num_sentences) if num_sentences else None
    if num_sentences:
        summary = summarize_text(text, num_sentences, lda_model=lda_model)
        click.echo(f"Summary ({num_sentences} sentences):\n{summary}")
    else:
        summary = summarize_text(text, summary_length, lda_model=lda_model)
        click.echo(f"Summary ({summary_length} words):\n{summary}")

if __name__ == '__main__':
    main()