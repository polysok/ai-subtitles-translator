import json
import os
import sys

from pathlib import Path

import click

from app.tools.json_extraction import JSONExtractor
from app.tools.llm import stream_request_llm_server
from app.tools.translation import process_subtitle_file


MAX_CONCAT_SUBTITLES = 5

def main() -> None:
    """Main function to run by default."""
    source = input("Enter the path to the subtitle file to translate:").strip()
    language = input("Enter the target language (e.g., French, Spanish):").strip()
    cli(source, "auto",language)

@click.command()
@click.argument("source", type=click.File("rb"), nargs=-1)
@click.argument("destination", type=click.File("wb"))
@click.argument("language", type=click.STRING, default="French")
def cli(source:str, destination:str, language:str) -> None:
    """Command line interface for subtitle translation."""
    # check if the file exists and create a output file based on the input file name
    if source.startswith("'"):
        source = source[1:-1]
    if source.endswith("'"):
        source = source[:-1]
    if not Path.exists(source):
        print(f"The file {source} doesn't exist.")
        sys.exit(1)
    elif destination == "auto":
        destination = os.path.splitext(source)[0] + "_translated.srt"  # noqa: PTH122

    json_extractor = JSONExtractor()
    subtitles_parts = process_subtitle_file(source)
    final_subtitles = []
    concat_subtitles = []
    for x, subtitle in enumerate(subtitles_parts):
        print(f"Addition of {subtitle.index} to keep context for better translation.")
        concat_subtitles.append(subtitle)
        if(len(concat_subtitles)>=MAX_CONCAT_SUBTITLES or x == len(subtitles_parts)-1):
            sub_texts = [sub.text for sub in concat_subtitles]
            prompt = json.dumps(sub_texts)
            print(f"Sending request for translation of {len(sub_texts)} items...")
            resp_txt = stream_request_llm_server(prompt)

            arrays = json_extractor.extract_json_arrays(resp_txt)
            if arrays and len(arrays)> 0:
                with Path.open(destination, 'a', encoding='utf-8') as f_out:
                    for i, subtitle in enumerate(concat_subtitles):  # noqa: PLW2901
                        if i < len(arrays[0]):
                            translated_text = arrays[0][i]
                            subtitle.text = translated_text.replace(" ", " ")  # noqa: RUF001
                            final_subtitles.append(subtitle)
                            new_subtitle_part = f"{subtitle.index}\n{subtitle.start} --> {subtitle.end}\n{subtitle.text}\n\n"
                            f_out.write(new_subtitle_part)
                print(f"Translation process terminated. The result is written into the file {destination}")
            else:
                print("No arrays found in the response")
            concat_subtitles = []

    if __name__ == "__main__":
        main()
