def cleanup_text(text: str) -> str:
    text = text.replace("\r\n", "\n")
    text = remove_blank_lines_at_eof(text)
    return text


def remove_blank_lines_at_eof(text: str) -> str:
    return text.rstrip() + "\n"
