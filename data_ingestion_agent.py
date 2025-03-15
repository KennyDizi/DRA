from multiprocessing import Pool
import os
from traceback import format_exc
from logger import get_logger
from utils import KnowledgeBaseCollection
from langchain_docling import DoclingLoader
from docling.chunking import HybridChunker
from langchain_unstructured import UnstructuredLoader
from langchain_docling.loader import ExportType

class DataIngestionAgent:
    """
    This class is used to ingest data into the knowledge base collection with vectorization.
    """
    def __init__(self, knowledge_base_collection: str = KnowledgeBaseCollection.GENERIC):
        self.knowledge_base_collection = knowledge_base_collection
        self.logger = get_logger()

    @staticmethod
    def process_file(file_path: str):
        docling_supported_file_extensions = [".pdf", ".docx", ".xlsx", ".pptx", ".png", ".jpeg", ".tiff", ".bmp"]
        if file_path.endswith(tuple(docling_supported_file_extensions)):
            return DataIngestionAgent.process_file_with_docling_loader(file_path)
        else:
            return DataIngestionAgent.process_file_with_unstructured_loader(file_path)

    @staticmethod
    def process_file_with_docling_loader(file_path: str):
        """Process a single file using DoclingLoader"""
        chunker = HybridChunker()
        loader = DoclingLoader(file_path=file_path, chunker=chunker, export_type=ExportType.MARKDOWN)
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
        self.logger.info(f"Ingesting data to {self.knowledge_base_collection} collection.")
        file_paths = self.get_files()
        self.logger.info(f"Files: {file_paths}")

        if not file_paths:
            self.logger.warning("No files found for processing.")
            return

        successful_docs = []
        failed_files = []

        # use parallel processing to chunk the files
        with Pool(processes=min(os.cpu_count(), 4)) as pool:  # Limits to CPU cores or 4 max
            results = pool.map(DataIngestionAgent.process_file_safe, file_paths)
            for file_path, docs, error in results:
                if error:
                    failed_files.append((file_path, str(error)))
                    self.logger.error(f"Failed to process {file_path}: {error}.")
                else:
                    successful_docs.extend(docs)

        self.logger.info(f"Successfully processed docs: {len(successful_docs)}.")

        if failed_files:
            self.logger.error("Failed to process these files:")
            for file_path, error in failed_files:
                self.logger.error(f"\n- {file_path} ({error}).")

    def get_files(self):
        """
        Get all the files in the folder path
        """
        # folder_path is a combination of the knowledge base collection with the root directory
        folder_path = os.path.join("openworkspace-o1-docs", self.knowledge_base_collection)
        file_paths =[]
        for file in os.listdir(folder_path):
            file_paths.append(os.path.join(folder_path, file))
        return file_paths

    def chunk_files(self, file_paths: list[str]):
        """
        Chunk the files into smaller chunks
        """
        pass
