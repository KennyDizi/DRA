from multiprocessing import Pool
import os
from traceback import format_exc
from logger import get_logger
from langchain_docling import DoclingLoader
from docling.chunking import HybridChunker
from langchain_unstructured import UnstructuredLoader
from langchain_docling.loader import ExportType

IGNORE_FILE_EXTENSIONS = [".DS_Store"]

class DataIngestionAgent:
    """
    This class is used to ingest data into the knowledge base collection with vectorization.
    """
    def __init__(self):
        self.logger = get_logger()

    @staticmethod
    def process_file(file_path: str):
        docling_supported_file_extensions = [".png", ".jpeg", ".tiff", ".bmp"]
        if file_path.lower().endswith(tuple(docling_supported_file_extensions)):
            return DataIngestionAgent.process_file_with_docling_loader(file_path)
        else:
            return DataIngestionAgent.process_file_with_unstructured_loader(file_path)

    @staticmethod
    def process_file_with_docling_loader(file_path: str):
        """Process a single file using DoclingLoader"""
        chunker = HybridChunker()
        loader = DoclingLoader(file_path=file_path, chunker=chunker, export_type=ExportType.DOC_CHUNKS)
        docs = loader.load()
        return docs

    @staticmethod
    def process_file_with_unstructured_loader(file_path: str):
        """Process a single file using UnstructuredLoader"""
        loader = UnstructuredLoader(file_path=file_path)
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
        self.logger.info(f"Ingesting data ...")
        file_paths = self.get_files(folder_name="original-docs")
        self.logger.info(f"Files: {file_paths}")

        if not file_paths:
            self.logger.warning("No files found for processing.")
            return


        failed_files: list[tuple[str, str]] = [] # List of files that failed to process

        # use parallel processing to chunk the files
        with Pool(processes=min(os.cpu_count(), 4)) as pool:  # Limits to CPU cores or 4 max
            results = pool.map(DataIngestionAgent.process_file_safe, file_paths)
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
                    with open(os.path.join("my-docs", f"{file_name_without_ext}.md"), "w") as f:
                        f.write(combined_docs)

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
