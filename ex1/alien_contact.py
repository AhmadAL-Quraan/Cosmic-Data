from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, model_validator


class StartError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self, message)

    def __str__(self) -> str:
        return f"{self.message}"


class Verified(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self, message)

    def __str__(self) -> str:
        return f"{self.message}"


class WitnessCount(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self, message)

    def __str__(self) -> str:
        return f"{self.message}"


class MessageError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self, message)

    def __str__(self) -> str:
        return f"{self.message}"


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
    witness_count: int = Field(..., ge=1, le=100)
    message_received: Optional[str] = Field(default=None, max_length=500)
    is_verified: bool = False

    @model_validator(mode="after")
    def test(self) -> "alien_contact":
        if not self.contact_id.startswith("AC"):
            # equal to print(start_with_error object) -> override on __str__
            raise StartError("Contact ID must start with 'AC' (Alien Contact)")

        if self.is_verified is False:
            raise Verified("Physical contact reports must be verified")

        if self.witness_count < 3:
            raise WitnessCount(
                "Telepathic contact requires at least 3 witnesses"
            )

        if self.signal_strength > 0.7 and self.message_received is None:
            raise MessageError(
                "Strong signals (> 7.0) should include received messages"
            )

        # Model validator,
        return self


if __name__ == "__main__":
    print("Alien Contact Log Validation")
    print("====================================")
    try:
        report = alien_contact(
            contact_id="AC-2026-01",
            timestamp=datetime(2026, 7, 3, 22, 15),
            location="Area 51, Nevada",
            contact_type=ContactType.RADIO,
            signal_strength=8.9,
            duration_minutes=45,
            witness_count=4,
            message_received="Greetings from Zeta Reticuli",
            is_verified=True,
        )
        print("Valid contact report:")
        print(f"ID: {report.contact_id}")
        print(f"Type: {report.contact_type.value}")
        print(f"Location: {report.location}")
        print(f"Signal: {report.signal_strength}")
        print(f"Duration: {report.duration_minutes}")
        print(f"Message: {report.message_received}")
    except Exception as e:
        print(f"Expected validation error:\n{e}")

    print("\n==============================================")
    try:
        report = alien_contact(
            contact_id="AC-2026-01",
            timestamp=datetime(2026, 7, 3, 22, 15),
            location="Area 51, Nevada",
            contact_type=ContactType.RADIO,
            signal_strength=8.9,
            duration_minutes=45,
            witness_count=4,
            message_received="Greetings from Zeta Reticuli",
            is_verified=False,
        )
        print("Valid contact report:")
        print(f"ID: {report.contact_id}")
        print(f"Type: {report.contact_type.value}")
        print(f"Location: {report.location}")
        print(f"Signal: {report.signal_strength}")
        print(f"Duration: {report.duration_minutes}")
        print(f"Message: {report.message_received}")
    except Exception as e:
        print(f"Expected validation error:\n{e}")
# print(report.model_dump())
