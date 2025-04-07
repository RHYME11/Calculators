
def conv_coeff(transition_type, A):
  # Define the formulas with transition_type and mass number
  formulas = {
    "E1": lambda A: 6.45e-2*(A**(2/3)), 
    "E2": lambda A: 5.94e-2*(A**(4/3)),
    "E3": lambda A: 5.94e-2*(A**2),
    "E4": lambda A: 6.29e-2*(A**(8/3)),
    "E5": lambda A: 6.93e-2*(A**(10/3)),
    "M1": lambda A: 1.79,
    "M2": lambda A: 1.65*(A**(2/3)),
    "M3": lambda A: 1.65*(A**(4/3)),
    "M4": lambda A: 1.75*(A**2),
  }
  
  return formulas.get(transition_type, lambda A:-1.0)(A) # Return 1.0 if not found





#=========== CLI Mode =============#
if __name__ == "__main__":
  #=========== Input ============#
  valid_transitions = {"E1", "E2", "E3", "E4", "E5", "M1", "M2", "M3", "M4"}
  
  # Validate transition type
  while True:
    transition = input("Enter mutipolarity (E1-E5, M1-M4): ").upper()
    if transition in valid_transitions:
      break
    else:
      print(f"Invalid input. Please enter a mutipolarity.")

  # Validate A (must be positive integer)
  while True:
    try:
      A = int(input("Enter mass number: "))
      if A > 0:
        break
      else:
        print("Invalid input. Mass number must be a positive integer.")
    except ValueError:
      print("Invalid input. Please enter a valid number.")

  # Mapping transition types to their respective units
  units = {
    "E1": "e²fm²",
    "E2": "e²fm⁴",
    "E3": "e²fm⁶",
    "E4": "e²fm⁸",
    "E5": "e²fm¹⁰",
    "M1": "μN²",
    "M2": "μN²fm²",
    "M3": "μN²fm⁴",
    "M4": "μN²fm⁶"
  }

  # convert to Weisskopf = 1, else = -1;
  while True:
    conv_wu = input(f"Convert from {units[transition]} to W.u. (y/n):").strip().lower()
    coeff = conv_coeff(transition,A)
    if conv_wu in {'y', 'n'}:
      break
    print("Invalid input. Please enter 'y' or 'n'.")

  coeff = conv_coeff(transition, A)
  if conv_wu == 'n':
    coeff = 1 / coeff

  # Validate BEM input
  while True:
    try:
      BEM = float(input(f"Enter B({transition}) in {units[transition] if conv_wu == 'y' else 'W.u.'}: "))
      if BEM > 0:
        break
      print("Transition strength must be a positive number.")
    except ValueError:
      print("Invalid input. Please enter a valid number.")

  B_conv = BEM/coeff
  formatted_result = f"B({transition}) = {BEM} {units[transition] if conv_wu == 'y' else 'W.u.'} ==> {round(B_conv, 4)} {'W.u.' if conv_wu == 'y' else units[transition]}"
  print(formatted_result)

