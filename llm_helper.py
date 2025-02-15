import requests
from dotenv import load_dotenv
import os   
import json
from fastapi import HTTPException
load_dotenv()

# API_PROXY_TOKEN = os.getenv("eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjI0ZHMzMDAwMDMyQGRzLnN0dWR5LmlpdG0uYWMuaW4ifQ.-xGMyxXYRNdZc3_uTeLjPYTh69OibQEQhQAqbZwRYTE")
# API_PROXY_URL = "https://aiproxy.sanand.workers.dev/openai/"

# def query_llm_for_task(prompt: str):
#     headers = {"Authorization": f"Bearer {API_PROXY_TOKEN}"}
#     data = {"prompt": f"Match this task to a known command: {prompt}", "max_tokens": 50}
#     response = requests.post(API_PROXY_URL, headers=headers, json=data)
#     if response.status_code == 200:
#         return response.json().get("result").strip()
#     else:
#         raise Exception(f"Error querying LLM: {response.status_code}")

# # def query_llm(prompt: str):
# #     headers = {"Authorization": f"Bearer {API_PROXY_TOKEN}"}
# #     data = {"prompt": prompt, "max_tokens": 150}
# #     response = requests.post(API_PROXY_URL, headers=headers, json=data)
# #     if response.status_code == 200:
# #         return response.json().get("result").strip()
# #     else:
# #         raise Exception(f"Error querying LLM: {response.status_code}")
    
# def query_llm(prompt: str):
#     headers = {
#         "Authorization": f"Bearer {API_PROXY_TOKEN}",
#         "Content-Type": "application/json"
#     }
#     data = {
#         "model": "gpt-4o-mini",  # Required model parameter
#         "messages": [
#             {"role": "user", "content": prompt}
#         ]
#     }

#     response = requests.post(API_PROXY_URL, headers=headers, json=data)

#     if response.status_code == 200:
#         return response.json()["choices"][0]["message"]["content"].strip()
#     else:
#         error_message = response.json().get("error", {}).get("message", "Unknown error")
#         raise Exception(f"Error querying LLM: {response.status_code} - {error_message}")


API_PROXY_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjI0ZHMzMDAwMDMyQGRzLnN0dWR5LmlpdG0uYWMuaW4ifQ.-xGMyxXYRNdZc3_uTeLjPYTh69OibQEQhQAqbZwRYTE"
API_PROXY_URL = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"

# def query_llm_for_task(prompt: str):
#     headers = {
#         "Authorization": f"Bearer {API_PROXY_TOKEN}",
#         "Content-Type": "application/json"
#     }
#     data = {
#         "model": "gpt-4o-mini",
#         "messages": [{"role": "user", "content": f"Match this task to a known command: {prompt}"}]
#     }
#     response = requests.post(API_PROXY_URL, headers=headers, json=data)
#     if response.status_code == 200:
#         return response.json()["choices"][0]["message"]["content"].strip()
#     else:
#         error_message = response.json().get("error", {}).get("message", "Unknown error")
#         raise Exception(f"Error querying LLM: {response.status_code} - {error_message}")

# def query_llm_for_task(prompt: str):
#     headers = {
#         "Authorization": f"Bearer {API_PROXY_TOKEN}",
#         "Content-Type": "application/json"
#     }
#     data = {
#         "model": "gpt-4o-mini",
#         "messages": [
#             {"role": "system", "content": "You are an assistant that understands tasks in multiple languages and maps them to internal functions for Phase A tasks."},
#             {"role": "user", "content": prompt}
#         ]
#     }
#     response = requests.post(API_PROXY_URL, headers=headers, json=data)
#     if response.status_code == 200:
#         return response.json()["choices"][0]["message"]["content"].strip()
#     else:
#         raise Exception(f"Error querying LLM: {response.status_code}")
    
def query_llm_for_task(prompt: str):
    headers = {
        "Authorization": f"Bearer {API_PROXY_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are a multilingual assistant that maps any given task to the correct internal function. The supported tasks include: count_wednesdays, format_markdown, sort_contacts, write_recent_log, index_markdown, extract_email_sender, extract_credit_card_number, find_similar_comments, calculate_gold_sales, enforce_data_access, fetch_api_data, git_clone_commit, run_sql_query, compress_or_resize_image, convert_markdown_to_html,. Return only the exact function name."},
            {"role": "user", "content": prompt}
        ]
    }
    response = requests.post(API_PROXY_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"].strip()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    

def query_llm(prompt: str):
    headers = {
        "Authorization": f"Bearer {API_PROXY_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4o-mini",  # Correct model parameter
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(API_PROXY_URL, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"].strip()
    else:
        error_message = response.json().get("error", {}).get("message", "Unknown error")
        raise Exception(f"Error querying LLM: {response.status_code} - {error_message}")