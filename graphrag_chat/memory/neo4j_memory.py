
from google.adk.events import Event
from google.adk.sessions import Session
from google.adk.memory.base_memory_service import BaseMemoryService
from google.adk.memory.base_memory_service import MemoryResult
from google.adk.memory.base_memory_service import SearchMemoryResponse


class Neo4jMemoryService(BaseMemoryService):
  """An in-memory memory service for prototyping purpose only.

  Uses keyword matching instead of semantic search.
  """

  def __init__(self):
    self.session_events: dict[str, list[Event]] = {}
    """keys are app_name/user_id/session_id"""

  def add_session_to_memory(self, session: Session):
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