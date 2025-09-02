import re

from pathlib import Path

from app.models.subtitle import Subtitle


MAX_LINES = 3

def parse_subtitle_paragraph(subtitle_text:str) -> Subtitle|None:
    """Parse a subtitle block and return a Subtitle object.

    Args:
        subtitle_text (str): Text of the subtitle block

    Returns:
        Subtitle: Subtitle object or None if parsing fails
    """
    lines = subtitle_text.strip().split('\n')

    if len(lines) < MAX_LINES:
        return None

    try:
        # First line: index
        lines[0] = lines[0].replace("\ufeff", "").strip() # Remove BOM if present
        index = int(lines[0])

        # Second line: timestamps
        timestamp_line = lines[1]
        start, end = timestamp_line.split(' --> ')

        # Following lines: text
        text = '\n'.join(lines[2:])

        return Subtitle(index, int(start), int(end), text)

    except (ValueError, IndexError) as e:
        print(f"Error during parsing: {e}")
        return None

def split_subtitles(text: str) -> list:
    """More precise version that also captures subtitle numbers."""
    # Pattern that captures the number and separates it
    pattern = r'(\n|^)(\d{1,5})\n'

    # Split while keeping numbers as markers
    parts = re.split(pattern, text)

    paragraphs = []
    index_str = ''
    for part in parts:
        if part.strip() and part.strip().isdigit():
            index_str = part.strip()
        elif index_str:
                s = parse_subtitle_paragraph(f"{index_str}\n{part.strip()}")
                if s:
                    paragraphs.append(s)
                index_str = ''
        else:
            s = parse_subtitle_paragraph(part.strip())
            if s:
                paragraphs.append(s)

    return paragraphs

def process_subtitle_file(file_path:str) -> list:
    """Process a complete subtitle file.

    Args:
        file_path (str): Path to the subtitle file

    Returns:
        list: List of paragraphs
    """
    try:
        with Path(file_path).open(mode='r', encoding='utf-8') as file:
            content = file.read()
        return split_subtitles(content)
    except FileNotFoundError:
        print(f"File {file_path} not found")
        return []
    except Exception as e:
        print(f"Error reading file: {e}")
        return []
