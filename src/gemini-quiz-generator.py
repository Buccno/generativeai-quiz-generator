import google.generativeai as genai
import os

os.environ["API_KEY"] = 'YOUR_API_KEY'
genai.configure(api_key=os.environ["API_KEY"])

def generate_questions(text, num_questions=10):
    questions = []
    for i in range(num_questions):
        for attempt in range(5):  
            prompt = f"""
            Your task is to generate a unique multiple-choice question based on the information in the passage. Each question should be clear, concise, and directly related to the text provided.
            
            Please structure your response with the following format:

            1. Begin with "Question:" followed by the question text.
            2. Provide four answer options labeled (a), (b), (c), and (d). Each option should be concise and relevant.
            3. Conclude with "Answer:" followed by the correct answer option in the format "a)", "b)", "c)", or "d)".

            Ensure that:
            - The question covers important ideas or details from the text, without limiting to a single topic unless specified by the text.
            - Each option is distinct, clear, and plausible based on the information in the passage.
            - Avoid trivial or obvious answers that are not aligned with the text content.
            - The format is exactly as shown below to avoid invalid responses.

            Example format:
            Question: question?
            a) Answer 1
            b) Answer 2
            c) Answer 3
            d) Answer 4
            Answer: b)
            
            Text: {text}
            
            Please generate Question {i+1}:
            """

            # Model Configuration
            model_config = {
              "temperature": 1,
              "top_p": 0.99,
              "top_k": 0,
              "max_output_tokens": 4096,
            }

            model = genai.GenerativeModel('gemini-1.5-flash-latest', 
                                          generation_config=model_config)
            
            response = model.generate_content(prompt)
            if response.text and "Invalid question format" not in response.text:
                questions.append(response.text.strip())
                break 
            else:
                print(f"No valid response received for question {i + 1}. Attempt {attempt + 1} of 5.")
        
        else:
            print(f"Failed to generate a valid question for question {i + 1} after 5 attempts.")
            questions.append("Question: Unable to generate a valid question.")
    
    return questions

def generate_html_output(questions):
    html_output = "<html><head><style>\n"
    html_output += "button { margin-top: 10px; }\n"
    html_output += "</style></head><body><h2>Quiz</h2><ol>\n"
    
    for i, question in enumerate(questions, 1):
        # Extract question text and options
        question_text, options = extract_question_and_options(question)
        html_output += f"<li>{question_text}<br>\n"
        for option in options:
            html_output += f"<input type='radio' name='question{i}' value='{option}'> {option}<br>\n"
        html_output += f"<button onclick=\"showAnswer('answer{i}')\">Show Answer</button>\n"
        html_output += f"<p id='answer{i}' style='display:none;'>Answer: {extract_answer(question)}</p></li>\n"
    
    html_output += "</ol>\n<script>\n"
    html_output += "function showAnswer(id) {\n"
    html_output += "  var answer = document.getElementById(id);\n"
    html_output += "  answer.style.display = answer.style.display === 'none' ? 'block' : 'none';\n"
    html_output += "}\n</script>\n</body></html>"
    
    return html_output

def extract_question_and_options(question_text):
    lines = question_text.splitlines()
    question_part = None
    options = []
    
    for line in lines:
        line = line.strip()
        if line.lower().startswith("question:"):
            question_part = line.split(":", 1)[1].strip()
        elif line.startswith("a)") or line.startswith("b)") or line.startswith("c)") or line.startswith("d)"):
            options.append(line.strip())
    
    return question_part, options

def extract_answer(question_text):
    lines = question_text.splitlines()
    for line in lines:
        if line.lower().startswith("answer:"):
            return line.split(":", 1)[1].strip()
    return "Answer not provided"

# Read the text from the `input.txt` file
with open("input/input.txt", "r", encoding="utf-8") as file:
    text = file.read()

# Check if the input file is empty and notify the user if it is
if not text.strip():  # Checks if the file content is empty or whitespace
    print("The input file is empty. Please provide content in input.txt and try again.")
else:
    # Generate questions based on the text
    questions = generate_questions(text)

    # Generate HTML output with the questions
    html_output = generate_html_output(questions)

    # Save the HTML output to a file
    with open("questions.html", "w", encoding="utf-8") as file:
        file.write(html_output)

    print("HTML file created with multiple-choice questions.")
