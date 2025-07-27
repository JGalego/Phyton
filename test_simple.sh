#!/bin/bash
# Quick test of Phyton interactive mode with simple statements

echo "Testing Phyton interactive mode..."
echo ""

# Create a test script that feeds simple commands to Phyton
cat << 'EOF' | python3 phyton.py
prin("Hello Phyton!")
x = 5
iff x > 3: prin("x is big")
fore i inn range(3): prin(i)
quit()
EOF
