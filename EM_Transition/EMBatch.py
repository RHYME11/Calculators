import re
import os
import sys
import readline
import glob
import math
from B_unit_conv import conv_coeff


# Valid positive number
def check_positive(value, line_number, column_name):
  if value > 0:
    return value
  else:
    print(f"Invalid input! Line#{line_number},Column '{column_name}' must be a positive number!")
    sys.exit(1)
  

# Read each line:
def parse_line(line, line_number):
  parts = line.split()
  if len(parts) < 3:
    print("Miss information. A, Mult and Er are necessary.")
    sys.exit(1)
  try:
    A = check_positive(int(parts[0]), line_number, "A")
    Mult = parts[1]
    Multmatch = re.fullmatch(r"([EM])(\d+)", Mult)
    if not Multmatch:
      print(f"Invalid input @ Line#{line_number},Column 'Mult'.")
      sys.exit(1)
    Er = check_positive(float(parts[2]), line_number, "Er")
    
    if len(parts) > 3 and parts[3] !="" and float(parts[3]) !=-1:
      hl = check_positive(float(parts[3]), line_number, "t1/2")
    else:
      hl = -1.0

    if len(parts) > 4 and parts[4] !="":
      br = check_positive(float(parts[4]), line_number, "br")
      if not (0< br <= 1):
        print(f"Invalid input. Line {line_number}, Column 'br' must be between 0 and 1!")
        sys.exit(1)
    else:
      br = 1 # default br = 1  
 
    optional_fields = [float(parts[i]) if i < len(parts) else -1.0 for i in range(5, 11)] 
    
    # one of t1/2, BEM, BWu must exist
    BEM = optional_fields[4]
    BWu = optional_fields[5]
    if hl<0 and BEM<0 and BWu<0:
      print(f"Missing transition info (t1/2, BEM, BWu) in row {line_number}\n")
      sys.exit(1)

    return [A, Mult, Er, hl, br] + optional_fields[:6]  
  
  except ValueError:
    print(f"Invalid input! Line#{line_number}: Incorrect data format.")
    sys.exit(1)

# Read File
def ReadFile(input_file):
  data_mat = []
  with open(input_file, "r") as file:
    for line_number, line in enumerate(file, start=1):
      line = line.strip()
      if line.startswith("#") or not line:
        continue
      parsed_data = parse_line(line, line_number)
      if parsed_data:
        data_mat.append(parsed_data)
  return data_mat

#========================================== Calculation Formulas ======================================#
# Element#9: BEM Calculation
# 1st: BEM exists, keep the original value
# 2nd: BWu exists, calculate BEM based on BWu first
# Last: if neither BEM or BWu is known, calculate BEM based on Er, t1/2 and br.
def BEM(values):
  if values[9] > 0: # values[9] = BEM
    return values[9]
  elif values[10] > 0: # values[10] = BWu
    coeff = conv_coeff(values[1], values[0])
    coeff = 1./coeff # 1/coeff: convert Wu to e2fm2 
    return values[10]/coeff 
  else:
    transition_type = values[1]
    E_gamma = values[2]
    Tp = values[3]/values[4] # Tp = T/br
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

# Element#10: BWu Calculation
# 1st: BWu exists, keep the original value
# 2nd: BEM exists, calculate BWu based on BEM first
# Last: if neither BEM or BWu is known, calculate BEM based on Er, t1/2 and br.
def BWu(values):
  if values[10] > 0:
    return values[10]
  elif values[9] > 0:
    coeff = conv_coeff(values[1], values[0])
    return values[9]/coeff
  else:
    Tp = values[3] / values[4] # Tp = T/br
    tsp = sphl(values)
    return tsp/Tp

# Element#11: ME (matrix element) Calculation
def ME(values):
  BWu = values[9]
  Ji = values[6]
  if BWu > 0 and Ji >=0:
    return (BWu*(2*Ji+1))**0.5
  else:
    return -1

# Element#12: tsp Calculation
def sphl(values): # in unit ps^-1
  transition_type = values[1]
  A = values[0]
  E_gamma = values[2]
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

