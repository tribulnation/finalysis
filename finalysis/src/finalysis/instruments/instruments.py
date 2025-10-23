from typing_extensions import Literal
from datetime import timedelta
from dataclasses import dataclass
import numpy as np
from .base import Instrument, N

@dataclass
class Spot(Instrument):
  price: float

  def payoff(self, u: N):
    return np.array((u - self.price) * self.quantity)

@dataclass
class Option(Instrument):
  strike: float
  premium: float
  kind: Literal['call', 'put']

  def payoff(self, u: N):
    sign = 1 if self.kind == 'call' else -1
    diff = sign * (u - self.strike)
    return np.maximum(diff, 0) * self.quantity

  @classmethod
  def black_scholes(
    cls, price: float, strike: float, time2expiry: 'timedelta',
    *, iv: float, kind: Literal['call', 'put'],
  ):
    """Create an option from Black-Scholes parameters."""
    from finalysis import black_scholes_premium
    premium = black_scholes_premium(price, strike, time2expiry, iv=iv, kind=kind)
    return cls(strike=strike, premium=premium, kind=kind)
  
@dataclass
class Future(Instrument):
  price: float
  kind: Literal['long', 'short'] = 'long'

  def payoff(self, u: N):
    s = 1 if self.kind == 'long' else -1
    return np.array((u - self.price) * s * self.quantity)