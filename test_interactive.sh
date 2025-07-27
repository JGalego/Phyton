#!/bin/bash
# Quick test of Phyton interactive mode

echo "Testing Phyton interactive mode..."
echo ""

# Create a test script that feeds commands to Phyton
cat << 'EOF' | python3 phyton.py
deff test():
    prin("Hello from interactive Phyton!")

test()
iff 2 + 2 == 4:
    prin("Math works!")

fore i inn range(2):
    prin(f"Interactive loop: {i}")

quit()
EOF
