from dataclasses import dataclass
from datetime import date, timedelta
from .ingredient import Ingredient


@dataclass
class PantryIngredient:
    ing: Ingredient
    expiration_date: date
    opened_date: date = None
    max_days_after_open: int = None

    def is_expired(self) -> bool:
        today = date.today()
        if self.opened_date and self.max_days_after_open:
            open_expiration = self.opened_date + timedelta(days=self.max_days_after_open)
            return today > open_expiration or today > self.expiration_date
        return today > self.expiration_date

    def __repr__(self):
        lines = [
            f"Ingredient:",
            f"  - Name:             {self.ing.name}",
            f"  - Quantity:         {self.ing.amount} {self.ing.unit}",
        ]
        if self.expiration_date is not None:
            lines.append(f"  - Expiration Date:  {self.expiration_date.isoformat()}")
        if self.opened_date and self.max_days_after_open is not None:
            lines.append(f"  - Opened On:        {self.opened_date.isoformat()}")
            lines.append(f"  - Best After Open:  {self.max_days_after_open} days")
        lines.append(f"  - Expired?          {'YES' if self.is_expired() else 'NO'}")
        return "\n".join(lines)
