import json
import cld2
from collections import Counter

# Path to your file
file_path = 'conv_sample'

def truncate_text(text, max_length):
    if len(text) <= max_length:
        return text
    else:
        return text[:max_length - 3] + '...'

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
    start_line = 1
    num_datapoints = 100  # Number of data points to iterate through
    max_text_length = 100  # Maximum number of characters to display
    
    detected_languages = Counter()
    non_english_lines = []
    unknown_lines= []
    english_lines= []

    with open(file_path, 'r') as file:
        data_lines = file.readlines()

    for line_number in range(start_line, start_line + num_datapoints):
        if line_number <= len(data_lines):
            data_line = data_lines[line_number - 1]
            try:
                json_data = json.loads(data_line.strip())  # Strip newline characters
                
                text = extract_text_from_data(json_data)
                truncated_text = truncate_text(text, max_text_length)
                
                detected_lang = cld2.detect(text)
                detected_language = detected_lang[2][0][1] if detected_lang[0] else "Unknown"
                detected_languages[detected_language] += 1
                
                print(f"Data Point {line_number} Text: {truncated_text}")
                print(f"LANGUAGE: {detected_language}")

                if detected_language != 'en' and detected_language != 'Unknown':
                    non_english_lines.append(f"Data Point {line_number} classified as {detected_language}. Text: {truncated_text}")
                
                elif detected_language == 'Unknown':
                    unknown_lines.append(f"Data Point {line_number} classified as {detected_language}. Text: {truncated_text}")
                
                elif detected_language == 'en':
                    english_lines.append(f"Data Point {line_number} classified as {detected_language}. Text: {truncated_text}")

            except json.JSONDecodeError:
                print(f"Error decoding JSON for Data Point {line_number}")
        else:
            print(f"Line {line_number} is beyond the available data lines.")
    
    total_detected = sum(detected_languages.values())
    print("\nLanguage Detection Statistics:")
    for lang, count in detected_languages.items():
        percentage = (count / total_detected) * 100
        print(f"{lang.upper()}: {percentage:.2f}%")
    
    show_non_english = input("\nWould you like to see all Non-English lines? [y/n]: ")
    if show_non_english.lower() == 'y':
        print("\nNon-English Lines:")
        for line in non_english_lines:
            print(line)

    show_unknowns = input("\nWould you like to see all Unknown lines? [y/n]: ")
    if show_unknowns.lower() == 'y':
        print("\nUnknown Lines:")
        for line in unknown_lines:
            print(line)

    show_english = input("\nWould you like to see all English lines? [y/n]: ")
    if show_english.lower() == 'y':
        print("\nUnknown Lines:")
        for line in english_lines:
            print(line)

if __name__ == "__main__":
    main()
