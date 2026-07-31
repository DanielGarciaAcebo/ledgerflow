from dataclasses import dataclass, field


@dataclass(slots=True)
class Transaction:
    name: str
    amount: object
    group_assignments: dict[str, bool] = field(
        default_factory=dict,
    )

