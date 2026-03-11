import os
import csv
import json

# writing text and CSV processing logic...
class FileAgent:
    """
    Agent for reading and writing files into standard formats (txt, csv).
    Includes a local search capability for finding strings within files.
    """

    def __init__(self, root_dir: str = "."):
        # setting base directory for search and files...
        self.root_dir = root_dir

    def read_text(self, filename: str) -> str:
        """Reads plain text content directly from a file."""
        # reading text file...
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return f"Error: File '{filename}' not found."

    def write_text(self, filename: str, content: str) -> bool:
        """Writes content to a file with basic status feedback."""
        # writing to text file...
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            return f"Error: {str(e)}"

    def read_csv(self, filename: str) -> list:
        """Reads CSV data and returns list of dictionaries for analysis."""
        # processing CSV files...
        try:
            with open(filename, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                return list(reader)
        except Exception as e:
            return {"error": str(e), "filename": filename}

    def write_csv(self, filename: str, data: list, headers: list = None) -> bool:
        """Writes structured data back to a CSV file."""
        # writing to CSV with headers...
        try:
            if not data:
                return "Empty data provided."
            # identifying keys if headers were not given...
            if headers is None:
                headers = data[0].keys()
            
            with open(filename, mode='w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
                writer.writerows(data)
            return True
        except Exception as e:
            return f"Error: {str(e)}"

    def local_search(self, search_term: str, extension: str = ".txt") -> list:
        """Iterates through files and returns matches (local search engine)."""
        # creating local search function...
        matches = []
        for filename in os.listdir(self.root_dir):
            if filename.endswith(extension):
                # adding basic search logic...
                content = self.read_text(filename)
                if search_term.lower() in content.lower():
                    matches.append(filename)
        return matches

# adding example file agent usage (internal check)...
if __name__ == "__main__":
    fa = FileAgent()
    print("File Agent Ready.")
    print("Checking local directory for search term 'test'...")
    # results = fa.local_search("test")
    # print(results)
