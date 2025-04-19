# Quantum Approximate Optimization Algorithm (QAOA) for Portfolio Optimization

This project implements a quantum approximate optimization algorithm (QAOA) for portfolio optimization, using NumPy and SciPy to simulate the quantum behavior.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

- **Problem:** We address a toy portfolio optimization problem where the objective is to minimize a risk measure subject to a budget constraint (select exactly 2 assets out of 3).
- **Approach:** We model the problem as a quadratic objective function with a penalty term for constraint violations. QAOA is then used to find an optimal (or near-optimal) solution.
- **Tools:** This project uses NumPy and SciPy to simulate the quantum behavior of QAOA from scratch, without relying on quantum computing libraries.

## Mathematical Formulation

### Portfolio Optimization Problem

The Markowitz portfolio optimization problem can be formulated as follows:

Minimize the risk: 
$$ \text{Risk} = \sum_{i=1}^{n} \sum_{j=1}^{n} x_i Q_{ij} x_j $$

Subject to the budget constraint:
$$ \sum_{i=1}^{n} x_i = k $$

Where:
- $x_i \in \{0, 1\}$ is a binary variable indicating whether asset $i$ is selected (1) or not (0)
- $Q_{ij}$ represents the covariance between assets $i$ and $j$ (risk matrix)
- $k$ is the number of assets to select (in our case, $k=2$)

In our implementation, we convert this to an unconstrained problem by adding a penalty term:
$$ \text{Cost} = \sum_{i=1}^{n} \sum_{j=1}^{n} x_i Q_{ij} x_j + \lambda \left( \sum_{i=1}^{n} x_i - k \right)^2 $$

Where $\lambda$ is a penalty parameter (set to 10 in our implementation).

### QAOA Algorithm

The QAOA algorithm works as follows:

1. We map our optimization problem to a cost Hamiltonian $H_C$ where:
   $$ H_C|\mathbf{x}\rangle = \text{Cost}(\mathbf{x})|\mathbf{x}\rangle $$

2. We use a mixing Hamiltonian $H_M$ that explores the solution space:
   $$ H_M = \sum_{i=1}^{n} X_i $$
   where $X_i$ is the Pauli-X operator applied to qubit $i$.

3. We prepare an initial state $|\psi_0\rangle$ as the equal superposition of all basis states:
   $$ |\psi_0\rangle = \frac{1}{\sqrt{2^n}} \sum_{\mathbf{x}} |\mathbf{x}\rangle $$

4. Apply the QAOA circuit with parameters $\gamma$ and $\beta$:
   $$ |\psi(\gamma, \beta)\rangle = e^{-i\beta H_M} e^{-i\gamma H_C} |\psi_0\rangle $$

5. Compute the expectation value of the cost:
   $$ E(\gamma, \beta) = \langle\psi(\gamma, \beta)| H_C |\psi(\gamma, \beta)\rangle $$

6. Optimize the parameters $\gamma$ and $\beta$ to minimize $E(\gamma, \beta)$.

7. Measure the resulting state in the computational basis. The most probable outcome corresponds to the approximate solution.

## Files

- `README.md`: This file.
- `requirements.txt`: Contains the Python dependencies.
- `main.py`: An implementation of QAOA from scratch using NumPy and SciPy.

## Installation

### Clone the Repository

```bash
git clone https://github.com/geeky-orange/Quantum-Approximate-Optimization-Algorithm-QAOA-.git
cd Quantum-Approximate-Optimization-Algorithm-QAOA-
```

### Create a Virtual Environment and Install Dependencies

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

Run the QAOA implementation:

```bash
python main.py
```

This will output the optimal asset selection and risk value for the portfolio optimization problem.

## QAOA Implementation Details

Our implementation directly simulates the quantum state evolution:

1. **Cost Hamiltonian Construction**: We map our portfolio optimization problem to a diagonal matrix where each entry corresponds to the cost of a particular asset selection.

2. **Mixing Hamiltonian Construction**: We implement the tensor product structure of $H_M$ using NumPy's kron function.

3. **Unitary Evolution**: We compute the matrix exponentials $U_C = e^{-i\gamma H_C}$ and $U_M = e^{-i\beta H_M}$ using SciPy's expm function.

4. **Parameter Optimization**: We perform a grid search over $\gamma \in [0, 2\pi]$ and $\beta \in [0, \pi]$ to find the optimal parameters.

5. **State Measurement**: We compute the probability distribution of the final quantum state and identify the most probable solution.

## Results Discussion

The QAOA algorithm successfully finds the optimal portfolio allocation for our toy problem. Here are the key insights from the results:

### Optimal Solution
- **Selected Assets**: 1 and 2 (binary representation: 011)
- **Risk Value**: 2.4
- **Constraint Satisfaction**: Exactly 2 assets selected, as required

### Parameter Optimization
- **Optimal γ**: 4.62
- **Optimal β**: 2.69

### Analysis of All Possible States
When looking at all 8 possible states (2³ for 3 binary variables), we can observe:

1. **States with exactly 2 assets**:
   - State 011 (assets 1,2): Risk = 2.4 ← **Optimal solution**
   - State 101 (assets 0,2): Risk = 2.6 
   - State 110 (assets 0,1): Risk = 3.0

2. **States with constraint violations**:
   - States with 1 asset (001, 010, 100): Risk values are lower (1.0), but violate our constraint
   - State with 3 assets (111): Risk value is higher (5.0) and violates our constraint
   - State with 0 assets (000): Risk value is 0, but violates our constraint

This demonstrates that QAOA correctly navigates the trade-off between minimizing the objective function and satisfying constraints, encoded through penalty terms. The algorithm successfully finds the global optimum among all feasible solutions (those that satisfy our constraint of selecting exactly 2 assets).

### QAOA Effectiveness
The fact that a single-layer (p=1) QAOA circuit with optimized parameters can find the exact solution to this small problem demonstrates the promise of QAOA for combinatorial optimization. For larger problems, deeper circuits (larger p values) would likely be needed to achieve high-quality solutions.

## Extending the Project

Here are some ways you could extend the project:

1. **Increase Problem Size**: Add more assets to see how the algorithm scales
2. **Multiple QAOA Layers**: Implement p>1 QAOA layers for better performance
3. **Better Parameter Optimization**: Use more sophisticated optimization strategies
4. **Real Quantum Hardware**: Interface with Qiskit or other libraries to run on real quantum hardware
5. **Additional Constraints**: Add more realistic portfolio constraints like sector diversification

## References

- [Best practices for portfolio optimization by quantum computing, experimented on real quantum devices](https://doi.org/10.1038/s41598-023-45392-w)
- [Farhi, E., Goldstone, J., & Gutmann, S. (2014). A Quantum Approximate Optimization Algorithm](https://arxiv.org/abs/1411.4028)
- [Guerreschi, G. G., & Matsuura, A. Y. (2019). QAOA for Max-Cut Problems](https://arxiv.org/abs/1901.08059)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Notes

This is a toy example meant for educational purposes. Further improvements and scaling would be necessary to handle real-world portfolio optimization problems with more assets and complex constraints. 