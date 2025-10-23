from typing_extensions import TypeVar
from abc import ABC, abstractmethod
from dataclasses import dataclass, field, replace
import numpy as np

N = float | np.ndarray

@dataclass
class Instrument(ABC):
  quantity: float = field(default=1, kw_only=True)

  @abstractmethod
  def payoff(self, underlying: N, /) -> np.ndarray:
    ...

  def __add__(self, other: 'Instrument') -> 'Sum':
    return Sum([self, other])
  
  def __mul__(self, quantity: float) -> 'Instrument':
    return replace(self, quantity=quantity*self.quantity)

  def __truediv__(self, quantity: float) -> 'Instrument':
    return self * (1/quantity)
  
  __rmul__ = __mul__

  def __neg__(self) -> 'Instrument':
    return self * -1
  
  def __sub__(self, other: 'Instrument') -> 'Sum':
    return self + -other
  
  def __rsub__(self, other: 'Instrument') -> 'Sum':
    return -self + other
  

@dataclass
class Sum(Instrument):
  instruments: list[Instrument]

  def payoff(self, underlying: N, /):
    return np.sum([instrument.payoff(underlying) for instrument in self.instruments], axis=0)
  
  def __add__(self, other: 'Instrument') -> 'Sum':
    return replace(self, instruments=self.instruments + [other])
  