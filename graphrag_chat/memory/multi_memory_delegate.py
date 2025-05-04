from typing import List
from google.adk.sessions import Session
from google.adk.memory.base_memory_service import SearchMemoryResponse, MemoryResult
from .graph_memory_service import GraphMemoryService

class MultiMemoryDelegate(GraphMemoryService):
    def __init__(self, delegates: List[GraphMemoryService]):
        self.delegates = delegates

    def add_memory(self, session: Session):
        for delegate in self.delegates:
            delegate.add_memory(session)

    def search_memory(self, *, app_name: str, user_id: str, query: str) -> SearchMemoryResponse:
        combined_response = SearchMemoryResponse()
        seen_sessions = set()
        for delegate in self.delegates:
            response = delegate.search_memory(app_name=app_name, user_id=user_id, query=query)
            for memory in getattr(response, 'memories', []):
                key = (memory.session_id, id(memory))
                if key not in seen_sessions:
                    combined_response.memories.append(memory)
                    seen_sessions.add(key)
        return combined_response
