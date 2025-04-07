# Calculators

## EM_Transition
Calculators for B(E/M), matrix elements, and conversions between B(E$`l`$/M$`l`$) in e$`^2`$fm$`^{2L}`$ and W.u.

### BEM.py
Calculation on transition strengths.
- **Input:** E$`_{\gamma}`$ and t$`_{1/2}`$.
- **Output:** B(E/M) in e$`^2`$fm$`^{2L}`$ or $`\mu`$N$`^2`$fm$`^{2(L-1)}`$.

### B_exc_conv.py
Converts transition strength to the reversed direction, typically used in Coulomb excitation analysis.
$`
B(f \to i) = \frac{(2J_i + 1)}{(2J_f + 1)} B(\uparrow i \to f).
`$
- **Input:** B(E/M), J$`_i`$, and J$`_f`$.
- **Output:** Reversed B(E/M) in the same unit as the input.

### ME.py
Calculation on reduced matrix element following,
$`
\boldsymbol{B(i \to f) = \frac{\left| \langle J_f || \mathcal{O} (\pi \lambda) || J_i \rangle \right|^2}{(2J_i + 1)}.}
`$
- **Input:** B(E/M), J$`_i`$.
- **Output:** ME = $`\left| \langle J_f || \mathcal{O} (\pi \lambda) || J_i \rangle \right|`$

### B_unit_conv.py:
Convert transition strengths(B) between units.
- **Input:** mass number(A), B(E/M).
- **Output:**  B(E/M).

### BWu.py
Calculation for B(E/M) in W.u. and estimate the single particle half-life.

The single-particle half-life for electric transitions:

$`
t_{1/2}(\gamma)(EL)_{SP} = \frac{\ln 2 \cdot L \cdot [(2L + 1)!!]^2 \hbar}
{2(L + 1)e^2 R^{2L}} 
\left( \frac{3 + L}{3} \right)^2 
\left( \frac{\hbar c}{E_{\gamma}} \right)^{2L+1}
`$

The single-particle half-life for magnetic transitions:

$`
t_{1/2}(\gamma)(ML)_{SP} = \frac{\ln 2 \cdot L \cdot [(2L + 1)!!]^2 \hbar}
{80(L + 1) \mu_N^2 R^{2L-2}} 
\left( \frac{3 + L}{3} \right)^2 
\left( \frac{\hbar c}{E_{\gamma}} \right)^{2L+1}
`$

- **Input:** E$`_{\gamma}`$, A and t$`_{1/2}`$.
- **Output:** B(E/M) in W.u., tsp in ps. 


### EMBatch.py
Batch process on multipole EM transitions for all calculations at once, including B(E/M) in 2 units, reversed B(E/M) in 2 units, matrix elements.
- **Input:** check `example.inp`
- **Output:** check `example.out`

|        | Input/Output   | Unit      | Notes                                                                                                                                                                 |
|--------|----------------|-----------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| A      | Input Required |           | mass number                                                                                                                                                           |
| Mult   | Input Required |           | Allow: E1-E5, M1-M4                                                                                                                                                   |
| Er     | Input Required | MeV       | Gamma Energy                                                                                                                                                          |
| t1/2   | Input Optional | ps        | Half-life of initial state. Not lifetime!!! Full half-life!!! (you can set it to partial half-life, and set br = 1 later.). Default t1/2 = -1.                        |
| br     | Input Optional |           | br = (0,1].  Default br = 1.                                                                                                                                          |
| Ei     | Input Optional | MeV       | E.x. of initial state, which should include the corrections for the decay to other states, the internal conversion coefficient and the mixing ratio. Default Ei = -1. |
| Ji     | Input Optional |           | Spin of initial state. Default Ji = -1.                                                                                                                               |
| Ef     | Input Optional | MeV       | E.x. of final state. Default Ef = -1.                                                                                                                                 |
| Jf     | Input Optional |           | Spin of final state. Default Jf = -1.                                                                                                                                 |
| BEM    | Input Optional | eg, e2fm2 | Transition strength.                                                                                                                                                  |
| BWu    | Input Optional | W.u.      | Weisskopf Estimation                                                                                                                                                  |
| ME     | Output         | eg, efm   | Matrix Element. Require: Ji >= 0.                                                                                                                                     |
| tsp    | Output         | ps        | Weisskopf Estimation Single-particle half-life (partial)..                                                                                                            |
| BEM(↑) | Output         | eg, e2fm2 | Transition strength. De-excitation. Require: Ji >= 0 && Jf <= 0                                                                                                       |
| BWu(↑) | Output         | W.u.      | Weisskopf Estimation De-excitation. Require:Ji >= 0 && Jf <= 0                                                                                                        |

**Note:** At least one of the following values must be provided: `t1/2`, `BEM`, or `BWu`.
The program will automatically calculate the missing value(s) based on the input.  
If only `t1/2` is provided, both `BEM` and `BWu` will be estimated using the Weisskopf approximation.

#### ⚠ Important Input Formatting Warning ⚠

1. When providing input values, **do not leave any empty spaces between true input values**. All columns before a valid input must be explicitly filled.  

✅ **Correct Example:**  
| #A  | Mult | Er   | t1/2 | br | Ei    | Ji  | Ef | Jf | BEM | BWu |
|-----|------|------|------|----|-------|----|----|----|----|----|
| 22  | E2   | 1.274 | 3.6  | 1  | 1.274 | 2  | 0  | 0  | -1  | -1  |

❌ **Incorrect Example (missing Ei value):**  
| #A  | Mult | Er   | t1/2 | br | Ei | Ji | Ef | Jf | BEM | BWu |
|-----|------|------|------|----|----|----|----|----|----|----|
| 20  | E2   | 1.633 | 0.73 | 1  | -  | 2  | -  | -  | -1  | -1  |

Leaving any blank space before a true input value can cause errors in processing the data. </br>


#### TODO
Convert python to c++.

