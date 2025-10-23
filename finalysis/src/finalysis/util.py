from typing_extensions import Literal, TYPE_CHECKING
from datetime import timedelta
import numpy as np

def black_scholes_premium(
  price: float, strike: float, time2expiry: timedelta,
  *, iv: float, kind: Literal['call', 'put']
):
  """Compute Black-Scholes price for a European call or put option."""
  from scipy.stats import norm
  S, K, sigma = price, strike, iv
  T = time2expiry.total_seconds() / (365 * 24 * 3600)  # Convert timedelta to years
  d1 = (np.log(S / K) + (sigma**2 / 2) * T) / (sigma * np.sqrt(T))
  d2 = d1 - sigma * np.sqrt(T)

  if kind == 'call':
    return float(S * norm.cdf(d1) - K * norm.cdf(d2))
  else:
    return float(K * norm.cdf(-d2) - S * norm.cdf(-d1))