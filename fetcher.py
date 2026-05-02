import arxiv
import datetime
from datetime import timedelta, timezone
import time
from config_loader import load_config

class ArxivFetcher:
    def __init__(self, config):
        self.config = config
        self.search_params = config.get("search_params", {})
        self.time_frame_hours = self.search_params.get("time_frame_hours", 24)
        self.subject_filters = self.search_params.get("subject_filters", [])

    def _format_arxiv_date(self, dt):
        """Formats a datetime object into the arXiv required format: YYYMMDDHHmm."""
        return dt.strftime("%Y%m%d%H%M")

    def fetch_recent_papers(self):
        """Fetches papers from arXiv using an optimized API query."""
        # Build Date Range Query (submittedDate:[START+TO+END])
        now_utc = datetime.datetime.now(timezone.utc)
        start_time_utc = now_utc - timedelta(hours=self.time_frame_hours)
        start_str = self._format_arxiv_date(start_time_utc)
        end_str = self._format_arxiv_date(now_utc)
        date_query = f"submittedDate:[{start_str} TO {end_str}]"
        
        client = arxiv.Client()

        papers = []
        # Iterate through subjects
        for subj in self.subject_filters:

            subject_query = f"cat:{subj}"
            full_query = f"{subject_query} AND {date_query}"

            print(f"Executing arXiv search with query: {full_query}")

            search = arxiv.Search(
                query=full_query,
                max_results=500,
                sort_by=arxiv.SortCriterion.SubmittedDate
            )

            try:
                count = 0
                for result in client.results(search):
                    papers.append({
                        "title": result.title,
                        "link": result.entry_id,
                        "abstract": result.summary,
                        "published": result.published,
                        "primary_category": result.primary_category
                    })
                    count += 1
                print(f"{subj}: {count}")
            except Exception as e:
                print(f"Error during arXiv search: {e}")

            time.sleep(3) # Time sleep to respect rate limits
            
        return papers

if __name__ == "__main__":
    # Test the optimized fetcher
    try:
        config = load_config()
        fetcher = ArxivFetcher(config)
        recent_papers = fetcher.fetch_recent_papers()
        print(f"Successfully found {len(recent_papers)} papers matching criteria.")
        if recent_papers:
            print(f"Sample: {recent_papers[0]['title']} [{recent_papers[0]['primary_category']}]")
    except Exception as e:
        print(f"Failed to run fetcher test: {e}")
