from dataclasses import dataclass
from datetime import date

@dataclass
class Ingredient:
    def __init__(self, name: str, expiration_date: date, open_date: date = None, max_days_after_open: int = None, unit: str = 'g'):
        self.name = name
        self.expiration_date = expiration_date
        self.open_date = open_date
        self.max_days_after_open = max_days_after_open
        self.unit = unit

    def is_expired(self) -> bool:
        today = date.today()
        if self.open_date and self.max_days_after_open:
            open_expiration = self.open_date + date.timedelta(days=self.max_days_after_open)
            return today > open_expiration or today > self.expiration_date
        return today > self.expiration_date

    def __repr__(self):
        lines = [
            f"Ingredient:",
            f"  - Name:             {self.name}",
            f"  - Expiration Date:  {self.expiration_date.isoformat()}",
        ]
        if self.open_date and self.max_days_after_open is not None:
            lines.append(f"  - Opened On:        {self.open_date.isoformat()}")
            lines.append(f"  - Best After Open:  {self.max_days_after_open} days")
        lines.append(f"  - Unit:             {self.unit}")
        lines.append(f"  - Expired?          {'YES' if self.is_expired() else 'NO'}")
        return "\n".join(lines)