def B_exc_conv(B, Ji, Jf):
  """Convert transition strength from de-excitation to excitation."""
  return (2 * Ji + 1) / (2 * Jf + 1) * B

def get_positive_float(prompt):
  """Prompt user for a positive float input."""
  while True:
    try:
      value = float(input(prompt))
      if value > 0:
        return value
      print("Invalid input. Value must be a positive number.")
    except ValueError:
      print("Invalid input. Please enter a valid number.")

def get_valid_spin(prompt):
  """Prompt user for a non-negative integer or half-integer spin."""
  while True:
    try:
      spin = float(input(prompt))
      if spin < 0:
        print("Invalid input. Spin must be non-negative.")
      elif spin * 2 % 1 != 0:
        print("Invalid input. Spin must be an integer or half-integer.")
      else:
        return spin
    except ValueError:
      print("Invalid input. Please enter a valid number.")

#=========== Input ============#
B = get_positive_float("Enter transition strength (Ji -> Jf): ")
Ji = get_valid_spin("Enter Ji: ")
Jf = get_valid_spin("Enter Jf: ")

#=========== Output ============#
B_revs = B_exc_conv(B, Ji, Jf)
print(f"Reversed transition strength (Jf -> Ji): {B_revs:.4f}")

