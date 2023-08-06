from typing import (Callable,
                    TypeVar)

Domain = TypeVar('Domain')
Range = TypeVar('Range')
Map = Callable[[Domain], Range]
Operator = Map[Domain, Domain]
