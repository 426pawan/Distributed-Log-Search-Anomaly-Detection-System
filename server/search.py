from whoosh.index import open_dir
from whoosh.qparser import QueryParser

INDEX_DIR = "indexdir"
ix = open_dir(INDEX_DIR)

def search_logs(keyword):
    with ix.searcher() as searcher:
        query = QueryParser("message", ix.schema).parse(keyword)
        results = searcher.search(query, limit=20)
        for r in results:
            print(f"[{r['timestamp']}] {r['host']} {r['process']}: {r['message']}")

if __name__ == "__main__":
    keyword = input("Enter search keyword: ")
    search_logs(keyword)
