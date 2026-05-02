import argparse
import json
import sys
from config_loader import load_config
from fetcher import ArxivFetcher
from analyzer import PaperAnalyzer
from generator import PaperGenerator

def main():
    parser = argparse.ArgumentParser(description="ArXiv Researcher Agent: Fetch, Filter, and Generate Research Digests.")
    parser.add_argument(
        "--config", "-c",
        type=str, 
        default="config.json", 
        help="Path to the configuration JSON file (default: config.json)."
    )
    parser.add_argument(
        "--no-filter", 
        action="store_true", 
        help="Skip the filtering stage and generate a digest from all fetched papers."
    )
    args = parser.parse_args()

    try:
        # 1. Load Configuration
        print(f"Loading configuration from {args.config}...")
        config = load_config(args.config)

        # 2. Initialize Components
        fetcher = ArxivFetcher(config)
        generator = PaperGenerator(config)
        analyzer = PaperAnalyzer(config)

        # 3. Step 1: Fetching
        print("Fetching recent papers from arXiv...")
        papers = fetcher.fetch_recent_papers()
        print(f"Retrieved {len(papers)} papers.")

        if not papers:
            print("No papers found to process.")
            return

        # 4. Step 2: Filtering (Conditional)
        if args.no_filter:
            print("Skipping filtering stage as requested.")
            filtered_papers = papers
        else:
            print("Applying intelligent filtering (Keyword + LLM)...")
            filtered_papers = analyzer.filter_papers(papers)
            print(f"Filtering complete: {len(papers)} papers reduced to {len(filtered_papers)} relevant papers.")

        # 5. Step 3: Generating
        print("Generating research digest...")
        generator.generate_digest(filtered_papers)
        print("Process completed successfully.")

    except Exception as e:
        print(f"CRITICAL ERROR: {argparse.ArgumentTypeError if 'argparse' in str(type(e)) else e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

