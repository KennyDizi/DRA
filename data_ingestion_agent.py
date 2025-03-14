from .utils import KnowledgeBaseCollection

class DataIngestionAgent:
    def __init__(self, knowledge_base_collection: str):
        self.knowledge_base_collection = knowledge_base_collection if not None else KnowledgeBaseCollection.GENERIC

    def ingest_data(self, data: str):
        pass
