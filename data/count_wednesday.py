from dateutil import parser
import os

# Set the absolute path of the directory
script_dir = r"C:\Users\Ishaan Tanwar\Desktop\VSCODE\Project 1\data"

# Define the paths to the input and output files
input_file = os.path.join(script_dir, "dates.txt")
output_file = os.path.join(script_dir, "count-wednesdays.txt")

wednesday_count = 0

# Read dates and count Wednesdays
try:
    with open(input_file, "r") as file:
        for line in file:
            date_str = line.strip()
            try:
                date_obj = parser.parse(date_str)
                if date_obj.weekday() == 2:  # 2 represents Wednesday
                    wednesday_count += 1
            except (ValueError, parser.ParserError):
                continue

    # Write the result to the output file
    with open(output_file, "w") as output_file:
        output_file.write(str(wednesday_count))

    print(f"Wednesdays count written to {output_file}: {wednesday_count}")

except FileNotFoundError as e:
    print(f"Error: {e.strerror}. Please make sure the file exists at {input_file}")