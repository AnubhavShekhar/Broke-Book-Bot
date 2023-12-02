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
            logging.info(f"Current pointer (START) : {self.pointer}")
            self.reply_text = self.get_formatted_text(uid)
            self.download_links = self.libgen.resolve_download_links(
                self.records[uid][0])
            return self.reply_text, self.download_links, self.pointer

        elif flag == -1:
            self.pointer -= 1
            logging.info(f"Current pointer : {self.pointer}")

            if self.pointer >= 0:
                self.reply_text = self.get_formatted_text(uid)
                self.download_links = self.libgen.resolve_download_links(
                    self.records[uid][self.pointer])
                return self.reply_text, self.download_links, self.pointer

            else:
                logging.info(
                    f"{self.get_records.__name__} | No more previous records.")
                self.reply_text = "No more previous records!"
                self.download_links = None
                return self.reply_text, self.download_links, self.pointer

        elif flag == 1:
            self.pointer += 1
            logging.info(f"Current pointer : {self.pointer}")

            if self.pointer <= len(self.records[uid])-1:
                self.reply_text = self.get_formatted_text(uid)
                self.download_links = self.libgen.resolve_download_links(
                    self.records[uid][self.pointer])
                return self.reply_text, self.download_links, self.pointer

            else:
                logging.info(f"{self.get_records.__name__} | No more records!")
                self.reply_text = "No more next records!"
                self.download_links = None
                return self.reply_text, self.download_links, self.pointer
        else:
            logging.warning("Invalid flag!")

    def get_formatted_text(self, uid: str) -> str:
        """
        Get the formatted text 
        """
        title = self.records[uid][self.pointer]['Title']
        author = self.records[uid][self.pointer]['Author']
        year = self.records[uid][self.pointer]['Year']
        ext = self.records[uid][self.pointer]['Extension']

        formatted_text = f"*RESULTS [{self.pointer+1}/{len(self.records[uid])}]*\n➖➖➖➖➖➖\n*Title*: _{title}_"

        if author:
            formatted_text += f"\n\n*Author* : _{author}_"
        if year:
            formatted_text += f"\n*Year* : _{year}_"
        if ext:
            formatted_text += f"\n*Extension* : _{ext}_"

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
