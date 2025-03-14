from logger import get_logger
from utils import KnowledgeBaseCollection

class DataIngestionAgent:
    def __init__(self, knowledge_base_collection: str = KnowledgeBaseCollection.GENERIC):
        self.knowledge_base_collection = knowledge_base_collection
        self.logger = get_logger()

    def ingest_data(self):
        self.logger.info(f"Ingesting data to {self.knowledge_base_collection} collection.")
        pass
