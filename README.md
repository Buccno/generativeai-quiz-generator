# Quiz Generator

### Overview

This project aims to help retain key concepts from texts that are difficult to practice regularly. By generating quiz questions from input text, it makes it easier to reinforce and remember essential information.

To use this tool:
1. Place the text from which you want to generate questions in `input.txt` (located in the `input` folder).
2. Set up the requirements and add your Gemini AI API key in the specified line in the Python script.
3. Run the `quiz-generator.bat` file.

The result will be a 10-question quiz generated from your input text.


**Note**: If you want to save the generated questions with a specific topic title, you can modify line 121 of the Python code:

```python
with open("questions.html", "w", encoding="utf-8") as file:
    # Replace "questions.html" with a filename of your choice, such as "desired_topic_title.html".
```

## Prerequisites

- Python 3.10
- Gemini AI API key

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/Buccno/generativeai-quiz-generator.git
    ```

2. **Set up your API key**:
    Open the Python code and enter your Gemini API key on the designated line.

## Running the Project

Simply double-click `quiz-generator.bat` to start the process. This will generate a 10-question quiz from the text in `input/input.txt`.
