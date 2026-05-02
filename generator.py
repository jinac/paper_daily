import datetime
import os

class PaperGenerator:
    def __init__(self, config):
        self.config = config
        self.output_path = config.get("output", {}).get("file_path", "RESEARCH_DIGEST.md")

    def _format_paper(self, paper):
        """Formats a single paper dictionary into a Markdown block."""
        title = paper.get("title", "Unknown Title")
        link = paper.get("link", "#")
        abstract = paper.get("abstract", "No abstract available.")
        pub_date = paper.get("published", datetime.datetime.now())
        category = paper.get("primary_category", "N/A")

        # Format date as YYYY-MM-DD
        date_str = pub_date.strftime("%Y-%m-%d") if isinstance(pub_date, datetime.datetime) else str(pub_date)

        return (
            f"### [{title}]({link})\n"
            f"*Published: {date_str} | Category: {category}*\n\n"
            f"{abstract}\n"
            f"\n---\n"
        )

    def generate_digest(self, papers):
        """Generates the full Markdown digest and writes it to the output path."""
        if not papers:
            message = f"# ArXiv Research Digest - {datetime.datetime.now().strftime('%Y-%m-%d')}\n\n**No new papers found matching your criteria.**"
            self._write_to_file(message)
            print("No papers to generate. Created digest with 'no papers' message.")
            return

        header = f"# ArXiv Research Digest - {datetime.datetime.now().strftime('%Y-%m-%d')}\n\n"
        
        paper_blocks = [self._format_paper(p) for p in papers]
        content = header + "\n".join(paper_blocks)
        
        self._write_to_file(content)
        print(f"Successfully generated digest at: {self.output_path}")

    def _write_to_file(self, content):
        """Writes the content to the specified file path, creating directories if needed."""
        directory = os.path.dirname(self.output_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
            
        with open(self.output_path, "w", encoding="utf-8") as f:
            f.write(content)

if __name__ == "__main__":
    # Quick test logic
    import json

    try:
        with open("config.json", "r") as f:
            import json
            config = json.load(f)
        
        generator = PaperGenerator(config)
        
        test_papers = [
            {
                "title": "Test Paper 1",
                "link": "https://arxiv.org/abs/2405.00001",
                "abstract": "This is a test abstract for paper 1.",
                "published": datetime.datetime(2024, 5, 1),
                "primary_category": "cs.AI"
            },
            {
                "title": "Test Paper 2",
                "link": "https://arxiv.org/abs/2405.00002",
                "abstract": "This is a test abstract for paper 2.",
                "published": datetime.datetime(2024, 5, 2),
                "primary_category": "cs.CV"
            }
        ]
        
        print("Running generator test...")
        generator.generate_digest(test_papers)
        
        # Check if file was created
        if os.path.exists(config.get("output", {}).get("file_path", "RESEARCH_DIGEST.md")):
            print("Test passed: File created.")
        else:
            print("Test failed: File not created.")
            
    except Exception as e:
        print(f"Test failed: {e}")
