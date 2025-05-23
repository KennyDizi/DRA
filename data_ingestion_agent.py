import os
from multiprocessing import get_context
from traceback import format_exc
from logger import get_logger
from langchain_unstructured import UnstructuredLoader

IGNORE_FILE_EXTENSIONS = [".DS_Store"]
DOC_PATH = os.getenv("DOC_PATH") or "./my-docs"
ORIGINAL_DOCS_PATH = os.getenv("ORIGINAL_DOCS_PATH") or "./original-docs"

class DataIngestionAgent:
    """
    This class is used to ingest data into the knowledge base collection with vectorization.
    """
    def __init__(self):
        self.logger = get_logger()

    @staticmethod
    def process_file(file_path: str):
       return DataIngestionAgent.process_file_with_unstructured_loader(file_path)

    @staticmethod
    def process_file_with_unstructured_loader(file_path: str):
        """Process a single file using UnstructuredLoader"""
        api_key = os.getenv("UNSTRUCTURED_API_KEY") if os.getenv("UNSTRUCTURED_API_KEY") else None
        partition_via_api = True if api_key else False
        loader = UnstructuredLoader(file_path=file_path, partition_via_api=partition_via_api, api_key=api_key)
        docs = loader.load()
        return docs

    @staticmethod
    def process_file_safe(file_path: str):
        try:
            docs = DataIngestionAgent.process_file(file_path)
            return (file_path, docs, None)
        except Exception as e:
            return (file_path, None, f"{str(e)}\nTraceback:\n{format_exc()}")

    def ingest_data(self):
        self.logger.info("Ingesting data ...")
        file_paths = self.get_files(folder_name=ORIGINAL_DOCS_PATH)
        self.logger.info(f"Files: {file_paths}")

        if not file_paths:
            self.logger.warning("No files found for processing.")
            return


        failed_files: list[tuple[str, str]] = [] # List of files that failed to process

        # Check if folder my-docs exists, if not create it
        if not os.path.exists(DOC_PATH):
            os.makedirs(DOC_PATH)

        # use parallel processing to chunk the files
        with get_context('spawn').Pool(processes=min(os.cpu_count(), 4)) as pool:  # Using spawn context
            results = pool.map(DataIngestionAgent.process_file_safe, file_paths)
            pool.close()  # Explicit close
            pool.join()   # Explicit join
            for file_path, docs, error in results:
                self.logger.info(f"Processing {file_path} ...")
                if error:
                    failed_files.append((file_path, str(error)))
                    self.logger.error(f"Failed to process {file_path}: {error}.")
                else:
                    file_name = os.path.basename(file_path)
                    file_name_without_ext = os.path.splitext(file_name)[0]  # Get name without extension
                    combined_docs = ""
                    self.logger.info(f"File {file_name} has {len(docs)} chunks.")
                    for doc in docs:
                        combined_docs += f"{doc.page_content}\n"
                    with open(os.path.join(DOC_PATH, f"{file_name_without_ext}.md"), "w") as f:
                        f.write(combined_docs)
                    self.logger.info(f"New file has been saved to {DOC_PATH}/{file_name_without_ext}.md")

        if failed_files:
            self.logger.error("Failed to process these files:")
            for file_path, error in failed_files:
                self.logger.error(f"\n- {file_path} ({error}).")

    def get_files(self, folder_name: str):
        """
        Get all the files in the folder path
        """
        folder_path = os.path.join(folder_name)
        file_paths =[]
        for file in os.listdir(folder_path):
            if file.endswith(tuple(IGNORE_FILE_EXTENSIONS)):
                continue
            file_paths.append(os.path.join(folder_path, file))
        return file_paths

def main():
    data_ingestion_agent = DataIngestionAgent()
    data_ingestion_agent.ingest_data()

if __name__ == "__main__":
    main()