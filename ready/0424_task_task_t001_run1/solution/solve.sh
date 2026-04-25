#!/bin/bash
set -e

# Create output directory
mkdir -p /root/output

# Create the solution Python script using heredoc
cat << 'EOF' > /root/solve_task.py
import json
import z3
from sympy import symbols, sqrt, simplify

# The common normalized LaTeX expression (quadratic formula) from trajectory
# This was extracted from the three input files and normalized by removing whitespace
COMMON_EXPR = r'x=\frac{-b\pm\sqrt{b^2-4ac}}{2a}'

OUTPUT_PATH = '/root/output/quadratic_common.json'

def prove_roots_real():
    """Use Z3 to prove that roots are real when a!=0 and D>=0."""
    z3_a = z3.Real('a')
    z3_b = z3.Real('b')
    z3_c = z3.Real('c')
    z3_D = z3_b * z3_b - 4 * z3_a * z3_c

    # Premises: a != 0 and D >= 0
    premises = z3.And(z3_a != 0, z3_D >= 0)

    # Theorem: premises => 2*a != 0 (denominator is non-zero, sqrt(D) is real)
    theorem = z3.Implies(premises, 2 * z3_a != 0)

    solver = z3.Solver()
    solver.set("timeout", 5000)
    solver.add(z3.Not(theorem))  # Prove by refutation

    result = solver.check()
    return result == z3.unsat

def compute_signature():
    """Compute signature by substituting a=1, b=5, c=6 into quadratic roots."""
    a, b, c = symbols('a b c', real=True)
    D = b**2 - 4*a*c

    # Quadratic formula roots
    r1 = (-b + sqrt(D)) / (2*a)
    r2 = (-b - sqrt(D)) / (2*a)

    # Substitute values
    r1_val = r1.subs({a: 1, b: 5, c: 6})
    r2_val = r2.subs({a: 1, b: 5, c: 6})

    # Product of roots
    product = simplify(r1_val * r2_val)

    # Signature: product * 1000, rounded
    signature = int(round(float(product.evalf()) * 1000))
    return signature

def main():
    # Prove roots are real
    roots_real_proved = prove_roots_real()

    # Compute signature
    signature = compute_signature()

    # Write output
    output = {
        "common_expr": COMMON_EXPR,
        "roots_real_proved": roots_real_proved,
        "signature": signature
    }

    with open(OUTPUT_PATH, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"Output written to {OUTPUT_PATH}")
    print(json.dumps(output, indent=2))

if __name__ == '__main__':
    main()
EOF

# Install dependencies and execute the script
pip install sympy z3-solver  --break-system-packages -q 2>/dev/null
python3 /root/solve_task.py