# Element#14: MEdex (matrix element) for de-excitation Calculation
def MEdex(values):
  BWu = values[13]
  Jf = values[8]
  if BWu > 0 and Jf >=0:
    return (BWu*(2*Jf+1))**0.5
  else:
    return -1

# Element#13: BEM for de-excitation Calculation
def BEM_dex(values):
  BEM = values[9]
  Ji = values[6]
  Jf = values[8]
  if BEM>0 and Ji>=0 and Jf>=0:
    return (2*Ji+1)/(2*Jf+1)*BEM
  else:
    return -1

# Element#14: BWu for de-excitation Calculation
def BWu_dex(values):
  BWu = values[10]
  Ji = values[6]
  Jf = values[8]
  if BWu>0 and Ji>=0 and Jf>=0:
    return (2*Ji+1)/(2*Jf+1)*BWu
  else:
    return -1
  
#======================= Input File =============================#

# Enable tab-completion for file paths
def complete_path(text, state):
  matches = glob.glob(text + '*')  # Get all matching files/folders
  return matches[state] if state < len(matches) else None
   
# Function to enable file path completion dynamically
def enable_path_completion():
  readline.set_completer(complete_path)
  readline.set_completer_delims(' \t\n') # Allow file paths with '/'
  # Detect if macOS is using libedit
  if "libedit" in readline.__doc__:
    readline.parse_and_bind("bind ^I rl_complete")  # MacOS (libedit) fix
  else:
    readline.parse_and_bind("tab: complete")  # Default GNU readline behavior

#======================= Output File =============================#
def write_to_file(data_mat, input_file):
  output_file = input_file.replace(".inp", ".out")
  with open(output_file,"w") as file:
    file.write("# ============================ Introduction ================================ #\n")
    file.write("# Output file for EM transition strengths calculation.\n")
    file.write("# All energies are in MeV.\n")
    file.write("# All times in ps.\n")
    file.write("# ME = matrix element in unit, like efm.\n")
    file.write("# tsp = single particle half-life in ps by Weisskopf estimation.\n")
    file.write("# BEM(↑) = B in unit e2fm2 for de-excitation.\n")
    file.write("# BWu(↑) = B in W.u. for de-excitation.\n")
    file.write("# ME(↑) = matrix element for de-excitation.\n")
    file.write("# ========================================================================== #\n\n\n")
    
    header_format = "{:<7} {:<8} {:<10} {:<10} {:<8} {:<10} {:<6} {:<6} {:<6} {:<12} {:<12} {:<12} {:<12} {:<12} {:<12} {:<12}\n"

    row_format = "{:<7} {:<8} {:<10.4f} {:<10.4f} {:<8.4f} {:<10.4f} {:<6} {:<6} {:<6} {:<12.4f} {:<12.4f} {:<12.4f} {:<12.4f} {:<12.4f} {:<12.4f} {:<12.4f}\n"
    

    file.write(header_format.format(
      "#A", "Mult", "Er", "t1/2", "br", "Ei", "Ji", "Ef", "Jf",
      "BEM", "BWu", "ME", "tsp", "BEM(↑)", "BWu(↑)", "ME(↑)"
    ))
    for row in data_mat:
      file.write(row_format.format(
        int(row[0]), row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8],
        row[9], row[10], row[11], row[12], row[13], row[14], row[15]
      ))

  print(f"Data written to '{output_file}' successfully!")

# main function
def main():
  while True:
    enable_path_completion()
    input_file = input(f"Enter input file path: ").strip()
    if not os.path.exists(input_file):
      print(f"File '{input_file}' does not exist. Please try again.\n")
    else:
      break
  
  data_mat = ReadFile(input_file)
  for row in data_mat:
    row[9]  = BEM(row)
    row[10] = BWu(row)
    row.append(ME(row))
    row.append(sphl(row))
    row.append(BEM_dex(row))   
    row.append(BWu_dex(row))   
    row.append(MEdex(row))   
  
  write_to_file(data_mat,input_file)


#============================================#
main()
#============================================#
