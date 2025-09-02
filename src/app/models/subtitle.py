class Subtitle:
    """Represents a subtitle with its temporal metadata."""

    def __init__(self, index:int, start:int, end:int, text:str) -> None:
        """Represents a subtitle with its temporal metadata.

        Args:
            index (int): Subtitle number
            start (str): Start timestamp in "HH:MM:SS,mmm" format
            end (str): End timestamp in "HH:MM:SS,mmm" format
            text (str): Subtitle text
        """
        self.index = index
        self.start = start
        self.end = end
        self.text = text.strip()

    def __str__(self) -> str:
        """Text representation of the subtitle."""
        return f"{self.index}\n{self.start} --> {self.end}\n{self.text}"

    def __repr__(self) -> str:
        """Representation for debugging."""
        return f"Subtitle(index={self.index}, start='{self.start}', end='{self.end}', text='{self.text[:30]}...')"
