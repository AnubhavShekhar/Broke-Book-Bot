from libgen_api import LibgenSearch
import logging
import json


class Records:

    def __init__(self, query: str, record_pool) -> None:
        """
        Initialize the variables
        """
        self.query = query
        self.libgen = LibgenSearch()
        self.records = record_pool
        self.formatted_records = []
        self.download_links = []
        self.reply_text = ""
        self.pointer = 0

    def initialize_records(self, uid: str) -> None:
        """
        Initialize records
        Creates a list of dictionaries of the query results
        """

        self.records[str(uid)] = self.libgen.search_title(self.query)
        logging.info(
            f"{self.initialize_records.__name__} | Records initialized")
        logging.info(json.dumps(self.records, indent=2))

    def get_records(self, flag: int, uid: str) -> [str, list]:
        """
        Get initial records when flag == 0
        Get next record when flag == 1
        Get previous record when flag == -1
        """

        if flag == 0:
            self.reply_text = self.get_formatted_text(0, uid)
            self.download_links = self.libgen.resolve_download_links(
                self.records[uid][0])
            return self.reply_text, self.download_links

        elif flag == -1:
            self.pointer -= 1

            if self.pointer > 0:
                self.reply_text = self.get_formatted_text(1, uid)
                self.download_links = self.libgen.resolve_download_links(
                    self.records[uid][self.pointer])
                return self.reply_text, self.download_links

            else:
                logging.info(
                    f"{self.get_records.__name__} | No more previous records.")
                self.reply_text = "No more previous records!"
                self.download_links = None
                return self.reply_text, self.download_links

        elif flag == 1:
            self.pointer += 1

            if self.pointer < len(self.records[uid]):
                self.reply_text = self.get_formatted_text(1, uid)
                self.download_links = self.libgen.resolve_download_links(
                    self.records[uid][self.pointer])
                return self.reply_text, self.download_links

            else:
                logging.info(f"{self.get_records.__name__} | No more records!")
                self.reply_text = "No more next records!"
                self.download_links = None
                return self.reply_text, self.download_links
        else:
            logging.warning("Invalid flag!")

    def get_formatted_text(self, flag: int, uid: str) -> str:
        """
        Get the formatted text 
        """

        formatted_text = ""
        if flag == 0:
            formatted_text = f"""
Title: {self.records[uid][0]['Title']}\n
Author : {self.records[uid][0]['Author']}\n
Year: {self.records[uid][0]['Year']}\n
Extension: {self.records[uid][0]['Extension']}\n
Direct Download Links:\n
"""
            return formatted_text
        else:
            formatted_text = f"""
Title: {self.records[uid][self.pointer]['Title']}\n
Author : {self.records[uid][self.pointer]['Author']}\n
Year: {self.records[uid][self.pointer]['Year']}\n
Extension: {self.records[uid][self.pointer]['Extension']}\n
Direct Download Links:\n
"""
            return formatted_text

    def reset(self, uid: str) -> None:
        """
        Resets the pointer and clears records and download links
        """

        self.pointer = 0
        logging.info(
            f"{self.reset.__name__} | Pointer reset! | {self.pointer}")

        self.records[uid] = []
        logging.info(
            f"{self.reset.__name__} | Records cleared! | {self.records[uid]}")

        self.download_links.clear()
        logging.info(
            f"{self.reset.__name__} | Download links cleared! | {self.download_links}")
