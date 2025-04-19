# Quantum Approximate Optimization for Portfolio Balancing

This project implements a quantum approximate optimization algorithm (QAOA) for portfolio optimization, using NumPy and SciPy to simulate the quantum behavior.



## Overview

- **Problem:** We address a toy portfolio optimization problem where the objective is to minimize a risk measure subject to a budget constraint (select exactly 2 assets out of 3).
- **Approach:** We model the problem as a quadratic objective function with a penalty term for constraint violations. QAOA is then used to find an optimal (or near-optimal) solution.
- **Tools:** This project uses NumPy and SciPy to simulate the quantum behavior of QAOA from scratch, without relying on quantum computing libraries.

## Files

- `README.md`: This file.
- `requirements.txt`: Contains the Python dependencies.
- `main.py`: An implementation of QAOA from scratch using NumPy and SciPy, without relying on quantum computing libraries.
- `.gitignore`: Specifies intentionally untracked files to ignore.


## Installation

### Clone the Repository

```bash
git clone https://github.com/your-username/quantum-portfolio-optimization.git
cd quantum-portfolio-optimization
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

## QAOA Implementation

The `main.py` file provides a pure NumPy/SciPy implementation of QAOA for portfolio optimization. It:

1. Constructs the cost Hamiltonian by mapping the portfolio optimization problem to a diagonal matrix
2. Constructs the mixing Hamiltonian using Pauli-X operators
3. Simulates the QAOA quantum circuit by applying the cost and mixing unitaries
4. Performs a grid search over gamma and beta parameters to find the optimal solution
5. Reports the optimal solution, showing which assets should be selected to minimize risk

This implementation is useful for educational purposes to understand how QAOA works without requiring a quantum computing library.

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

## Notes

This is a toy example meant for educational purposes. Further improvements and scaling would be necessary to handle real-world portfolio optimization problems with more assets and complex constraints. 