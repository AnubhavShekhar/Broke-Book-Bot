from libgen_api import LibgenSearch
import logging


class Records:
    def __init__(self, query: str) -> None:
        """
        Initialize the variables
        """

        self.query = query
        self.libgen = LibgenSearch()
        self.record = []
        self.formatted_records = []
        self.download_links = []
        self.reply_text = ""
        self.pointer = 0

    def initialize_records(self) -> None:
        """
        Initialize records
        Creates a list of dictionaries of the query results
        """

        self.record = self.libgen.search_title(self.query)
        logging.info(f"{self.initialize_records.__name__} | Records initialized")
        logging.info(self.record)

    def get_records(self, flag: int) -> [str, list]:
        """
        Get initial records when flag == 0
        Get next record when flag == 1
        Get previous record when flag == -1
        """

        if flag == 0:
            self.reply_text = self.get_formatted_text(0)
            self.download_links = self.libgen.resolve_download_links(
                self.record[0])
            return self.reply_text, self.download_links

        elif flag == -1:
            self.pointer -= 1

            if self.pointer > 0:
                self.reply_text = self.get_formatted_text(1)
                self.download_links = self.libgen.resolve_download_links(
                    self.record[self.pointer])
                return self.reply_text, self.download_links

            else:
                logging.info(f"{self.get_records.__name__} | No more previous records.")
                self.reply_text = "No more previous records!"
                self.download_links = None
                return self.reply_text, self.download_links

        elif flag == 1:
            self.pointer += 1

            if self.pointer < len(self.record):
                self.reply_text = self.get_formatted_text(1)
                self.download_links = self.libgen.resolve_download_links(
                    self.record[self.pointer])
                return self.reply_text, self.download_links

            else:
                logging.info(f"{self.get_records.__name__} | No more records!")
                self.reply_text = "No more next records!"
                self.download_links = None
                return self.reply_text, self.download_links
        else:
            logging.warning("Invalid flag!")

    def get_formatted_text(self, flag: int) -> str: 
        """
        Get the formatted text 
        """

        formatted_text = ""
        if flag == 0:
            formatted_text = f"""
Title: {self.record[0]['Title']}\n
Author : {self.record[0]['Author']}\n
Year: {self.record[0]['Year']}\n
Extension: {self.record[0]['Extension']}\n
Direct Download Links:\n
"""
            return formatted_text
        else:
            formatted_text = f"""
Title: {self.record[self.pointer]['Title']}\n
Author : {self.record[self.pointer]['Author']}\n
Year: {self.record[self.pointer]['Year']}\n
Extension: {self.record[self.pointer]['Extension']}\n
Direct Download Links:\n
"""
            return formatted_text

    def reset(self) -> None:
        """
        Resets the pointer and clears records and download links
        """

        self.pointer = 0
        logging.info(f"{self.reset.__name__} | Pointer reset! | {self.pointer}")

        self.record.clear()
        logging.info(f"{self.reset.__name__} | Records cleared! | {self.record}")

        self.download_links.clear()
        logging.info(f"{self.reset.__name__} | Download links cleared! | {self.download_links}")

