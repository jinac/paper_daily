import feedparser
import datetime
from datetime import timedelta, timezone
import time
from config_loader import load_config

def dedup(paper_objs):
    seen = set()
    unique_papers = []
    for obj in paper_objs:
        if obj['id'] not in seen:
            unique_papers.append(obj)
            seen.add(obj['id'])
    return(unique_papers)

class RSSFetcher:
    def __init__(self, config):
        self.config = config
        self.rss_urls = config.get("rss_urls", [])
        self.time_frame_hours = config.get("time_frame_hours", 24)

    def fetch_recent_papers(self):
        """Fetches papers from arXiv RSS feeds."""
        now_utc = datetime.datetime.now(timezone.utc)
        start_time_utc = now_utc - timedelta(hours=self.time_frame_hours)
        
        papers = []
        
        for url in self.rss_urls:
            print(f"Fetching RSS feed: {url}")
            try:
                feed = feedparser.parse(url)
                count = 0
                for entry in feed.entries:
                    # Parse publishing date from entry
                    published_dt = datetime.datetime(*entry.published_parsed[:6], tzinfo=datetime.timezone.utc)
                    
                    # Check if entry is within time frame and is a new announcement
                    if published_dt >= start_time_utc and getattr(entry, 'arxiv_announce_type', None) == "new":
                        papers.append({
                            "title": entry.title,
                            "link": entry.link,
                            "abstract": entry.summary,
                            "published": published_dt,
                            "primary_category": url.split('/')[-1], # Heuristic
                            "id": entry.get('id', entry.link)
                        })
                        count += 1
                print(f"Found {count} new papers in {url}")
            except Exception as e:
                print(f"Error during RSS fetch for {url}: {e}")
            
            time.sleep(1) # Respect rate limits
        
        papers = dedup(papers)
        return papers

if __name__ == "__main__":
    # Test the RSS fetcher
    try:
        config = load_config()
        fetcher = RSSFetcher(config)
        recent_papers = fetcher.fetch_recent_papers()
        print(f"Successfully found {len(recent_papers)} papers matching criteria.")
        if recent_papers:
            print(f"Sample: {recent_papers[0]['title']}")
    except Exception as e:
        print(f"Failed to run fetcher test: {e}")

