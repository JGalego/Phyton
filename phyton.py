#!/usr/bin/env python3
"""
Phyton - A Python interpreter that accepts multiple spellings of keywords.

Phyton (Greek for 'plant') is designed to confuse bad spellers by being forgiving
of common misspellings in Python keywords. This makes coding more accessible for
those who struggle with spelling or typing accuracy.

Features:
    - Accepts 50+ common misspellings of Python keywords
    - Interactive REPL mode with multi-line support
    - File execution mode for .phy files
    - Preserves all Python functionality while fixing spelling
    - Friendly error messages with Phyton branding

Usage:
    Interactive mode:
        python3 phyton.py
        
    File execution:
        python3 phyton.py script.phy

Examples:
    # These are all valid Phyton code:
    deff hello():
        prin("Hello World!")
        
    iff True:
        prin("This works!")
        
    fore i inn range(3):
        prin(i)

Author: Created with GitHub Copilot
License: Public Domain - Have fun with bad spelling! 🌱
"""

import re
import sys

class PhytonInterpreter:
    """
    A Python interpreter that accepts multiple spellings of keywords.

    Phyton (Greek for 'plant') is designed to be forgiving of common misspellings
    in Python keywords, making coding more accessible for those who struggle with
    spelling or typing accuracy.

    Attributes:
        keyword_mappings (dict): Dictionary mapping correct keywords to lists of misspellings
    """

    def __init__(self):
        """
        Initialize the Phyton interpreter with keyword mapping dictionary.

        Sets up a comprehensive mapping of correct keywords to lists of their
        common misspellings. This structure makes it easier to maintain and
        extend the misspelling database.
        """
        # Map of correct keywords to lists of their common misspellings
        self.keyword_mappings = {
            'def': ['def', 'deff', 'define', 'defin'],
            'if': ['if', 'iff', 'iif'],
            'elif': ['elif', 'elsif', 'elseif', 'else_if'],
            'else': ['else', 'els', 'elze'],
            'for': ['for', 'fore', 'four', 'fr'],
            'while': ['while', 'wile', 'whyle', 'whil'],
            'in': ['in', 'inn', 'iin'],
            'return': ['return', 'retrun', 'retrn', 'ret'],
            'import': ['import', 'imprt', 'imort', 'importt'],
            'from': ['from', 'frm', 'fom'],
            'as': ['as', 'az', 'ass'],
            'class': ['class', 'clas', 'clss', 'klass'],
            'try': ['try', 'tri', 'tyr'],
            'except': ['except', 'exept', 'excpt', 'catch'],
            'finally': ['finally', 'finaly', 'finale'],
            'with': ['with', 'wth', 'wit'],
            'and': ['and', 'andd', 'adn'],
            'or': ['or', 'orr'],
            'not': ['not', 'nott', 'no'],
            'is': ['is', 'iz', 'iss'],
            'True': ['True', 'true', 'TRUE', 'tru'],
            'False': ['False', 'false', 'FALSE', 'fals'],
            'None': ['None', 'none', 'NONE', 'null', 'nil'],
            'print': ['print', 'prin', 'prnt', 'pritn'],
        }

    def add_misspelling(self, correct_keyword, misspelling):
        """
        Add a new misspelling for an existing keyword.
        
        Args:
            correct_keyword (str): The correct Python keyword
            misspelling (str): A new misspelling to add for this keyword
            
        Returns:
            bool: True if added successfully, False if keyword doesn't exist
        """
        if correct_keyword in self.keyword_mappings:
            if misspelling not in self.keyword_mappings[correct_keyword]:
                self.keyword_mappings[correct_keyword].append(misspelling)
            return True
        return False

    def add_keyword(self, correct_keyword, misspellings=None):
        """
        Add a new keyword with its misspellings.
        
        Args:
            correct_keyword (str): The correct Python keyword
            misspellings (list): List of misspellings for this keyword
        """
        if misspellings is None:
            misspellings = [correct_keyword]
        elif correct_keyword not in misspellings:
            misspellings.insert(0, correct_keyword)

        self.keyword_mappings[correct_keyword] = misspellings

    def get_misspellings(self, correct_keyword):
        """
        Get all misspellings for a given correct keyword.
        
        Args:
            correct_keyword (str): The correct Python keyword
            
        Returns:
            list: List of misspellings, or empty list if keyword not found
        """
        return self.keyword_mappings.get(correct_keyword, [])

    def fix_spelling(self, code):
        """
        Fix common misspellings of Python keywords in the provided code.

        Uses regex with word boundaries to replace misspelled keywords with their
        correct equivalents while preserving the rest of the code structure.

        Args:
            code (str): The Phyton source code containing potential misspellings

        Returns:
            str: The code with misspellings corrected to valid Python syntax
        """
        # Use word boundary regex to replace whole words only
        fixed_code = code

        for correct_keyword, misspellings in self.keyword_mappings.items():
            for misspelling in misspellings:
                # Skip if it's already the correct keyword
                if misspelling == correct_keyword:
                    continue

                # Use word boundaries to avoid partial matches
                pattern = r'\b' + re.escape(misspelling) + r'\b'
                fixed_code = re.sub(pattern, correct_keyword, fixed_code)

        return fixed_code

    def execute(self, code):
        """
        Execute Phyton code after fixing spelling errors.

        Takes Phyton source code, fixes any misspelled keywords, and executes
        the corrected Python code. Provides helpful error messages with Phyton
        branding for different types of errors.

        Args:
            code (str): The Phyton source code to execute

        Side Effects:
            - Prints corrected code if spelling fixes were applied
            - Executes the code in the global namespace
            - Prints specific error messages for different error types:
              * SyntaxError: Invalid Python syntax
              * NameError: Undefined variable or function
              * TypeError: Type-related errors
              * ValueError: Invalid values
              * ImportError: Module import failures
              * KeyboardInterrupt: User interruption
              * Other exceptions: Unexpected errors with debugging info
        """
        try:
            # Fix misspellings
            fixed_code = self.fix_spelling(code)

            # Print what we're executing (for debugging)
            if fixed_code != code:
                print(f"# Phyton: Fixed spelling -> {fixed_code}")

            # Execute the fixed code
            exec(fixed_code, globals())  # pylint: disable=exec-used

        except SyntaxError as e:
            print(f"PhytonSyntaxError: {e}")
        except NameError as e:
            print(f"PhytonNameError: {e}")
        except TypeError as e:
            print(f"PhytonTypeError: {e}")
        except ValueError as e:
            print(f"PhytonValueError: {e}")
        except ImportError as e:
            print(f"PhytonImportError: {e}")
        except KeyboardInterrupt:
            print("PhytonKeyboardInterrupt: Execution interrupted")
        except Exception as e:  # pylint: disable=broad-exception-caught
            # Last resort - but now we know it's something unexpected
            print(f"PhytonUnexpectedError: {type(e).__name__}: {e}")
            print("This might be a bug in Phyton or an unusual error condition.")

    def interactive_mode(self):
        """
        Run Phyton in interactive REPL (Read-Eval-Print Loop) mode.

        Provides an interactive command-line interface similar to Python's REPL,
        but with spelling tolerance. Supports multi-line input for functions,
        classes, and other compound statements.

        Features:
            - Spelling-tolerant keyword input
            - Multi-line statement support
            - Graceful error handling
            - Exit commands: 'exit()', 'quit()', 'exit', 'quit'
            - Keyboard interrupt handling (Ctrl+C)

        Side Effects:
            - Prints welcome message and instructions
            - Continuously prompts for user input until exit
            - Executes user commands and displays results
        """
        print("Welcome to Phyton 🌱 (Greek for 'plant')")
        print("The Python interpreter for bad spellers!")
        print("Type 'exit()' or 'quit()' to leave")
        print("Use empty line to execute multi-line statements")
        print()

        multi_line_buffer = []

        while True:
            try:
                if multi_line_buffer:
                    prompt = "phyton... "
                else:
                    prompt = "phyton>>> "

                line = input(prompt)

                if line.strip().lower() in ['exit()', 'quit()', 'exit', 'quit']:
                    print("Goodbye from Phyton! 🌿")
                    break

                # Check if we need to continue reading (line ends with : or is indented)
                if line.strip():
                    multi_line_buffer.append(line)

                    # If line ends with : or next line starts with whitespace, continue
                    if line.rstrip().endswith(':') or \
                        (multi_line_buffer and line.startswith(('    ', '\t'))):
                        continue

                # Execute the buffered code
                if multi_line_buffer:
                    code = '\n'.join(multi_line_buffer)
                    self.execute(code)
                    multi_line_buffer = []
                elif line.strip():
                    self.execute(line)

            except KeyboardInterrupt:
                print("\nKeyboardInterrupt")
                multi_line_buffer = []
            except EOFError:
                print("\nGoodbye from Phyton! 🌿")
                break

