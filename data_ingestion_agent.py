from multiprocessing import Pool
import os
from traceback import format_exc
from typing import List
from logger import get_logger
from utils import KnowledgeBaseCollection
from langchain_docling import DoclingLoader
from docling.chunking import HybridChunker
from langchain_unstructured import UnstructuredLoader
from langchain_docling.loader import ExportType
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

IGNORE_FILE_EXTENSIONS = [".DS_Store"]

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
        self.logger.info(f"Ingesting data to {self.knowledge_base_collection} collection.")
        file_paths = self.get_files()
        self.logger.info(f"Files: {file_paths}")

        if not file_paths:
            self.logger.warning("No files found for processing.")
            return

        successful_docs: list[Document] = [] # List of successfully processed documents
        failed_files: list[tuple[str, str]] = [] # List of files that failed to process

        # use parallel processing to chunk the files
        with Pool(processes=min(os.cpu_count(), 4)) as pool:  # Limits to CPU cores or 4 max
            results = pool.map(DataIngestionAgent.process_file_safe, file_paths)
            for file_path, docs, error in results:
                if error:
                    failed_files.append((file_path, str(error)))
                    self.logger.error(f"Failed to process {file_path}: {error}.")
                else:
                    successful_docs.extend(docs)

        # chunk the documents
        if successful_docs:
            self.incrementally_store_docs(successful_docs, collection_name=self.knowledge_base_collection, folder_path="openworkspace-o1-vecs")
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
            if file.endswith(tuple(IGNORE_FILE_EXTENSIONS)):
                continue
            file_paths.append(os.path.join(folder_path, file))
        return file_paths

    def chunk_docs(self, docs: list[Document]) -> List[Document]:
        """
        Chunk the documents into smaller chunks
        """
        splitter = RecursiveCharacterTextSplitter(chunk_size=200)
        chunks = splitter.split_documents(docs)
        return chunks

    def incrementally_store_docs(self, docs: list[Document], collection_name: str, folder_path: str):
        """
        Incrementally store the documents into the knowledge base collection vector store
        """
        embeddings = OpenAIEmbeddings(model="text-embedding-3-large", dimensions=1536)
        FAISS_INDEX_NAME = os.path.join(folder_path, f"faiss_index_{collection_name}")
        # Check if the index already exists
        if os.path.exists(FAISS_INDEX_NAME):
            self.logger.info(f"Loading existing FAISS index from {FAISS_INDEX_NAME}")
            # Load the existing FAISS index
            vector_store = FAISS.load_local(FAISS_INDEX_NAME, embeddings, allow_dangerous_deserialization=True)

            self.logger.info(f"Adding documents to the existing index.")
            # Add the documents to the existing index
            vector_store.add_documents(docs)

            # Save the FAISS index to disk
            FAISS.save_local(vector_store, FAISS_INDEX_NAME)
        else:
            self.logger.info(f"Creating a new FAISS index.")
            # Create a FAISS index from the text documents
            vector_store = FAISS.from_documents(docs, embeddings)

            # Save the FAISS index to disk
            FAISS.save_local(vector_store, FAISS_INDEX_NAME)
