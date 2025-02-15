# ishaan tanwar
import os
import subprocess
import requests
import sqlite3
import duckdb
import json
import shutil
import markdown
from PIL import Image
import speech_recognition as sr
from bs4 import BeautifulSoup
from dateutil import parser
from git import Repo
import pandas as pd
import os
import json
import glob
import datetime
import openai
import pytesseract
from PIL import Image
from sentence_transformers import SentenceTransformer, util
import base64
import re
from llm_helper import query_llm
from utils import write_file, safe_path
import torch
import csv

# Define the safe path function
def safe_path(filename):
    return os.path.join(os.getcwd(), "data", filename)

# Define the secure data directory
DATA_DIR = r"C:\Users\Ishaan Tanwar\Desktop\VSCODE\Project 1\data"

def safe_path(file_name):
    full_path = os.path.abspath(os.path.join(DATA_DIR, file_name))
    if not full_path.startswith(os.path.abspath(DATA_DIR)):
        raise PermissionError(f"Access denied: {full_path} is outside {DATA_DIR}")
    return full_path



### **A5: Write the first line of the 10 most recent .log files**
def write_recent_log(task_description):
    matched_task = query_llm(f"Identify the correct task for: {task_description}")

    if "log" in matched_task.lower() and ("write" in matched_task.lower() or "first" in matched_task.lower() or "recent" in matched_task.lower()):
        log_dir = safe_path("logs")
        output_file = safe_path("logs-recent.txt")

        log_files = sorted(glob.glob(os.path.join(log_dir, "*.log")), key=os.path.getmtime, reverse=True)[:10]
        first_lines = []

        for file in log_files:
            with open(file, "r", encoding="utf-8") as f:
                first_line = f.readline().strip()
                if first_line:
                    first_lines.append(first_line)

        write_file(output_file, "\n".join(first_lines))
        return f"First lines written to {output_file}"
    else:
        raise Exception("LLM could not identify the correct task.")

# def write_recent_log_lines():
#     log_dir = safe_path("logs")  # Path to logs directory
#     output_file = safe_path("logs-recent.txt")  # Output file

#     # Get all .log files sorted by modification time (most recent first)
#     log_files = sorted(glob.glob(os.path.join(log_dir, "*.log")), key=os.path.getmtime, reverse=True)[:10]

#     first_lines = []
#     for file in log_files:
#         with open(file, "r", encoding="utf-8") as f:
#             first_line = f.readline().strip()
#             if first_line:
#                 first_lines.append(first_line)

#     # Write first lines to output file
#     with open(output_file, "w", encoding="utf-8") as f:
#         f.write("\n".join(first_lines))

#     return f"First lines written to {output_file}"


### **A6: Extract H1 headings from Markdown files and create an index**
def index_markdown(task_description):
    matched_task = query_llm(f"Identify the correct task for: {task_description}")

    if "markdown" in matched_task.lower() and ("header" in matched_task.lower() or "index" in matched_task.lower() or "extract" in matched_task.lower() or "h1" in matched_task.lower()):
        docs_dir = safe_path("docs")
        output_file = safe_path("docs/index.json")

        index = {}
        for md_file in glob.glob(os.path.join(docs_dir, "**/*.md"), recursive=True):
            filename = os.path.basename(md_file)
            with open(md_file, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("# "):
                        index[filename] = line.strip("# ").strip()
                        break

        write_file(output_file, json.dumps(index, indent=4))
        return f"Markdown index written to {output_file}"
    else:
        raise Exception("LLM could not identify the correct task.")

# def extract_markdown_headers():
#     docs_dir = safe_path("docs")  # Path to docs directory
#     output_file = safe_path("docs/index.json")  # Save inside docs folder

#     index = {}

#     # Recursively search all .md files inside /data/docs/
#     for md_file in glob.glob(os.path.join(docs_dir, "**/*.md"), recursive=True):
#         filename = os.path.basename(md_file)  # Extract only the filename (no folder names)

#         with open(md_file, "r", encoding="utf-8") as f:
#             for line in f:
#                 if line.startswith("# "):  # First occurrence of H1 heading
#                     index[filename] = line.strip("# ").strip()
#                     break  # Stop after finding the first H1

#     # Write index to JSON file inside /docs/
#     with open(output_file, "w", encoding="utf-8") as f:
#         json.dump(index, f, indent=4)

#     return f"Markdown index written to {output_file}"

'''
def extract_markdown_headers():
    docs_dir = safe_path("docs")  # Path to docs directory
    output_file = safe_path("docs/index.json")  # Output file

    index = {}

    for md_file in glob.glob(os.path.join(docs_dir, "*.md")):
        with open(md_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("# "):  # First occurrence of H1 heading
                    filename = os.path.relpath(md_file)
                    index[filename] = line.strip("# ").strip()
                    break  # Stop after finding the first H1

    # Write index to JSON file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=4)

    return f"Markdown index written to {output_file}"
'''

### **A7: Extract sender’s email from email.txt using LLM**



AIPROXY_URL = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
AIPROXY_TOKEN = os.environ.get("AIPROXY_TOKEN")

def extract_email_sender(task_description):
    matched_task = query_llm(f"Identify the correct task for: {task_description}")

    if "email" in matched_task.lower() and ("extract" in matched_task.lower() or "address" in matched_task.lower()):
        input_file = safe_path("email.txt")
        output_file = safe_path("email-sender.txt")

        with open(input_file, "r", encoding="utf-8") as f:
            email_content = f.read()

        headers = {"Authorization": f"Bearer {AIPROXY_TOKEN}", "Content-Type": "application/json"}
        data = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "Extract the sender's email address from the given email text."},
                {"role": "user", "content": email_content}
            ]
        }

        response = requests.post(AIPROXY_URL, headers=headers, json=data)
        if response.status_code == 200:
            extracted_email = response.json()["choices"][0]["message"]["content"].strip()
            write_file(output_file, extracted_email)
            return f"Extracted email: {extracted_email}"
        else:
            raise Exception(f"AI Proxy request failed: {response.text}")
    else:
        raise Exception("LLM could not identify the correct task.")



