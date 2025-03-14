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

TODO:
### Batch_EM.py
Batch process on multipole EM transitions for all calculations at once, including B(E/M) in 2 units, reversed B(E/M) in 2 units, matrix elements.
- **Input:** input file (ref example.inp)
- **Output:** output file (ref example.out).
