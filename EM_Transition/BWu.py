import re
import math

def sphl(transition_type, A, E_gamma): # in unit ps^-1
  match = re.fullmatch(r"([EM])(\d+)", transition_type)
  if not match:
    raise ValueError("Invalid transition type format.")
  EM_type, L = match.groups()
  L = int(L)
  #print(f"L = {L}\t (2L+1)!! = {math.prod(range(2*L+1, 0, -2))}")
 
  hbarc = 197.327e-10 # unit: keV cm
  hbar = 6.58212e-19 # unit: keV s
  e2 = 1.44e-10 # unit: keV cm
  uN2 = 1.5922e-38 # unit: keV cm3
  R = 1.2e-13*(A**(1/3)) # unit: cm
  E_gamma = E_gamma*1e3 # unit: MeV -> keV

  if EM_type == 'E':
    tsp = 0.693*L*(math.prod(range(2*L+1, 0, -2))**2)*hbar/(2*(L+1)*e2*(R**(2*L)))*(((3+L)/3)**2)*((hbarc/E_gamma)**(2*L+1))
  if EM_type == 'M':
    tsp = 0.693*L*(math.prod(range(2*L+1, 0, -2))**2)*hbar/(80*(L+1)*uN2*(R**(2*L-2)))*(((3+L)/3)**2)*((hbarc/E_gamma)**(2*L+1))


  return tsp*1e12 # unit in ps; 






#=========== Input ============#
# Validate transition type
while True:
  transition = input("Enter mutipolarity (Eg, 'E2'): ").upper()
  match = re.fullmatch(r"([EM])(\d+)", transition)
  if not match:
    raise ValueError("Invalid transition type format.")
  else:
    break 
 
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
Tp = T / b # Tp = partial half-life
t_Weiss = sphl(transition, A, E_gamma) # Weisskopf estimation on single particle half-life in unit ps
BWu = t_Weiss/Tp # Wisskopf estimation on transition strengths

# Output results
print(f"B({transition}) = {round(BWu, 4)} W.u.")
print(f"t1/2(sp) = {round(t_Weiss, 4)} ps")


