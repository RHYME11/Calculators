def transition_strength(transition_type, E_gamma, T, b):
  """
  Calculate transition strength based on given parameters.
  
  Parameters:
  transition_type (str): Type of transition (E1-E6, M1-M4)
  E_gamma (float): Gamma-ray energy in MeV
  T (float): Half-life in ps
  b (float): Branching ratio
  
  Returns:
  float: Transition strength B(X) with appropriate units.
  """
  # Convert half-life T to Tp using branching ratio
  Tp = T / b  # Tp in ps
  
  # Define the formulas with time unit adjusted to ps
  formulas = {
    "E1": lambda E, Tp: 0.435 / (E**3 * Tp) * 1e-3,  # ps conversion from fs
    "E2": lambda E, Tp: 564 / (E**5 * Tp) * 1,       # ps conversion from ps
    "E3": lambda E, Tp: 1212 / (E**7 * Tp) * 1e3,    # ps conversion from μs
    "E4": lambda E, Tp: 4076 / (E**9 * Tp) * 1e12,   # ps conversion from s
    "E5": lambda E, Tp: (2.00 * 10**10) / (E**11 * Tp) * 1e12,  # ps conversion from s
    "E6": lambda E, Tp: (1.35 * 10**17) / (E**13 * Tp) * 1e12,  # ps conversion from s
    "M1": lambda E, Tp: 39.4 / (E**3 * Tp) * 1e-3,   # ps conversion from ps
    "M2": lambda E, Tp: 51.2 / (E**5 * Tp) * 1e3,    # ps conversion from ns
    "M3": lambda E, Tp: 0.110 / (E**7 * Tp) * 1e12,   # ps conversion from s
    "M4": lambda E, Tp: (0.370 * 10**6) / (E**9 * Tp) * 1e12,  # ps conversion from s
  }
  
  return formulas[transition_type](E_gamma, Tp)


#=========== Input ============#
valid_transitions = {"E1", "E2", "E3", "E4", "E5", "E6", "M1", "M2", "M3", "M4"}
valid_transitions = {"E1", "E2", "E3", "E4", "E5", "E6", "M1", "M2", "M3", "M4"}

# Validate transition type
while True:
  transition = input("Enter mutipolarity (E1-E6, M1-M4): ").upper()
  if transition in valid_transitions:
    break
  else:
    print(f"Invalid input. Please enter a mutipolarity.")

# Validate E_gamma (must be positive)
while True:
  try:
    E_gamma = float(input("Enter gamma-ray energy (MeV): "))
    if E_gamma > 0:
      break
    else:
      print("Invalid input. Gamma-ray energy must be a positive number.")
  except ValueError:
    print("Invalid input. Please enter a valid number.")

# Validate T (must be positive)
while True:
  try:
    T = float(input("Enter half-life of the initial state (ps): "))
    if T > 0:
      break
    else:
      print("Invalid input. Half-life must be a positive number.")
  except ValueError:
    print("Invalid input. Please enter a valid number.")

# Validate b (must be 0 < b ≤ 1)
while True:
  try:
    b = float(input("Enter branching ratio (0 < b ≤ 1): "))
    if 0 < b <= 1:
      break
    else:
      print("Invalid input. Branching ratio must be between 0 and 1 (exclusive of 0).")
  except ValueError:
    print("Invalid input. Please enter a valid number.")

#=========== Output ===========#
result = transition_strength(transition, E_gamma, T, b)

# Mapping transition types to their respective units
units = {
  "E1": "e²fm²",
  "E2": "e²fm⁴",
  "E3": "e²fm⁶",
  "E4": "e²fm⁸",
  "E5": "e²fm¹⁰",
  "E6": "e²fm¹²",
  "M1": "μN²fm²",
  "M2": "μN²fm²",
  "M3": "μN²fm⁴",
  "M4": "μN²fm⁶"
}
formatted_result = f"B({transition}) = {round(result, 4)} {units[transition]}"
print(formatted_result)



