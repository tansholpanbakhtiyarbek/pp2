def snake_to_camel(text):
    parts = text.split('_')
    return parts[0] + ''.join(word.capitalize() for word in parts[1:])

text = "snake_case_string"
print(snake_to_camel(text))