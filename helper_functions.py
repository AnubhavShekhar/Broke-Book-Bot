from libgen_api import LibgenSearch
import logging

class Records:
    def __init__(self, query : str):
        self.query = query
        self.libgen = LibgenSearch()
        self.records = []
        self.formatted_records = []
        self.download_links = []
        self.reply_text = ""
        self.pointer = 0
    
    def initialize_records(self):
        self.records = self.libgen.search_title(self.query)
        logging.info("Records initialized")
        logging.info(self.records)

    def get_records(self,flag):
        if flag == 0:
            self.reply_text = f"""
Title: {self.records[0]['Title']}\n
Author : {self.records[0]['Author']}\n
Year: {self.records[0]['Year']}\n
Extension: {self.records[0]['Extension']}\n
Direct Download Links:\n
"""
            self.download_links = self.libgen.resolve_download_links(self.records[0])
            self.pointer += 1
            return self.reply_text, self.download_links
        
        elif flag == -1:
            self.pointer -= 1
            if self.pointer > 0 :
                self.reply_text = f"""
Title: {self.records[self.pointer]['Title']}\n
Author : {self.records[self.pointer]['Author']}\n
Year: {self.records[self.pointer]['Year']}\n
Extension: {self.records[self.pointer]['Extension']}\n
Direct Download Links:\n
"""
                self.download_links = self.libgen.resolve_download_links(self.records[self.pointer])
                return self.reply_text, self.download_links
            else:
                self.reply_text = "No more previous records!"
        
        elif flag == 1:
            self.pointer += 1
            if self.pointer < len(self.records):
                self.reply_text = f"""
Title: {self.records[self.pointer]['Title']}\n
Author : {self.records[self.pointer]['Author']}\n
Year: {self.records[self.pointer]['Year']}\n
Extension: {self.records[self.pointer]['Extension']}\n
Direct Download Links:\n
"""
                self.download_links = self.libgen.resolve_download_links(self.records[self.pointer])
                return self.reply_text, self.download_links
            else:
                self.reply_text = "No more next records!"
    
    def reset(self):
        self.pointer = 0
        logging.info("Pointer reset!")
        logging.info(self.pointer)
        self.records.clear()
        logging.info("Records cleared!")
        logging.info(self.records)
        self.download_links.clear()
        logging.info("Download links cleared!")
        logging.info(self.download_links)