# def extract_email_sender():
#     input_file = safe_path("email.txt")  
#     output_file = safe_path("email-sender.txt")  

#     # Read email content
#     with open(input_file, "r", encoding="utf-8") as f:
#         email_content = f.read()

#     # Construct request for AI Proxy
#     headers = {
#         "Authorization": f"Bearer {AIPROXY_TOKEN}",
#         "Content-Type": "application/json"
#     }

#     data = {
#         "model": "gpt-4o-mini",
#         "messages": [
#             {"role": "system", "content": "Extract the sender's email address from the given email text."},
#             {"role": "user", "content": email_content}
#         ],
#         "temperature": 0.2
#     }

#     response = requests.post(AIPROXY_URL, headers=headers, json=data)

#     if response.status_code == 200:
#         extracted_email = response.json()["choices"][0]["message"]["content"].strip()
        
        # Write to output file
    #     with open(output_file, "w", encoding="utf-8") as f:
    #         f.write(extracted_email)

    #     return f"Extracted email: {extracted_email}"
    
    # else:
    #     raise Exception(f"AI Proxy request failed: {response.text}")
'''
def extract_email_sender():
    input_file = safe_path("email.txt")  # Email file
    output_file = safe_path("email-sender.txt")  # Output file

    with open(input_file, "r", encoding="utf-8") as f:
        email_content = f.read()

    # Call GPT-4o-Mini via AI Proxy
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "Extract the sender's email address from the given email content."},
                  {"role": "user", "content": email_content}],
        api_key=os.environ["AIPROXY_TOKEN"],
        base_url="https://aiproxy.sanand.workers.dev/openai/"
    )

    # Extract and save the email
    sender_email = response["choices"][0]["message"]["content"].strip()
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(sender_email)
    
    return sender_email
'''
'''
api_key = os.environ.get("AIPROXY_TOKEN")
if not api_key:
    raise ValueError("Missing AIPROXY_TOKEN. Set it before running.")

response = openai.ChatCompletion.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Extract sender's email: [email content]"}],
    temperature=0
)
'''
'''
def extract_email_sender():
    input_file = safe_path("email.txt")  # Email file
    output_file = safe_path("email-sender.txt")  # Output file

    with open(input_file, "r", encoding="utf-8") as f:
        email_content = f.read()

    # Use LLM (GPT) to extract sender email
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Extract the sender's email address from this email."},
            {"role": "user", "content": email_content}
        ]
    )

    sender_email = response["choices"][0]["message"]["content"].strip()

    # Write extracted email to output file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(sender_email)

    return f"Sender email written to {output_file}"
'''

