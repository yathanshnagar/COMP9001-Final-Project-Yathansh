from pathlib import Path

class Track:
    def __init__(self, filepath: Path):
        self.filepath = filepath

        # Song title (filename without extension)
        self.title = filepath.stem

        # Album and artist (assumes structure: /Artist/Album/Song.mp3)
        self.album = filepath.parent.name
        self.artist = filepath.parent.parent.name

        # Album folder path
        self.album_folder = filepath.parent

        # Look for cover image (jpg or png)
        self.cover_path = self._find_cover_image()

    def _find_cover_image(self) -> Path | None:
    # Returns a cover image path if any .jpg/.png with 'cover' in name is found.
        for file in self.album_folder.iterdir():
            if file.suffix.lower() in [".jpg", ".jpeg", ".png"] and "cover" in file.stem.lower():
                return file
        return None

    def has_cover(self) -> bool:
        """Return True if an album cover image is found."""
        return self.cover_path is not None

    def get_display_name(self) -> str:
        """Return a user-friendly string to display: 'Title by Artist [Album]'."""
        return f"{self.title} by {self.artist} [{self.album}]"

    def __repr__(self):
        return f"Track({self.get_display_name()})"
