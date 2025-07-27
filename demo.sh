#!/bin/bash
# Phyton demonstration script
# This shows off all the features of Phyton

echo "🌱 Welcome to Phyton Demo! 🌱"
echo "================================"
echo "The Python interpreter for bad spellers!"
echo ""

echo "1. Quick Start (basic misspellings):"
echo "------------------------------------"
./phyton examples/quick_start.phy
echo ""

echo "2. Hello World (classic programming with misspellings):"
echo "-------------------------------------------------------"
./phyton examples/hello_world.phy
echo ""

echo "3. Spelling Game (interactive fun):"
echo "-----------------------------------"
./phyton examples/spelling_game.phy
echo ""

echo "4. Advanced Features (complex constructs):"
echo "------------------------------------------"
./phyton examples/advanced_features.phy
echo ""

echo "5. Bad Speller's Paradise (maximum density):"
echo "--------------------------------------------"
./phyton examples/bad_spellers_paradise.phy
echo ""

echo "6. Spelling Nightmare (ultimate stress test):"
echo "---------------------------------------------"
./phyton examples/spelling_nightmare.phy
echo ""

echo "7. Strict Mode (no fuzzy matching):"
echo "-----------------------------------"
echo "Running with --no-fuzzy flag to disable fuzzy matching:"
./phyton --no-fuzzy examples/fuzzy_demo.phy
echo ""

echo "8. Command Option Misspellings:"
echo "-------------------------------"
echo "Phyton can even fix misspelled command options!"
echo "Trying --halp instead of --help:"
./phyton --halp | head -5
echo ""

echo "9. Fuzzy Demo (enabled by default):"
echo "-----------------------------------"
echo "Fuzzy matching helps with unknown misspellings:"
./phyton examples/fuzzy_demo.phy
echo ""

echo "🎉 Demo Complete! 🎉"
echo "==================="
echo "Phyton: Making Python accessible to bad spellers everywhere!"
echo "Try: ./phyton --interactive  (or even --interactiv!)"

echo ""
echo "🌿 Phyton Demo Complete! 🌿"
echo "All 7 examples ran successfully!"
echo ""
echo "💡 Next steps:"
echo "- Try interactive mode: ./phyton"
echo "- Try fuzzy matching: ./phyton --fuzzy examples/fuzzy_demo.phy"
echo "- Run individual examples: ./phyton examples/quick_start.phy"
echo "- Check examples/README.md for detailed explanations"
echo "- Create your own .phy files with creative misspellings!"
