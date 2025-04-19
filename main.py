import numpy as np
import scipy.linalg as sla
from math import pi, sqrt


def construct_cost_hamiltonian(n, Q, penalty):
    """Construct the cost Hamiltonian H_C as a diagonal matrix over the computational basis.

    For each basis state (represented by an integer s), compute:
      cost = x^T Q x + penalty * (sum(x) - 2)^2
    where x is the binary vector representation of s with n bits.
    """
    dim = 2 ** n
    diag = np.zeros(dim)
    for s in range(dim):
        # Convert integer s to binary vector of length n
        x = np.array(list(map(int, bin(s)[2:].zfill(n))))
        cost = x @ Q @ x + penalty * (np.sum(x) - 2) ** 2
        diag[s] = cost
    H_C = np.diag(diag)
    return H_C, diag


def construct_mixing_hamiltonian(n):
    """Construct the mixing Hamiltonian H_M = sum_{i=0}^{n-1} X_i where X is the Pauli-X matrix."""
    X = np.array([[0, 1], [1, 0]])
    I = np.eye(2)
    dim = 2 ** n
    H_M = np.zeros((dim, dim))
    for i in range(n):
        # Build operator for i-th qubit: kron(I,..., X, ..., I)
        op = 1
        for j in range(n):
            op = np.kron(op, X) if j == i else np.kron(op, I)
        H_M += op
    return H_M


def qaoa_state(gamma, beta, H_C, H_M, psi0):
    """Compute the state produced by a single-layer QAOA circuit.

    U_C(gamma) = exp(-i * gamma * H_C) (H_C is diagonal)
    U_M(beta)  = exp(-i * beta * H_M)
    Returns: state = U_M * U_C * psi0
    """
    # Since H_C is diagonal, compute its exponential easily
    U_C = np.diag(np.exp(-1j * gamma * np.diag(H_C)))
    U_M = sla.expm(-1j * beta * H_M)
    state = U_M @ U_C @ psi0
    return state


def expectation_value(state, diag_cost):
    """Compute the expectation value of the cost Hamiltonian given the state and its diagonal entries."""
    probs = np.abs(state) ** 2
    return np.sum(probs * diag_cost)


def main():
    n = 3  # number of assets / qubits
    Q = np.array([[1.0, 0.5, 0.3],
                  [0.5, 1.0, 0.2],
                  [0.3, 0.2, 1.0]])
    penalty = 10.0

    # Construct Hamiltonians
    H_C, diag_cost = construct_cost_hamiltonian(n, Q, penalty)
    H_M = construct_mixing_hamiltonian(n)
    dim = 2 ** n
    psi0 = np.ones(dim, dtype=complex) / sqrt(dim)  # equal superposition state

    # Grid search over parameters gamma and beta
    best_val = float('inf')
    best_gamma = None
    best_beta = None
    gammas = np.linspace(0, 2 * pi, 50)
    betas = np.linspace(0, pi, 50)
    for gamma in gammas:
        for beta in betas:
            state = qaoa_state(gamma, beta, H_C, H_M, psi0)
            exp_val = expectation_value(state, diag_cost)
            if exp_val < best_val:
                best_val = exp_val
                best_gamma = gamma
                best_beta = beta
    
    print("Optimal parameters:")
    print("gamma =", best_gamma)
    print("beta =", best_beta)
    print("Expected cost =", best_val)
    
    # Evaluate the state at the optimal parameters
    state_opt = qaoa_state(best_gamma, best_beta, H_C, H_M, psi0)
    probs = np.abs(state_opt) ** 2
    best_state_index = np.argmax(probs)
    best_state_bin = bin(best_state_index)[2:].zfill(n)
    print("Most probable state (binary) =", best_state_bin)
    print("Cost for that state =", diag_cost[best_state_index])
    
    # Extract solution
    x = np.array(list(map(int, best_state_bin)))
    print(f"\nSelected assets: {[i for i in range(n) if x[i] == 1]}")
    print(f"Risk (quadratic term): {x @ Q @ x}")
    
    # Print all possible states and their costs for comparison
    print("\nAll possible states:")
    for s in range(2**n):
        s_bin = bin(s)[2:].zfill(n)
        x = np.array(list(map(int, s_bin)))
        risk = x @ Q @ x
        asset_count = np.sum(x)
        constraint_violation = (asset_count - 2)**2
        print(f"State {s_bin}: Risk = {risk:.3f}, Assets = {asset_count}, Violation = {constraint_violation}")


if __name__ == '__main__':
    main() 