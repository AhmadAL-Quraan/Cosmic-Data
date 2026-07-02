from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, model_validator


class ContactType(Enum):
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class alien_contact(BaseModel):
    contact_id: str = Field(..., min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(..., min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(..., ge=0.0, le=10.0)
    duration_minutes: int = Field(..., ge=1, le=1440)
    witness_count: int = Field(..., min_length=1, max_length=100)
    message_received: Optional[str] = Field(default=None, max_length=500)
    is_verified: bool = False

    @model_validator(mode="after")
    def test(self) -> "alien_contact":
        if self.contact_id != "AB":
            return ras


report = alien_contact(
    contact_id="AC-2026-01",
    timestamp=datetime(2026, 7, 3, 22, 15),
    location="Roswell, New Mexico",
    contact_type=ContactType.TELEPATHIC,
    signal_strength=8.9,
    duration_minutes="s",
    witness_count=4,
    message_received="They asked about our music.",
    is_verified=True,
)

# print(report.model_dump())
