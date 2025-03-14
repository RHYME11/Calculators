# Calculators

## EM_Transition
Calculators for B(E/M), matrix elements, and conversions between B(E$`l`$/M$`l`$) in e$`^2`$fm$`^{2L}`$ and W.u.

### BEM.py
- **Input:** E$`_{\gamma}`$ and t$`_{1/2}`$.
- **Output:** B(E/M) in e$`^2`$fm$`^{2L}`$ or $`\mu`$N$`^2`$fm$`^{2(L-1)}`$.

### B_exc_conv.py
Converts transition strength to the reversed direction, typically used in Coulomb excitation analysis.

$`
B(f \to i) = \frac{(2J_i + 1)}{(2J_f + 1)} B(\uparrow i \to f).
`$

- **Input:** B(E/M), J$`_i`$, and J$`_f`$.
- **Output:** Reversed B(E/M) in the same unit as the input.

