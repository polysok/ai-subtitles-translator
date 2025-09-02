import json
import re


class JSONExtractor:
    """Extract JSON from string."""

    def __init__(self) -> None:
        # Regex patterns to match JSON structures
        self.json_patterns = [
            # JSON between triple backticks with "json"
            r'```json\s*(.*?)\s*```',
            # JSON between triple backticks without "json"
            r'```\s*([\[\{].*?[\]\}])\s*```',
            # Simple JSON beginning by [ or {
            r'(\[.*?\]|\{.*?\})',
            # Multi JSON lines
            r'(\[[\s\S]*?\]|\{[\s\S]*?\})',
        ]

    def extract_json_arrays(self, text: str) ->list:
        """Extract all json array from LLM response.

        Args:
            text (str): text from LLM response

        Returns:
            return found json arrays as list of lists
        """
        json_arrays = []

        for pattern in self.json_patterns:
            matches = re.finditer(pattern, text, re.DOTALL | re.IGNORECASE)

            for match in matches:
                json_str = match.group(1) if len(match.groups()) > 0 else match.group(0)

                try:
                    json_str = self._clean_json_string(json_str)
                    parsed_json = json.loads(json_str)

                    # Chekc if it's a list
                    if isinstance(parsed_json, list):
                        json_arrays.append(parsed_json)
                    # Si c'est un objet contenant des tableaux
                    elif isinstance(parsed_json, dict):
                        for _, value in parsed_json.items():
                            if isinstance(value, list):
                                json_arrays.append(value)

                except json.JSONDecodeError:
                    # Try to clean and parse again
                    cleaned_json = self._clean_json_string(json_str)
                    try:
                        parsed_json = json.loads(cleaned_json)
                        if isinstance(parsed_json, list):
                            json_arrays.append(parsed_json)
                        elif isinstance(parsed_json, dict):
                            for _, value in parsed_json.items():
                                if isinstance(value, list):
                                    json_arrays.append(value)
                    except json.JSONDecodeError:
                        continue

        return json_arrays

    def _clean_json_string(self, json_str: str) -> str:
        """Clean json string to fix common errors.

        Args:
            json_str (str): JSON string to clean

        Returns:
            str: Cleaned JSON string
        """
        # Trim whitespace
        json_str = json_str.strip()

        # Clean leading/trailing non-JSON characters
        json_str = re.sub(r'^[^[\{]*', '', json_str)
        json_str = re.sub(r'[^\]\}]*$', '', json_str)

        # Fix single quotes to double quotes
        json_str = re.sub(r"'([^']*)':", r'"\1":', json_str)
        json_str = re.sub(r":\s*'([^']*)'", r': "\1"', json_str)

        # Delete trailling commas
        return re.sub(r',\s*([}\]])', r'\1', json_str)


