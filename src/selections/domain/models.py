class Selection:
    def __init__(
        self,
        country: str,
        confederation: str,
        captain: str,
        coach: str,
        world_cups: int,
        flag: str,
        id: int | None = None,
    ):
        self._id = id
        self._country = country
        self._confederation = confederation
        self._captain = captain
        self._coach = coach
        self._world_cups = world_cups
        self._flag = flag

    def id(self) -> int | None:
        return self._id

    def country(self) -> str:
        return self._country

    def confederation(self) -> str:
        return self._confederation

    def captain(self) -> str:
        return self._captain

    def coach(self) -> str:
        return self._coach

    def world_cups(self) -> int:
        return self._world_cups

    def flag(self) -> str:
        return self._flag
    
    def set_id(self, id: int) -> None:
        self._id = id

    def update(
        self,
        country: str,
        confederation: str,
        captain: str,
        coach: str,
        world_cups: int,
        flag: str,
    ) -> None:
        self._country = country
        self._confederation = confederation
        self._captain = captain
        self._coach = coach
        self._world_cups = world_cups
        self._flag = flag