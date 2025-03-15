from multiprocessing import Pool
import os
from logger import get_logger
from utils import KnowledgeBaseCollection
from langchain_docling import DoclingLoader
from docling.chunking import HybridChunker
from langchain_unstructured import UnstructuredLoader

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
        loader = DoclingLoader(file_path=file_path, chunker=chunker)
        docs = loader.load()
        return docs

    @staticmethod
    def process_file_with_unstructured_loader(file_path: str):
        """Process a single file using UnstructuredLoader"""
        loader = UnstructuredLoader(file_path=file_path)
        docs = loader.load()
        return docs

    def ingest_data(self):
        self.logger.info(f"Ingesting data to {self.knowledge_base_collection} collection.")
        file_paths = self.get_files()
        self.logger.info(f"Files: {file_paths}")

        # use parallel processing to chunk the files
        with Pool(processes=len(file_paths)) as pool:
            docs = pool.map(DataIngestionAgent.process_file, file_paths)
            self.logger.info(f"Docs: {docs}")
        pass

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
