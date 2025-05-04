from abc import ABC, abstractmethod
from google.adk.sessions import Session
from google.adk.memory.base_memory_service import SearchMemoryResponse

class GraphMemoryService(ABC):
    @abstractmethod
    def add_memory(self, session: Session):
        pass

    @abstractmethod
    def search_memory(self, *, app_name: str, user_id: str, query: str) -> SearchMemoryResponse:
        pass
