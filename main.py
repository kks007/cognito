# File: my_assistant/main.py
import click
from document_summarization.summarizer import summarize_text
from document_summarization.ocr import perform_ocr

@click.command()
@click.option('--text', help='Text to summarize')
@click.option('--file', type=click.Path(exists=True), help='File to summarize or OCR')
@click.option('--num-sentences', default=3, help='Number of sentences in the summary')
@click.option('--summary-length', default=50, help='Desired length of the summary in words')
def main(text, file, num_sentences, summary_length):
    if not text and not file:
        click.echo("Please provide either --text or --file option.")
        return

    if text and file:
        click.echo("Please provide only one of --text or --file option.")
        return

    if file:
        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            result_text = perform_ocr(file)
            if result_text:
                click.echo(f"OCR Result:\n{result_text}\n")
            else:
                click.echo("OCR failed. Please check the image file path and try again.")
                return
        else:
            with open(file, 'r') as f:
                text = f.read()

    if num_sentences:
        summary = summarize_text(text, num_sentences)
        click.echo(f"Original Text:\n{text}\n")
        click.echo(f"Summary ({num_sentences} sentences):\n{summary}")
    else:
        summary = summarize_text(text, summary_length)
        click.echo(f"Original Text:\n{text}\n")
        click.echo(f"Summary ({summary_length} words):\n{summary}")

if __name__ == '__main__':
    main()