### **A8: Extract credit card number from credit-card.png using OCR**
def extract_credit_card_number(task_description):
    matched_task = query_llm(f"Identify the correct task for: {task_description}")

    if "credit card" in matched_task.lower() and ("extract" in matched_task.lower() or "number" in matched_task.lower()):
        input_file = safe_path("credit_card.png")
        output_file = safe_path("credit-card.txt")

        with open(input_file, "rb") as f:
            image_base64 = base64.b64encode(f.read()).decode("utf-8")

        headers = {"Authorization": f"Bearer {AIPROXY_TOKEN}", "Content-Type": "application/json"}
        data = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "Extract the credit card number accurately from a PNG image. Return only the 16-digit number without spaces or dashes. Provide 'No number found' if extraction fails."},
                #{"role": "system", "content": "Extract only the credit card number accurately from the given image. Return only the number, nothing else. If no number is found then say no number available"},
                {"role": "user", "content": f"Extract the credit card number from this image: {image_base64}"}
            ]
        }

        response = requests.post(AIPROXY_URL, headers=headers, json=data)
        if response.status_code == 200:
            extracted_text = response.json()["choices"][0]["message"]["content"].strip()
            card_number = "".join(filter(str.isdigit, extracted_text))

            if not card_number:
                raise Exception("Failed to extract a valid credit card number.")

            write_file(output_file, card_number)
            return f"Extracted credit card number: {card_number}"
        else:
            raise Exception(f"AI Proxy request failed: {response.text}")
    else:
        raise Exception("LLM could not identify the correct task.")

# AIPROXY_URL = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
# AIPROXY_TOKEN = os.environ.get("AIPROXY_TOKEN")

# def extract_credit_card_number():
#     input_file = safe_path("credit_card.png")  # Image file
#     output_file = safe_path("credit-card.txt")  # Output file

#     # Read and encode image as base64
#     with open(input_file, "rb") as f:
#         image_base64 = base64.b64encode(f.read()).decode("utf-8")

#     # Construct request for AI Proxy
#     headers = {
#         "Authorization": f"Bearer {AIPROXY_TOKEN}",
#         "Content-Type": "application/json"
#     }

#     data = {
#         "model": "gpt-4o-mini",
#         "messages": [
#             {"role": "system", "content": "Extract only the credit card number from the given image text. Return only the number, nothing else."},
#             {"role": "user", "content": f"Extract the credit card number from this image: {image_base64}"}
#         ],
#         "temperature": 0.2
#     }

#     response = requests.post(AIPROXY_URL, headers=headers, json=data)

#     if response.status_code == 200:
#         extracted_text = response.json()["choices"][0]["message"]["content"].strip()

#         # Clean and format the response to extract only numbers
#         card_number = "".join(filter(str.isdigit, extracted_text))

#         if not card_number:
#             raise Exception("Failed to extract a valid credit card number.")

#         # Write to output file
#         with open(output_file, "w", encoding="utf-8") as f:
#             f.write(card_number)

#         return f"Extracted credit card number: {card_number}"
    
#     else:
#         raise Exception(f"AI Proxy request failed: {response.text}")
'''
def extract_credit_card_number():
    input_file = safe_path("credit_card.png")  # Image file
    output_file = safe_path("credit-card.txt")  # Output file

    # Perform OCR on the image
    image = Image.open(input_file)
    extracted_text = pytesseract.image_to_string(image)

    # AI Proxy endpoint & token
    openai.api_base = "https://aiproxy.sanand.workers.dev/openai/v1"
    openai.api_key = os.environ["AIPROXY_TOKEN"]

    # Use LLM to extract credit card number
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Extract only the credit card number from the given text. No spaces, no extra words."},
            {"role": "user", "content": extracted_text}
        ]
    )

    # Process response
    card_number = response["choices"][0]["message"]["content"].strip().replace(" ", "")

    # Write extracted number to output file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(card_number)


    return f"Credit card number written to {output_file}"
'''
'''
def extract_credit_card_number():
    input_file = safe_path("credit-card.png")  # Image file
    output_file = safe_path("credit-card.txt")  # Output file

    # Perform OCR on the image
    image = Image.open(input_file)
    extracted_text = pytesseract.image_to_string(image)

    # Use LLM to extract credit card number
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Extract only the credit card number from the given text."},
            {"role": "user", "content": extracted_text}
        ]
    )

    card_number = response["choices"][0]["message"]["content"].strip().replace(" ", "")

    # Write extracted number to output file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(card_number)

    return f"Credit card number written to {output_file}"
'''

