#!/usr/bin/env python3

import math
import argparse


def d_min_fm(Ap: float, At: float) -> float:
  """
  Calculate D_min in fm.
  D_min = 1.25 * (Ap^(1/3) + At^(1/3)) + 5.0  [fm]
  """
  # [EDIT L16] Implement D_min formula from the attachment
  return 1.25 * (Ap ** (1.0 / 3.0) + At ** (1.0 / 3.0)) + 5.0


def safe_energy_mev(Ap: float, At: float, Zp: float, Zt: float, theta_cm_deg: float) -> float:
  """
  Calculate E(theta_CM) in MeV.

  E(theta_CM) = 0.72 * (Zp*Zt / D_min) * ((Ap + At)/At) * (1 + 1/sin(theta_CM/2))
  where theta_CM is in degrees (converted to radians internally).
  """
  if At <= 0:
    raise ValueError("At must be > 0.")
  if Ap <= 0:
    raise ValueError("Ap must be > 0.")

  Dmin = d_min_fm(Ap, At)

  theta_rad = math.radians(theta_cm_deg)
  half = theta_rad / 2.0
  s = math.sin(half)

  if abs(s) < 1e-15:
    raise ValueError("sin(theta_CM/2) is zero (or too close to zero). Choose a different angle.")

  # [EDIT L43] Implement E(theta_CM) formula from the attachment
  E = 0.72 * (Zp * Zt / Dmin) * ((Ap + At) / At) * (1.0 + 1.0 / s)
  return E


def _prompt_float(name: str) -> float:
  # English prompt but you can type numbers normally
  while True:
    raw = input(f"Enter {name}: ").strip()
    try:
      return float(raw)
    except ValueError:
      print("Invalid number, please try again.")


def main() -> None:
  parser = argparse.ArgumentParser(
    description="Calculate D_min [fm] and E(theta_CM) [MeV] using the attached formulas."
  )
  parser.add_argument("--Ap", type=float, help="Projectile mass number A_p")
  parser.add_argument("--At", type=float, help="Target mass number A_t")
  parser.add_argument("--Zp", type=float, help="Projectile charge Z_p")
  parser.add_argument("--Zt", type=float, help="Target charge Z_t")
  parser.add_argument("--theta", type=float, help="theta_CM in degrees")
  args = parser.parse_args()

  Ap = args.Ap if args.Ap is not None else _prompt_float("projectile A")
  Zp = args.Zp if args.Zp is not None else _prompt_float("projectile Z")
  At = args.At if args.At is not None else _prompt_float("target A")
  Zt = args.Zt if args.Zt is not None else _prompt_float("target Z")
  theta = args.theta if args.theta is not None else _prompt_float("theta (center of mass, deg)")

  Dmin = d_min_fm(Ap, At)
  E = safe_energy_mev(Ap, At, Zp, Zt, theta)

  print("\n=== Results ===")
  print(f"D_min = {Dmin:.1f} fm")
  print(f"E(theta_CM={theta:.6f} deg) = {E:.6f} MeV")


if __name__ == "__main__":
  main()

