from fastapi import FastAPI, Query, HTTPException, Request, File, UploadFile
from pydantic import BaseModel
import tasks
import os
import json
app = FastAPI()
from llm_helper import query_llm_for_task
from tasks import count_wednesdays , format_markdown, sort_contacts, write_recent_log, index_markdown, extract_email_sender, extract_credit_card_number, find_similar_comments, calculate_gold_sales, fetch_and_save_api_data, clone_and_commit_to_github, run_sql_query, compress_or_resize_image, convert_markdown_to_html, read_csv_from_upload

# from prevent_file_deletion import PreventFileDeletionMiddleware
# app.add_middleware(PreventFileDeletionMiddleware)

# from enforce_data_access import EnforceDataAccessMiddleware
# app.add_middleware(EnforceDataAccessMiddleware)
# # Security constraints (B1 & B2)
SECURE_DATA_DIR = "./data"

# Define request model for JSON body support
class TaskRequest(BaseModel):
    task: str


# @app.post("/run")
# async def run_task(request: TaskRequest):
#     """Run a task based on JSON request body."""
#     print(f"Received request: {request}")  # Debugging line
#     print(f"Available tasks: {list(TASK_MAPPING.keys())}")

#     task_name = request.task

#     if task_name not in TASK_MAPPING:
#         raise HTTPException(status_code=400, detail="Unknown task")

#     try:
#         result = TASK_MAPPING[task_name]()
#         return {"status": "success", "task": task_name, "result": result}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# Task Handler


# task_handlers = {
#     "count_wednesdays": tasks.count_wednesdays
# }

# @app.post("/run")
# def run_task(task: str):
#     try:
#         matched_task = query_llm_for_task(task)
#         if "count wednesdays" in matched_task.lower() or "mercredi" in matched_task.lower() or "miércoles" in matched_task.lower():
#             return tasks.count_wednesdays()
#         else:
#             raise HTTPException(status_code=400, detail="Unknown task")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
    
# @app.post("/run")
# def run_task(task: str):
#     try:
#         matched_task = query_llm_for_task(task)
#         task_handlers = {
#             "count_wednesdays": tasks.count_wednesdays,
#             # Add more tasks here
#     }
#         handler = task_handlers.get(matched_task)
#         if handler:
#             return handler()
#         else:
#             raise HTTPException(status_code=400, detail="Unknown task")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
# @app.post("/run")
# def run_task(task: str):
#     matched_task = query_llm_for_task(task)
#     task_handlers = {
#         "count_wednesdays": tasks.count_wednesdays,
#         "sort_contacts": tasks.sort_contacts,
#         "write_recent_log": tasks.write_recent_log,
#         "index_markdown": tasks.index_markdown,
#         "extract_email": tasks.extract_email,
#         "extract_card": tasks.extract_card,
#         "find_similar_comments": tasks.find_similar_comments,
#         "calculate_gold_sales": tasks.calculate_gold_sales
#     }

#     for key, handler in task_handlers.items():
#         if key in matched_task.lower():
#             result = handler()
#             output_file = tasks.get_output_filename(key)
#             with open(output_file, "w") as file:
#                 file.write(result)
#             return {"message": f"Output written to {output_file} for {key}", "result": result}

#     raise HTTPException(status_code=400, detail="Unknown task")


@app.post("/run")
def run_task(task: str):
    matched_task = query_llm_for_task(task)
    task_handlers = {
        "count_wednesdays": count_wednesdays,
        "format_markdown": format_markdown,
        "sort_contacts": sort_contacts,
        "write_recent_log": write_recent_log,
        "index_markdown": index_markdown,
        "extract_email_sender": extract_email_sender,
        "extract_credit_card_number": extract_credit_card_number,
        "find_similar_comments": find_similar_comments,
        "calculate_gold_sales": calculate_gold_sales,
        #Phase B tasks
        # "enforce_data_access": enforce_data_access
        "fetch_api_data": fetch_and_save_api_data,
        "git_clone_commit": clone_and_commit_to_github,
        "run_sql_query": run_sql_query,
         "compress_or_resize_image": compress_or_resize_image,
         "convert_markdown_to_html": convert_markdown_to_html,

    }
    handler = task_handlers.get(matched_task.lower())
    if handler:
        try:
            result = handler(task)
            return {"message": "Task completed", "result": result}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Task execution error: {str(e)}")
    else:
        raise HTTPException(status_code=400, detail="Task not found")

# Task Mapping
# TASK_MAPPING = {
#     # Phase B Tasks
#     "Fetch API data": tasks.fetch_api_data,
#     "Clone git repo and commit": tasks.clone_git_repo,  # Correct function name

