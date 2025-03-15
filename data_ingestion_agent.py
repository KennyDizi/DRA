import os
from logger import get_logger
from utils import KnowledgeBaseCollection
from langchain_docling import DoclingLoader
from docling.chunking import HybridChunker

class DataIngestionAgent:
    """
    This class is used to ingest data into the knowledge base collection with vectorization.
    """
    def __init__(self, knowledge_base_collection: str = KnowledgeBaseCollection.GENERIC):
        self.knowledge_base_collection = knowledge_base_collection
        self.logger = get_logger()

    def ingest_data(self):
        self.logger.info(f"Ingesting data to {self.knowledge_base_collection} collection.")
        file_paths = self.get_files()
        self.logger.info(f"Files: {file_paths}")
        chunker = HybridChunker()
        loader = DoclingLoader(file_path="data/test.pdf", chunker=chunker)
        docs = loader.load()
        pass

    def get_files(self):
        """
        Get all the files in the folder path
        """
        # folder_path is a combination of the knowledge base collection with the root directory
        folder_path = os.path.join(os.path.dirname(__file__), "openworkspace-o1-docs", self.knowledge_base_collection)
        file_paths =[]
        for file in os.listdir(folder_path):
            file_paths.append(os.path.join(folder_path, file))
        return file_paths

    def chunk_files(self, file_paths: list[str]):
        """
        Chunk the files into smaller chunks
        """
        pass
