

def contains_word(text: str, word_list: list[str]) -> bool:
    """
    Utility function to check if a text contains a word from a given list.

    Args:
        text (str): The text to check.
        word_list (list): The list of words to check for.

    Returns:
        bool: True if the text contains a word from the list, False otherwise.
    """
    for word in word_list:
        if word.lower() in text.lower():
            return True
    return False

# Example usage
text = "motocar"
word = "car"

if contains_word(text, ["on",'ki']):
  print(f"'{word}' is found entirely within '{text}'.")
else:
  print(f"'{word}' is not found entirely within '{text}'.")