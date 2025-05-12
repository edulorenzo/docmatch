import os
from utils import load_text, calculate_match

JOB_DESC_PATH = 'job_description.txt'
CV_FOLDER = 'cvs/'

def main():
    if not os.path.exists(JOB_DESC_PATH):
        print("❌ Missing job_description.txt")
        return

    job_desc = load_text(JOB_DESC_PATH)
    print("🔍 Comparing CVs against job description...\n")

    for filename in os.listdir(CV_FOLDER):
        file_path = os.path.join(CV_FOLDER, filename)
        text = load_text(file_path)
        if text:
            score = calculate_match(text, job_desc)
            print(f"{filename} → Match Score: {score:.2f}%")

if __name__ == '__main__':
    main()
