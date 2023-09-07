import json

# Path to your file
file_path = 'conv_sample'

def extract_text_from_data(data):
    try:
        post_list = data.get('post_list', [])
        if post_list:
            first_post = post_list[0]
            return first_post.get('text', 'Text not found')
        else:
            return 'No posts in the list'
    except KeyError:
        return 'Text extraction error'

def main():
    line_number = int(input("Enter the line number: "))
    
    with open(file_path, 'r') as file:
        data_lines = file.readlines()

    if 1 <= line_number <= len(data_lines):
        data_line = data_lines[line_number - 1]
        try:
            json_data = json.loads(data_line.strip())  # Strip newline characters
            
            # Print the entire JSON data for debugging
            # print(f"Data Point {line_number} JSON: {json_data}")
            
            text = extract_text_from_data(json_data)
            print(f"Data Point {line_number} Text: {text}")
        except json.JSONDecodeError:
            print(f"Error decoding JSON for Data Point {line_number}")
    else:
        print("Invalid line number")

if __name__ == "__main__":
    main()
