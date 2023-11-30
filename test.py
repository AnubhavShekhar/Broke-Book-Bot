from libgen_api import LibgenSearch
from icecream import ic


s = LibgenSearch()
results = s.search_title("Pride and Prejudice")
download_links = s.resolve_download_links(results)
print(download_links)