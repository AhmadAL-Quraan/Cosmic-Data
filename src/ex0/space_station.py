from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ValidationError


# ... (Eclipse) means no default value, user must provide data for it
class station(BaseModel):
    station_id: str = Field(..., min_length=3, max_length=10)
    name: str = Field(..., min_length=1, max_length=50)
    crew_size: int = Field(..., ge=1, le=20)
    power_level: float = Field(..., ge=0.0, le=100.0)
    oxygen_level: float = Field(..., ge=0.0, le=100.0)
    last_maintenance: datetime = Field(...)
    is_operational: bool = Field(default=True)
    # Optioanl means: a
    # field can either be a string or None, short for Union[str,None]
    notes: Optional[str] = Field(default=None, max_length=200)


if __name__ == "__main__":

    station1 = station(
        station_id="ISS001",
        name="International space station",
        crew_size=4,
        power_level=1.0,
        oxygen_level=1.0,
        # datetime(year,month,day,hour, minute, second)
        last_maintenance=datetime(2025, 7, 2, 3, 45, 33),
    )
    # print dict
    # print(station1.model_dump())
    # json format
    # print(station1.model_validate(data))
    print("Space Station Data Validation")
    print("=========================================")
    print("Valid station created:")
    print(f"ID: {station1.station_id}")
    print(f"Name: {station1.name}")
    print(f"Crew: {station1.crew_size} people")
    print(f"Power: {station1.power_level}%")
    print(f"Oxygen: {station1.oxygen_level}%")
    print(f"Status:\
{"Operational" if station1.is_operational else "not Operational"}")
    print(f"{station1.last_maintenance}")
    print("\n =============================================")
    print("Expected validation error:")

    try:
        station2 = station(
            station_id="2",
            name="International space station",
            crew_size=23,
            power_level=1.0,
            oxygen_level=1.0,
            # datetime(year,month,day,hour, minute, second)
            last_maintenance=datetime(2026, 7, 2, 17, 30, 0),
        )
    except ValidationError as e:
        for err in e.errors():
            print(err['msg'])