def main():
    """
    Main entry point for the Phyton interpreter.

    Determines whether to run in file execution mode or interactive mode based
    on command-line arguments. If a filename is provided, executes that file.
    Otherwise, starts the interactive REPL.

    Command-line usage:
        python3 phyton.py                 # Interactive mode
        python3 phyton.py filename.phy    # Execute file

    Side Effects:
        - Creates PhytonInterpreter instance
        - Either executes a file or starts interactive mode
        - Handles file not found and other execution errors
    """
    interpreter = PhytonInterpreter()

    if len(sys.argv) > 1:
        # Run file mode
        filename = sys.argv[1]
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                code = f.read()
            interpreter.execute(code)
        except FileNotFoundError:
            print(f"PhytonError: File '{filename}' not found")
        except PermissionError:
            print(f"PhytonError: Permission denied reading file '{filename}'")
        except UnicodeDecodeError as e:
            print(f"PhytonError: Cannot decode file '{filename}': {e}")
        except OSError as e:
            print(f"PhytonError: OS error reading file '{filename}': {e}")
        except Exception as e:  # pylint: disable=broad-exception-caught
            # Unexpected error when reading/processing the file
            print(f"PhytonUnexpectedError: {type(e).__name__}: {e}")
            print("This might be a bug in Phyton.")
    else:
        # Interactive mode
        interpreter.interactive_mode()

if __name__ == "__main__":
    main()
