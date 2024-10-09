from typing import TypedDict
from uuid import UUID

# ----------------------------------- POLL ----------------------------------- #

class CreatePollPayload(TypedDict):
    user_id: UUID
    prompt: str
    n_responses: int

# --------------------------------- RESPONSE --------------------------------- #

class UpdateResponsePayload(TypedDict):
    data: str