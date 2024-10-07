# Cognito

Personal workflow assistant

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

EDITH is a personal workflow assistant designed to help streamline various tasks such as document summarization, OCR, and email fetching. It leverages multiple libraries and APIs to provide a comprehensive tool for managing your workflow efficiently.

## Features

- Convert PDF documents to Word format using `pdf2docx`.
- Perform OCR on images using `pytesseract`.
- Summarize documents using NLP techniques with `nltk` and `gensim`.
- Fetch and process emails using the Gmail API.
- User-friendly interface built with `tkinter` and `ttkbootstrap`.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/sidd1092/edith.git
    cd edith
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Set up the Google API credentials for email fetching:
    - Follow the instructions [here](https://developers.google.com/gmail/api/quickstart/python) to create credentials.
    - Save the `credentials.json` file in the project directory.

## Usage

1. Run the main application:
    ```sh
    python main.py
    ```

2. Use the GUI to perform various tasks such as converting PDFs, performing OCR, summarizing documents, and fetching emails.
    ```sh
    python main-ui.py
    ```
    
## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