### **A9: Find most similar pair of comments using embeddings**
def find_similar_comments(task_description):
    matched_task = query_llm(f"Identify the correct task for: {task_description}")

    if "similar comments" in matched_task.lower() or "compare comments" in matched_task.lower():
        input_file = safe_path("comments.txt")
        output_file = safe_path("comments-similar.txt")

        with open(input_file, "r", encoding="utf-8") as f:
            comments = [line.strip() for line in f.readlines() if line.strip()]

        if len(comments) < 2:
            return "Not enough comments to compare."

        headers = {"Authorization": f"Bearer {AIPROXY_TOKEN}", "Content-Type": "application/json"}
        data = {"model": "text-embedding-3-small", "input": comments}
        response = requests.post("https://aiproxy.sanand.workers.dev/openai/v1/embeddings", headers=headers, json=data)

        if response.status_code == 200:
            embeddings = [torch.tensor(item['embedding']) for item in response.json()['data']]
            similarity_matrix = util.pytorch_cos_sim(torch.stack(embeddings), torch.stack(embeddings))

            max_score = -1
            most_similar_pair = ("", "")

            for i in range(len(comments)):
                for j in range(i + 1, len(comments)):
                    score = similarity_matrix[i][j].item()
                    if score > max_score:
                        max_score = score
                        most_similar_pair = (comments[i], comments[j])

            write_file(output_file, f"{most_similar_pair[0]}\n{most_similar_pair[1]}")
            return f"Most similar comments written to {output_file}: {most_similar_pair}"
        else:
            raise Exception(f"AI Proxy request failed: {response.text}")
    else:
        raise Exception("LLM could not identify the correct task.")


#A 10
def calculate_gold_sales(task_description):
    matched_task = query_llm(f"Identify the correct task for: {task_description}")

    if "gold ticket sales" in matched_task.lower() or ("calculate gold sales" in matched_task.lower() or "gold ticket" in matched_task.lower() or "ticket sales" in matched_task.lower() or "total sales" in matched_task.lower()):
        db_path = safe_path("ticket-sales.db")
        output_file = safe_path("ticket-sales-gold.txt")

        total_sales = 0.0
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT units, price FROM tickets WHERE type = 'Gold'")
            rows = cursor.fetchall()

            for units, price in rows:
                total_sales += units * price

            conn.close()

            write_file(output_file, str(total_sales))
            return f"Total Gold ticket sales written to {output_file}: {total_sales}"
        except Exception as e:
            raise Exception(f"Error processing database: {e}")
    else:
        raise Exception("LLM could not identify the correct task.")
# def find_most_similar_comments():
#     input_file = safe_path("comments.txt")
#     output_file = safe_path("comments-similar.txt")

#     # Load comments from file
#     with open(input_file, "r", encoding="utf-8") as f:
#         comments = [line.strip() for line in f.readlines() if line.strip()]

#     if len(comments) < 2:
#         return "Not enough comments to compare."

#     # Load the sentence transformer model
#     model = SentenceTransformer("all-MiniLM-L6-v2")

#     # Compute embeddings for each comment
#     embeddings = model.encode(comments, convert_to_tensor=True)

#     # Find the most similar pair
#     similarity_matrix = util.pytorch_cos_sim(embeddings, embeddings)
#     max_score = -1
#     most_similar_pair = ("", "")

#     for i in range(len(comments)):
#         for j in range(i + 1, len(comments)):
#             score = similarity_matrix[i][j].item()
#             if score > max_score:
#                 max_score = score
#                 most_similar_pair = (comments[i], comments[j])

#     # Write the most similar comments to file
#     with open(output_file, "w", encoding="utf-8") as f:
#         f.write(most_similar_pair[0] + "\n")
#         f.write(most_similar_pair[1] + "\n")

#     return f"Most similar comments written to {output_file}: {most_similar_pair}"

# Example usage:
#result = find_most_similar_comments()
#print(result)
'''
def find_most_similar_comments():
    input_file = safe_path("comments.txt")
    output_file = safe_path("comments-similar.txt")

    # Load comments from file
    with open(input_file, "r", encoding="utf-8") as f:
        comments = [line.strip() for line in f.readlines() if line.strip()]

    if len(comments) < 2:
        return "Not enough comments to compare."

    # Load the sentence transformer model
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Compute embeddings for each comment
    embeddings = model.encode(comments, convert_to_tensor=True)

    # Find the most similar pair
    similarity_matrix = util.pytorch_cos_sim(embeddings, embeddings)
    max_score = -1
    most_similar_pair = ("", "")

    for i in range(len(comments)):
        for j in range(i + 1, len(comments)):
            score = similarity_matrix[i][j].item()
            if score > max_score:
                max_score = score
                most_similar_pair = (comments[i], comments[j])

    # Write the most similar comments to file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(most_similar_pair))

    return f"Most similar comments written to {output_file}: {most_similar_pair}"
'''

