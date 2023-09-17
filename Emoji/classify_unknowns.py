import re
import cld2

def classify_unknowns(unknown_lines, language):
    classified_results = []
    chinese_count = 0  # Initialize a count for Chinese lines

    if language == "Chinese":

        # Define a regular expression pattern to match Chinese characters
        chinese_pattern = re.compile(r'[\u4e00-\u9fa5]+')

        for line in unknown_lines:
            # Filter out non-Chinese characters
            chinese_text = ''.join(chinese_pattern.findall(line))

            # Check if there's any Chinese text left
            if chinese_text:
                chinese_count += 1  # Increment the count for Chinese lines

                # Detect the language of the remaining text
                result = cld2.detect(chinese_text)
                detected_language = result[2][0][1] if result[0] else "Unknown"

                # Check if the detected language matches the expected language
                if detected_language.lower() == language.lower():
                    classified_results.append("Chinese")
                else:
                    classified_results.append(detected_language)
            else:
                classified_results.append("No Chinese characters")

    # Calculate the percentage of lines that contain Chinese
    total_lines = len(unknown_lines)
    chinese_percentage = (chinese_count / total_lines) * 100
    print(f"Lines containing Chinese: {chinese_count} out of {total_lines} ({chinese_percentage:.2f}%)")

    return


# Example usage:
unknown_lines = [
    "你好，这是一段中文文本。",
    "Hello, this is a mixed text with 中文 characters.",
    "This line has no Chinese characters at all.",
]

# language = "Chinese"
# results = classify_unknowns(unknown_lines, language)
# for line, result in zip(unknown_lines, results):
#     print(f"Line: {line} -> Classification: {result}")
