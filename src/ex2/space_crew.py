from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, ValidationError, model_validator


class MissionIdError(ValueError):
    def __init__(self, message: str) -> None:
        self.message = message

    def __str__(self) -> str:
        return f"{self.message}"


class LeaderMissingError(ValueError):
    def __init__(self, message: str) -> None:
        self.message = message

    def __str__(self) -> str:
        return f"{self.message}"


class LackExperienceError(ValueError):
    def __init__(self, message: str) -> None:
        self.message = message

    def __str__(self) -> str:
        return f"{self.message}"


class ActiveMemebersError(ValueError):
    def __init__(self, message: str) -> None:
        self.message = message

    def __str__(self) -> str:
        return f"{self.message}"


class Rank(Enum):
    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(..., min_length=3, max_length=10)
    name: str = Field(..., min_length=2, max_length=50)
    rank: Rank = Field(...)
    age: int = Field(..., ge=18, le=80)
    specialization: str = Field(..., min_length=3, max_length=30)
    years_experience: int = Field(..., ge=0, le=50)
    is_active: bool = Field(default=True)


class SpaceMission(BaseModel):
    mission_id: str = Field(..., min_length=5, max_length=15)
    mission_name: str = Field(..., min_length=3, max_length=100)
    destination: str = Field(..., min_length=3, max_length=50)
    launch_date: datetime = Field(...)
    duration_days: int = Field(..., ge=1, le=3650)
    # min length and
    # max works on any type that has a length: str,list,set , tuple
    crew: list[CrewMember] = Field(..., min_length=1, max_length=12)
    mission_status: str = Field(default="planned")
    budget_millions: float = Field(..., ge=1.0, le=10000.0)

    @model_validator(mode="after")
    def test(self) -> "SpaceMission":
        if not self.mission_id.startswith("M"):
            raise MissionIdError("Mission ID must start with 'M'")
        leader: bool = False
        for crew_member in self.crew:
            if (
                crew_member.rank.value == "captain"
                or crew_member.rank.value == "commander"
            ):
                leader = True
                break
        if leader is False:
            raise LeaderMissingError(
                "Must have at least one Commander or Captain"
            )

        if self.duration_days > 356:
            crew_num: int = int((len(self.crew) + 1) / 2)
            check_crew_experience = 0
            for crew_member in self.crew:
                if crew_member.years_experience > 5:
                    check_crew_experience += 1
            if check_crew_experience < crew_num:
                raise LackExperienceError("Long missions\
(> 365 days) need 50% experienced crew (5+ years)")
        if not all(crew_member.is_active for crew_member in self.crew):
            raise ActiveMemebersError("All crew members must be active")

        return self


if __name__ == "__main__":

    try:
        print("Space Mission Crew Validation")
        print("=================================")
        crew1 = CrewMember(
            member_id="ID-1",
            name="Ahmad Al-Quraan",
            rank=Rank.CADET,
            age=18,
            specialization="Mission Command",
            years_experience=3,
        )
        crew2 = CrewMember(
            member_id="ID-2",
            name="Mohmmad Al-Quraan",
            rank=Rank.CAPTAIN,
            age=18,
            specialization="Navigation",
            years_experience=6,
        )
        crew3 = CrewMember(
            member_id="ID-3",
            name="Sara Conor",
            rank=Rank.OFFICER,
            age=18,
            specialization="Engineering",
            years_experience=2,
        )
        crew_team: list[CrewMember] = []
        crew_team.append(crew1)
        crew_team.append(crew2)
        crew_team.append(crew3)
        mission1 = SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            launch_date=datetime(2026, 7, 14, 2, 33, 12),
            duration_days=900,
            crew=crew_team,
            budget_millions=2500.0,
        )
        print("Valid mission created:")
        print(f"Mission: {mission1.mission_name}")
        print(f"ID: {mission1.mission_id}")
        print(f"Destination: {mission1.destination}")
        print(f"Duration: {mission1.duration_days} days")
        print(f"Budget: ${mission1.budget_millions}M")
        print(f"Crew size: {len(mission1.crew)}")
        print("Crew members:")
        crew_team2: list[str] = []
        for crew_member in mission1.crew:
            crew_team2.append(f"{crew_member.name}\
({crew_member.rank}) - {crew_member.specialization}")

        for crew_member2 in crew_team2:
            print(f"- {crew_member2}")
    except ValidationError as e:
        print("Expected validation error:")
        for error in e.errors():
            print(error['msg'].removeprefix("Value error, "))
