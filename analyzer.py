class PaperAnalyzer:
    def __init__(self, config):
        self.config = config
        self.keywords = config.get("filtering", {}).get("keywords", [])
        self.llm_prompt = config.get("filtering", {}).get("llm_prompt", "")
        self.model = config.get("llm_settings", {}).get("model", "llama3")

    def keyword_filter(self, abstract):
        """Performs a fast keyword-based pass."""
        if not self.keywords:
            return True
        abstract_lower = abstract.lower()
        return any(kw.lower() in abstract_lower for kw in self.keywords)

    def filter_papers(self, papers):
        """Orchestrates the two-stage filtering process."""
        filtered_papers = []
        
        print(f"Filtering from {len(papers)} papers")
        for paper in papers:
            # Stage 1: Keyword Filter
            if self.keyword_filter(paper.get("abstract", "")):
                filtered_papers.append(paper)
                    
        return filtered_papers

if __name__ == "__main__":
    # Quick test logic
    import json
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
        
        analyzer = PaperAnalyzer(config)
        test_papers = [
            {
                "title": "Test Paper 1",
                "append_abstract": "This paper discusses transformers and agents in AI."
            },
            {
                "title": "Test Paper 2",
                "append_abstract": "This is a completely unrelated paper about biology."
            }
        ]
        
        # Adjust test papers to match the expected structure if needed
        test_papers_fixed = []
        for p in test_papers:
            test_papers_fixed.append({
                "title": p["title"],
                "abstract": p.pop("append_abstract")
            })

        print("Running analyzer test...")
        results = analyzer.filter_papers(test_papers_fixed)
        print(f"Passed: {len(results)} papers")
    except Exception as e:
        print(f"Test failed: {e}")

