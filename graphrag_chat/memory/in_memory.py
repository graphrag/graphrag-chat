
from google.adk.events import Event
from google.adk.sessions import Session
# from google.adk.memory.base_memory_service import BaseMemoryService
from google.adk.memory.base_memory_service import MemoryResult
from google.adk.memory.base_memory_service import SearchMemoryResponse

from .graph_memory_service import GraphMemoryService

class InMemoryService(GraphMemoryService):
    """An in-memory service to be used as a tool. NOT based on the ADK BaseMemoryService.
    Singleton implementation.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(InMemoryService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'session_events'):
            self.session_events: dict[str, list[Event]] = {}
            """keys are app_name/user_id/session_id"""

    def add_memory(self, session: Session):
        key = f'{session.app_name}/{session.user_id}/{session.id}'
        self.session_events[key] = [
            event for event in session.events if event.content
        ]

    def search_memory(
        self, *, app_name: str, user_id: str, query: str
    ) -> SearchMemoryResponse:
        """Prototyping purpose only."""
        keywords = set(query.lower().split())
        response = SearchMemoryResponse()
        for key, events in self.session_events.items():
            if not key.startswith(f'{app_name}/{user_id}/'):
                continue
            matched_events = []
            for event in events:
                if not event.content or not event.content.parts:
                    continue
                parts = event.content.parts
                text = '\n'.join([part.text for part in parts if part.text]).lower()
                for keyword in keywords:
                    if keyword in text:
                        matched_events.append(event)
                        break
            if matched_events:
                session_id = key.split('/')[-1]
                response.memories.append(
                    MemoryResult(session_id=session_id, events=matched_events)
                )
        return response