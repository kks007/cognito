# File: my_assistant/main.py
import click
from document_summarization.summarizer import summarize_text
from document_summarization.ocr import perform_ocr

@click.command()
@click.option('--text-summary', help='Text to summarize')
@click.option('--file-summary', type=click.Path(exists=True), help='File to summarize')
@click.option('--ocr-file', type=click.Path(exists=True), help='File to perform OCR')
@click.option('--num-sentences', default=3, help='Number of sentences in the summary')
@click.option('--summary-length', default=50, help='Desired length of the summary in words')
def main(text_summary, file_summary, ocr_file, num_sentences, summary_length):
    text = ""

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

    if num_sentences:
        summary = summarize_text(text, num_sentences)
        click.echo(f"Summary ({num_sentences} sentences):\n{summary}")
    else:
        summary = summarize_text(text, summary_length)
        click.echo(f"Summary ({summary_length} words):\n{summary}")

if __name__ == '__main__':
    main()