'''
def find_most_similar_comments():
    input_file = safe_path("comments.txt")  # Comments file
    output_file = safe_path("comments-similar.txt")  # Output file

    with open(input_file, "r", encoding="utf-8") as f:
        comments = [line.strip() for line in f.readlines() if line.strip()]

    if len(comments) < 2:
        return "Not enough comments to compare."

    # Load embedding model
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(comments, convert_to_tensor=True)

    # Find most similar pair
    max_sim = 0
    most_similar_pair = ("", "")

    for i in range(len(comments)):
        for j in range(i + 1, len(comments)):
            similarity = util.pytorch_cos_sim(embeddings[i], embeddings[j]).item()
            if similarity > max_sim:
                max_sim = similarity
                most_similar_pair = (comments[i], comments[j])

    # Write most similar comments to output file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"{most_similar_pair[0]}\n{most_similar_pair[1]}")

    return f"Most similar comments written to {output_file}"

'''

# PHASE A TASKS
#A2
def format_markdown(task_description):
    # task_description = "Format the contents of /data/format.md using prettier@3.4.2"
    matched_task = query_llm(f"Identify the correct task for: {task_description}")

    if "format" in matched_task.lower():
        file_path = safe_path("format.md")
        subprocess.run(["prettier", "--write", file_path], check=True, shell=True)
        return f"File formatted successfully: {file_path}"
    else:
        raise Exception("LLM could not identify the correct task.")
# def format_markdown():
#     file_path = safe_path("format.md")
#     subprocess.run(["prettier", "--write", file_path], check=True)
#     return f"File formatted successfully: {file_path}"


# A4
def sort_contacts(task_description):
    matched_task = query_llm(f"Identify the correct task for: {task_description}")

    if "sort" in matched_task.lower() and "contacts" in matched_task.lower():
        input_file = safe_path("contacts.json")
        output_file = safe_path("contacts-sorted.json")

        with open(input_file, "r", encoding="utf-8") as f:
            contacts = json.load(f)

        sorted_contacts = sorted(contacts, key=lambda x: (x["last_name"].strip().lower(), x["first_name"].strip().lower()))

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(sorted_contacts, f, indent=4, ensure_ascii=False)

        return f"Contacts sorted by last_name, then first_name, and saved to {output_file}"
    else:
        raise Exception("LLM could not identify the correct task.")
# def sort_contacts():
#     input_file = safe_path("contacts.json")
#     output_file = safe_path("contacts-sorted.json")

#     # Read contacts from JSON
#     with open(input_file, "r", encoding="utf-8") as f:
#         contacts = json.load(f)

#     print("Before Sorting:", contacts)  # Debug: Check if the data is correct

    # Sort by last_name, then first_name (case insensitive)
    sorted_contacts = sorted(contacts, key=lambda x: (x["last_name"].strip().lower(), x["first_name"].strip().lower()))

    print("After Sorting:", sorted_contacts)  # Debug: Check sorting output

    # Write sorted contacts to output file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(sorted_contacts, f, indent=4, ensure_ascii=False)

    return f"Contacts sorted by last_name, then first_name, and saved to {output_file}"

