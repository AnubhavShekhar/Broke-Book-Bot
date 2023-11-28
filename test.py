from libgen_api import LibgenSearch
from icecream import ic


s = LibgenSearch()
results = s.search_title("Pride and Prejudice")
# ic(results)
# for result in results:
#     download_links = s.resolve_download_links(result)
#     if result == results[6]:
#         break
# print(download_links)
# download_link = download_links["GET"]
# print(download_link)
# filtered_search_results = []

# for result in results:
#     formatting = f"Title: {result['Title']}\nAuthor : {result['Author']}\nYear: {result['Year']}\nExtension: {result['Extension']}\nDirect Download Links:\nGET: {download_links["GET"]}\nCloudflare: {download_links['Cloudflare']}\nIPFS.io: {download_links["IPFS.io"]}\n{"-"*20}"
#     filtered_search_results.append(message)

# reply = "\n".join(filtered_search_results)
# print(reply)

filtered_search_results = []

for result in results:
    download_links = s.resolve_download_links(result)
    formatting = f"Title: {result['Title']}\nAuthor : {result['Author']}\nYear: {result['Year']}\nExtension: {result['Extension']}\nDirect Download Links:\nGET: {download_links["GET"]}\nCloudflare: {download_links['Cloudflare']}\nIPFS.io: {download_links["IPFS.io"]}\n{"-"*20}"
    filtered_search_results.append(formatting)
    if result == results[6]:
        break

for element in filtered_search_results:
    print(element)


GET: {download_links["GET"]}\n
Cloudflare: {download_links['Cloudflare']}\n
IPFS: {download_links["IPFS.io"]}\n{"-"*20}