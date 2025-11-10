import re

# xsec: cross section in mb
# thickness: target thickness in mg/cm2
# A: target mass in g/mol
# Ibeam: beam intensity in pps
def calc_form(xsec, thickness, A, Ibeam):
  return (xsec / 1e27) * (thickness / 1e3 / A) * 6.023e23 * Ibeam

# Convert Ibeam unit
def Ibeam_unit_convert(Ibeam, unit):
  if unit == "pps":
    return Ibeam
  elif unit == "pnA":
    return Ibeam / 1e9 / 1.6e-19
  elif unit == "nA":
    Q = float(input("Enter beam charge state (e.g. 5 for 5+): "))
    return (Ibeam / 1e9) * Q / 1.6e-19

# Main
valid_Ibeam_unit = {"pps", "pnA", "nA"}
pattern = r"^([0-9.eE+-]+)\s*([a-zA-Z]+)$"

xsec = float(input("Enter production cross section (mb): "))
thickness = float(input("Enter target thickness (mg/cm2): "))
A = float(input("Enter target mass (g/mol): "))

# Ask until valid
while True:
  user_input = input("Enter beam intensity value and unit (e.g. '2.5 nA' or '2.5nA'): ").strip()
  match = re.match(pattern, user_input)
  if not match:
    print("⚠️  Invalid format. Example: 2.5 nA or 2.5nA")
    continue

  Ibeam_value = float(match.group(1))
  Ibeam_unit = match.group(2)
  if Ibeam_unit not in valid_Ibeam_unit:
    print("❌ Invalid unit. Please use one of:", valid_Ibeam_unit)
    continue
  break

# Convert and calculate
Ibeam_pps = Ibeam_unit_convert(Ibeam_value, Ibeam_unit)
result = calc_form(xsec, thickness, A, Ibeam_pps)

# Format output
formatted_result = "{:.4e}".format(result).replace("+", "")
print(f"Production rate (pps): {formatted_result}")