'''
import json
def sort_contacts():
    input_file = safe_path("contacts.json")
    output_file = safe_path("contacts-sorted.json")

    # Read contacts from JSON
    with open(input_file, "r", encoding="utf-8") as f:
        contacts = json.load(f)

    # Sort by last_name, then first_name (case insensitive)
    contacts = sorted(contacts, key=lambda x: (x["last_name"].lower(), x["first_name"].lower()))

    # Write sorted contacts to output file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(contacts, f, indent=4, ensure_ascii=False)

    return f"Contacts sorted by last_name, then first_name, and saved to {output_file}"
'''
'''
def sort_contacts():
    input_file = safe_path("contacts.json")
    output_file = safe_path("contacts-sorted.json")
    
    with open(input_file, "r") as f:
        contacts = sorted(f.readlines())

    with open(output_file, "w") as f:
        f.writelines(contacts)

    return f"Contacts sorted and saved to {output_file}"
'''
# A3
def count_wednesdays(task_description):
    day_map = {"sunday": 6, "monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3, "friday": 4, "saturday": 5}
    input_file = safe_path("dates.txt")
    output_file = safe_path("dates-wednesdays.txt")

    count = 0
    try:
        with open(input_file, "r") as file:
            for line in file:
                date_obj = parser.parse(line.strip())
                if date_obj.weekday() == day_map["wednesday"]:
                    count += 1
        write_file(output_file, str(count))
        return str(count)
    except Exception as e:
        raise Exception(f"Error processing file: {str(e)}")

# def count_wednesdays(task_description):
#     day_of_week = query_llm(f"Extract the weekday from this task description: {task_description}")
#     day_map = {"Sunday": 6, "Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4, "Saturday": 5}

#     if day_of_week not in day_map:
#         raise ValueError("Invalid day provided.")

#     input_file = safe_path("dates.txt") if "dates" in task_description else safe_path("extracts.txt")
#     output_file = safe_path("dates-wednesdays.txt") if "Wednesday" in day_of_week else safe_path("extracts-count.txt")

#     count = 0
#     with open(input_file, "r") as file:
#         for line in file:
#             try:
#                 date_obj = parser.parse(line.strip())
#                 if date_obj.weekday() == day_map[day_of_week]:
#                     count += 1
#             except Exception:
#                 continue

#     write_file(output_file, str(count))
#     return f"{day_of_week} count written to {output_file}: {count}"

# def sort_contacts():
#     # Implement sorting contacts and writing to /data/contacts-sorted.json
#     pass

# def write_recent_log():
#     # Implement writing recent logs to /data/logs-recent.txt
#     pass

# def index_markdown():
#     # Implement indexing markdown files and writing to /data/docs/index.json
#     pass

# def extract_email():
#     # Implement email extraction and writing to /data/email-sender.txt
#     pass

# def extract_card():
#     # Implement credit card extraction and writing to /data/credit-card.txt
#     pass

# def find_similar_comments():
#     # Implement finding similar comments and writing to /data/comments-similar.txt
#     pass

# def calculate_gold_sales():
#     # Implement calculating gold ticket sales and writing to /data/ticket-sales-gold.txt
#     pass

# def get_output_filename(task_name):
#     output_files = {
#         "count_wednesdays": "dates-wednesdays.txt",
#         "sort_contacts": "contacts-sorted.json",
#         "write_recent_log": "logs-recent.txt",
#         "index_markdown": "docs/index.json",
#         "extract_email": "email-sender.txt",
#         "extract_card": "credit-card.txt",
#         "find_similar_comments": "comments-similar.txt",
#         "calculate_gold_sales": "ticket-sales-gold.txt"
#     }
#     return safe_path(output_files.get(task_name, "output.txt"))
# def count_wednesdays(task_description):
#     # Use LLM to determine which day is being requested
#     day_of_week = query_llm(f"Extract the weekday from this task description: {task_description}")
#     day_map = {"Sunday": 6, "Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4, "Saturday": 5}

#     if day_of_week not in day_map:
#         raise ValueError("Invalid day provided.")

#     input_file = safe_path("dates.txt") if "dates" in task_description else safe_path("extracts.txt")
#     output_file = safe_path("dates-wednesdays.txt") if "Wednesday" in day_of_week else safe_path("extracts-count.txt")

#     count = 0
#     with open(input_file, "r") as file:
#         for line in file:
#             try:
#                 date_obj = parser.parse(line.strip())
#                 if date_obj.weekday() == day_map[day_of_week]:
#                     count += 1
#             except Exception:
#                 continue

#     write_file(output_file, str(count))
#     return f"{day_of_week} count written to {output_file}: {count}"
'''
def count_wednesdays():
    input_file = safe_path("dates.txt")
    output_file = safe_path("count-wednesdays.txt")
    
    wednesday_count = 0
    with open(input_file, "r") as file:
        for line in file:
            try:
                date_obj = parser.parse(line.strip())
                if date_obj.weekday() == 2:
                    wednesday_count += 1
            except Exception:
                continue

    with open(output_file, "w") as f:
        f.write(str(wednesday_count))

    return f"Wednesdays count written to {output_file}: {wednesday_count}"
'''
# PHASE B TASKS
# B3
def fetch_and_save_api_data(task_description):
    matched_task = query_llm(
        f"Phase B Task: Fetch API data. Only return the exact keyword 'fetch_api_data' with no formatting or code blocks."
    ).strip().lower()
# ishaanS
    # Handle LLM variations or formatting issues
    if 'fetch_api_data' in matched_task:
        api_url = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"  # Replace with actual API
        headers = {"Authorization": f"Bearer {AIPROXY_TOKEN}", "Content-Type": "application/json"}
        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            output_file = safe_path("api-data.json")
            write_file(output_file, response.text)
            return f"API data saved to {output_file}"
        elif response.status_code == 401:
            raise Exception("API request failed: 401 Unauthorized. Check API token.")
        else:
            raise Exception(f"API request failed: {response.status_code}")
    else:
        raise Exception(f"LLM Task Mismatch: Expected 'fetch_api_data', Received: {matched_task}")
# def fetch_api_data(task_description):
#     matched_task = query_llm(f"Identify the correct task for: {task_description}")

#     if "fetch api data" in matched_task.lower() or "get data from api" in matched_task.lower():
#         api_url = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"  # Replace with actual API
#         response = requests.get(api_url)

#         if response.status_code == 200:
#             output_file = safe_path("api-data.json")
#             write_file(output_file, response.text)
#             return f"API data saved to {output_file}"
#         else:
#             raise Exception(f"API request failed: {response.status_code}")
#     else:
#         raise Exception("LLM could not identify the correct task.")
# def fetch_api_data():
#     api_url = "http://127.0.0.1:8000/docs"
#     response = requests.get(api_url)
#     output_file = safe_path("api-response.json")
    
#     with open(output_file, "w") as f:
#         json.dump(response.json(), f, indent=4)

#     return f"API data saved to {output_file}"

# B4
def clone_and_commit_to_github(task_description):
    """Clones, commits, and pushes to the specified GitHub repository."""
    repo_url = "https://github.com/Ishaaann12/Project-1.git"
    remote_github = "https://github.com/Ishaaann12"
    local_path = "./data/project1_clone"

    try:
        if os.path.exists(local_path):
            subprocess.run(["rm", "-rf", local_path], check=True)
        subprocess.run(["git", "clone", repo_url, local_path], check=True)
        subprocess.run(["git", "-C", local_path, "config", "user.name", "Automation Agent"], check=True)
        subprocess.run(["git", "-C", local_path, "config", "user.email", "agent@example.com"], check=True)
        subprocess.run(["git", "-C", local_path, "remote", "set-url", "origin", f"{remote_github}/Project-1.git"], check=True)
        subprocess.run(["git", "-C", local_path, "add", "--all"], check=True)
        subprocess.run(["git", "-C", local_path, "commit", "--allow-empty", "-m", "Initial commit from automation agent"], check=True)
        subprocess.run(["git", "-C", local_path, "push", "origin", "main"], check=True)
        return "Repository cloned, committed, and pushed to Ishaaann12 GitHub."
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Git operation failed: {e}")
# def clone_and_commit_repo(task_description):
#     matched_task = query_llm(
#         "Phase B Task: Clone and commit a git repository. Return only the exact keyword 'git_clone_commit'."
#     ).strip().lower()

#     if 'git_clone_commit' in matched_task:
#         repo_url = "https://github.com/Ishaaann12/Project-1.git"  # Replace with actual URL
#         local_path = "./data/repo"

#         try:
#             subprocess.run(["git", "clone", repo_url, local_path], check=True)
#             subprocess.run(["git", "-C", local_path, "commit", "-am", "Initial commit from agent"], check=True)
#             return "Repository cloned and committed successfully."
#         except subprocess.CalledProcessError as e:
#             raise Exception(f"Git operation failed: {e}")
#     else:
#         raise Exception(f"LLM Task Mismatch: Expected 'git_clone_commit', Received: {matched_task}")

# def clone_git_repo(repo_url="https://github.com/example/repo.git"):
#     repo_dir = safe_path("git_repo")
#     if os.path.exists(repo_dir):
#         shutil.rmtree(repo_dir)
#     Repo.clone_from(repo_url, repo_dir)
#     return f"Repository cloned to {repo_dir}"

# B5
def run_sql_query(task_description, db_type="sqlite"):
    """Executes a SQL query on a SQLite or DuckDB database and saves the results."""
    output_file = safe_path("query-results.txt")
    query = "SELECT * FROM users LIMIT 10;"  # Example query (can be adjusted)
    
    try:
        if db_type == "sqlite":
            conn = sqlite3.connect(safe_path("database.sqlite"))
        elif db_type == "duckdb":
            conn = duckdb.connect(database=safe_path("database.duckdb"))
        else:
            raise ValueError("Unsupported database type")
        
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        
        # Format results for saving
        results = "\n".join([str(row) for row in rows])
        write_file(output_file, results)
        
        conn.close()
        return f"SQL query results saved to {output_file}"
    except Exception as e:
        return f"Error executing SQL query: {e}"
# def run_sql_query(db_type="sqlite", db_path="database.db", query="SELECT * FROM users"):
#     if "delete" in query.lower() or "drop" in query.lower():
#         return "Operation not allowed: DELETE and DROP statements are restricted."
    
#     db_file = safe_path(db_path)
#     conn = sqlite3.connect(db_file) if db_type == "sqlite" else duckdb.connect(db_file)
#     cursor = conn.cursor()
#     cursor.execute(query)
#     results = cursor.fetchall()
#     conn.close()
    
#     output_file = safe_path("query-results.json")
#     with open(output_file, "w") as f:
#         json.dump(results, f, indent=4)

#     return f"SQL results saved to {output_file}"

# B7
def compress_or_resize_image(task_description):
    """Compresses or resizes an image and saves the result."""
    input_path = safe_path("credit_card.png")
    output_path = safe_path("compressed_credit_card.png")

    try:
        with Image.open(input_path) as img:
            # Resize the image to a maximum width and height (e.g., 800x800) while maintaining aspect ratio
            img.thumbnail((800, 800))

            # Compress the image with quality setting
            img.save(output_path, format="PNG", optimize=True, quality=85)
        
        return f"Image compressed and saved to {output_path}"
    except Exception as e:
        return f"Error processing image: {e}"
# def scrape_website(url="https://example.com"):
#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, "html.parser")
    
#     output_file = safe_path("scraped-content.txt")
#     with open(output_file, "w", encoding="utf-8") as f:
#         f.write(soup.get_text())
    
#     return f"Scraped content saved to {output_file}"

# B6
def resize_image(image_name="input.jpg"):
    input_path = safe_path(image_name)
    output_path = safe_path(f"resized-{image_name}")
    
    with Image.open(input_path) as img:
        img.thumbnail((800, 800))
        img.save(output_path)
    
    return f"Resized image saved to {output_path}"

# B8
def transcribe_audio(audio_file="audio.mp3"):
    recognizer = sr.Recognizer()
    audio_path = safe_path(audio_file)
    
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
    
    text = recognizer.recognize_google(audio)
    output_file = safe_path("transcription.txt")
    
    with open(output_file, "w") as f:
        f.write(text)
    
    return f"Transcription saved to {output_file}"

# B9
def convert_markdown_to_html(file_name):
    """Searches for a specific Markdown file (ignoring prompt extras) and converts it to HTML."""
    # Clean input by removing extra words (e.g., 'Convert', 'to HTML')
    cleaned_name = file_name.lower().replace("convert", "").replace("to html", "").strip().replace("  ", " ")
    cleaned_name = cleaned_name if cleaned_name.endswith(".md") else cleaned_name + ".md"

    # Search for matching file name
    md_files = [f for f in glob.glob("**/*.md", recursive=True) if os.path.basename(f).lower() == cleaned_name.lower()]
    
    if not md_files:
        return f"No file named '{cleaned_name}' found in the project."

    md_file = md_files[0]  # Take the first matching file
    output_path = os.path.splitext(md_file)[0] + "_converted.html"

    try:
        with open(md_file, "r", encoding="utf-8") as file:
            md_content = file.read()

        html_content = markdown.markdown(md_content)
        write_file(output_path, html_content)
        
        return f"Markdown converted: {md_file} -> {output_path}"
    except Exception as e:
        return f"Error converting {md_file}: {e}"

# def convert_markdown_to_html(task_description):
#     """Converts a Markdown file to HTML and saves the output."""
#     input_path = safe_path("format.md")
#     output_path = safe_path("converted_to_html.html")

#     try:
#         with open(input_path, "r", encoding="utf-8") as file:
#             md_content = file.read()
        
#         # Convert Markdown to HTML
#         html_content = markdown.markdown(md_content)
#         write_file(output_path, html_content)
        
#         return f"Markdown converted to HTML and saved to {output_path}"
#     except Exception as e:
#         return f"Error converting Markdown to HTML: {e}"




# B10
import pandas as pd
import io
import json
from fastapi import UploadFile, HTTPException

# Core Function: Read Uploaded CSV and Return JSON
def read_csv_from_upload(file: UploadFile):
    try:
        contents = file.file.read()
        df = pd.read_csv(io.StringIO(contents.decode("utf-8")))
        return df.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing CSV: {e}")


# def filter_csv_data(csv_file="data.csv", column_name="Category", filter_value="Tech"):
#     input_path = safe_path(csv_file)
#     df = pd.read_csv(input_path)
    
#     filtered_df = df[df[column_name] == filter_value]
#     output_file = safe_path("filtered-data.json")
    
#     filtered_df.to_json(output_file, orient="records", indent=4)
#     return f"Filtered data saved to {output_file}"
