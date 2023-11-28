from libgen_api import LibgenSearch

class Records:
    def __init__(self, query : str):
        self.query = query
        self.libgen = LibgenSearch()
        self.records = []
        self.formatted_records = []
        self.download_links = []
        self.reply = ""
    
    def get_records(self):
        self.records = self.libgen.search_title(self.query)
        for record in self.records:
            self.download_links = self.libgen.resolve_download_links(record)
            formatting = f"""
Title: {record['Title']}\n
Author : {record['Author']}\n
Year: {record['Year']}\n
Extension: {record['Extension']}\n
Direct Download Links:\n
"""
            self.formatted_records.append(formatting)
            if record == self.records[0]:
                break
        self.reply = "\n".join(self.formatted_records)