#     "Run SQL query": tasks.run_sql_query,
#     "Extract website data": tasks.scrape_website,
#     "Compress image": tasks.resize_image,
#     "Transcribe MP3": tasks.transcribe_audio,
#     "Convert Markdown to HTML": tasks.convert_md_to_html,
#     "Write the first line of the 10 most recent .log files": tasks.write_recent_log_lines,
#     "Extract H1 headings from Markdown files": tasks.extract_markdown_headers,
#     "Extract sender email from email.txt": tasks.extract_email_sender,
#     "Extract credit card number from image": tasks.extract_credit_card_number,
#     "Find most similar comments": tasks.find_most_similar_comments,
#     "Filter CSV and return JSON": tasks.filter_csv_data,
#     # Phase B Tasks
#     "Format Markdown file": tasks.format_markdown,
#     "Sort contacts": tasks.sort_contacts,
#     "Count Wednesdays in date file": tasks.count_wednesdays,
#     "Fetch data from API": tasks.fetch_api_data,
#     "Clone a Git repository": tasks.clone_git_repo,
#     "Run SQL query (secure)": tasks.run_sql_query,
#     "Scrape a website": tasks.scrape_website,
#     "Resize an image": tasks.resize_image,
#     "Transcribe audio file": tasks.transcribe_audio,
#     "Convert Markdown to HTML (secure)": tasks.convert_md_to_html,
#     "Filter CSV data": tasks.filter_csv_data
# }
'''
@app.post("/run")
def run_task(request: TaskRequest):
    """Run a task based on JSON request body."""
    task_name = request.task

    if task_name not in TASK_MAPPING:
        raise HTTPException(status_code=400, detail="Unknown task")

    try:
        result = TASK_MAPPING[task_name]()
        return {"status": "success", "task": task_name, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
'''
@app.get("/read")
def read_data(path: str = Query(..., description="File path inside /data")):
    """Read a file inside the secure data directory."""
    full_path = os.path.join(SECURE_DATA_DIR, path)  

    if ".." in path or not full_path.startswith(SECURE_DATA_DIR):
        raise HTTPException(status_code=403, detail="Access denied")

    try:
        with open(full_path, "r", encoding="utf-8") as file:
            content = file.read()

        # ✅ If it's JSON, clean the keys (filenames)
        if path.endswith(".json"):
            try:
                json_data = json.loads(content)
                
                # Remove any unwanted prefixes in filenames
                cleaned_data = {os.path.basename(k): v for k, v in json_data.items()}
                
                return {"content": cleaned_data}  # Return cleaned JSON
            except json.JSONDecodeError:
                pass  # If not JSON, return as plain text

        return {"content": content}  # Return as-is for non-JSON files

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")

'''
@app.get("/read")
def read_data(path: str = Query(..., description="Path to file inside /data")):
    """Read a file inside the secure data directory."""
    if ".." in path or not path.startswith(SECURE_DATA_DIR):
        raise HTTPException(status_code=403, detail="Access denied")

    try:
        with open(path, "r") as file:
            return {"content": file.read()}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
'''
'''
@app.get("/read")
def read_data(path: str = Query(..., description="File path inside /data")):
    """Read a file inside the secure data directory."""
    full_path = os.path.join(SECURE_DATA_DIR, path)  

    if ".." in path or not full_path.startswith(SECURE_DATA_DIR):
        raise HTTPException(status_code=403, detail="Access denied")

    try:
        with open(full_path, "r", encoding="utf-8") as file:
            return {"content": file.read()}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
'''
# # @app.middleware("http")
# def enforce_data_access(request: Request, call_next):
#     if not request.url.path.startswith("/data"):
#         raise HTTPException(status_code=403, detail="Access outside /data is not allowed")
#     response = call_next(request)
#     return response
# async def enforce_data_access(request: Request, call_next):
#     if request.url.path.startswith("/data") or request.url.path == "/run":
#         response = await call_next(request)
#         return response
#     else:
#         raise HTTPException(status_code=403, detail="Access outside /data is forbidden")


# @app.get("/tasks")
# def list_tasks():
#     """Return a list of available tasks."""
#     return {"available_tasks": list(TASK_MAPPING.keys())}

@app.get("/")
def read_root():
    return {"message": "API is working!"}

# API Endpoint: Upload CSV and Get JSON
@app.post("/upload-csv/")
def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a CSV file.")
    
    try:
        data = read_csv_from_upload(file)
        return {"message": "CSV processed successfully", "data": data}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")



@app.delete("/run")
def run_delete_task(task: str):
    raise HTTPException(status_code=403, detail="File deletions are not allowed")