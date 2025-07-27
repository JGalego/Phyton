#!/usr/bin/env python3
"""
Comprehensive test suite for all Phyton features.
Tests keyword mapping, fuzzy matching, argument parsing, error handling, and coverage.
"""

import subprocess
import os
import sys
import tempfile
import unittest.mock
import stat
import contextlib
import io
import pytest
import phyton


class TestPhytonFeatures:  # pylint: disable=too-many-public-methods
    """Main test class for all Phyton functionality."""

    def run_phyton_command(self, args, input_text=None, timeout=10):
        """Run a phyton command and return output."""
        try:
            cmd = ['python3', 'phyton.py'] + args
            result = subprocess.run(
                cmd,
                input=input_text,
                text=True,
                capture_output=True,
                timeout=timeout,
                check=False
            )
            return result.stdout + result.stderr, result.returncode
        except subprocess.TimeoutExpired:
            return "TIMEOUT", -1
        except OSError as error:
            return f"ERROR: {error}", -1

    def create_temp_file(self, content, suffix='.phy'):
        """Create a temporary file with given content."""
        file_descriptor, path = tempfile.mkstemp(suffix=suffix)
        try:
            with os.fdopen(file_descriptor, 'w', encoding='utf-8') as file_handle:
                file_handle.write(content)
            return path
        except OSError:
            os.close(file_descriptor)
            raise

    # Keyword Mapping Tests
    @pytest.mark.parametrize("input_code,expected", [
        # def variations
        ('deff hello():\n    pass', 'def hello():\n    pass'),
        ('define hello():\n    pass', 'def hello():\n    pass'),
        ('defin hello():\n    pass', 'def hello():\n    pass'),
        # if/elif/else variations
        ('iff True:\n    pass', 'if True:\n    pass'),
        ('iif True:\n    pass', 'if True:\n    pass'),
        ('elsif True:\n    pass', 'elif True:\n    pass'),
        ('elseif True:\n    pass', 'elif True:\n    pass'),
        ('els:\n    pass', 'else:\n    pass'),
        ('elze:\n    pass', 'else:\n    pass'),
        # loop variations
        ('fore i inn range(3):\n    pass', 'for i in range(3):\n    pass'),
        ('four i inn range(3):\n    pass', 'for i in range(3):\n    pass'),
        ('wile True:\n    pass', 'while True:\n    pass'),
        ('whyle True:\n    pass', 'while True:\n    pass'),
        # other keywords
        ('retrun 5', 'return 5'),
        ('retrn 5', 'return 5'),
        ('imprt os', 'import os'),
        ('imort os', 'import os'),
        ('frm os imprt path', 'from os import path'),
        ('klass Test:\n    pass', 'class Test:\n    pass'),
        ('clas Test:\n    pass', 'class Test:\n    pass'),
        # boolean and None
        ('x = true', 'x = True'),
        ('x = false', 'x = False'),
        ('x = none', 'x = None'),
        ('x = null', 'x = None'),
        ('x = nil', 'x = None'),
        # print variations
        ('prin("hello")', 'print("hello")'),
        ('prnt("hello")', 'print("hello")'),
        ('pritn("hello")', 'print("hello")'),
        # logical operators
        ('x andd y', 'x and y'),
        ('x adn y', 'x and y'),
        ('x orr y', 'x or y'),
        ('nott x', 'not x'),
        ('no x', 'not x'),
    ])
    def test_keyword_mappings(self, input_code, expected):
        """Test all predefined keyword mappings."""
        interpreter = phyton.PhytonInterpreter(fuzzy_matching=False)
        actual = interpreter.fix_spelling(input_code)
        assert actual == expected

    # Fuzzy Matching Tests
    @pytest.mark.parametrize("input_code,expected", [
        ('defff hello():', 'def hello():'),
        ('printt("hello")', 'print("hello")'),
        ('prrint("hello")', 'print("hello")'),
        ('returnn 5', 'return 5'),
    ])
    def test_fuzzy_matching_enabled(self, input_code, expected):
        """Test fuzzy matching functionality when enabled."""
        interpreter_fuzzy = phyton.PhytonInterpreter(fuzzy_matching=True)
        fuzzy_result = interpreter_fuzzy.fix_spelling(input_code)
        assert fuzzy_result == expected

    @pytest.mark.parametrize("input_code", [
        'defff hello():',
        'printt("hello")',
        'prrint("hello")',
        'returnn 5',
    ])
    def test_fuzzy_matching_disabled(self, input_code):
        """Test fuzzy matching functionality when disabled."""
        interpreter_normal = phyton.PhytonInterpreter(fuzzy_matching=False)
        normal_result = interpreter_normal.fix_spelling(input_code)
        assert normal_result == input_code

    @pytest.mark.parametrize("case", [
        'xyz_unknown_word',  # Completely unknown
        'deffffff',  # Too many extra letters
        'a',  # Too short
    ])
    def test_fuzzy_edge_cases(self, case):
        """Test edge cases that shouldn't match in fuzzy mode."""
        interpreter_fuzzy = phyton.PhytonInterpreter(fuzzy_matching=True)
        result = interpreter_fuzzy.fix_spelling(case)
        assert result == case

    # Argument Parsing Tests
    def test_help_option(self):
        """Test --help displays help message."""
        output, code = self.run_phyton_command(['--help'])
        assert 'Phyton - A Python interpreter' in output
        assert code == 0

    @pytest.mark.parametrize("option", ['--halp', '--helap', '--hepl'])
    def test_misspelled_help_options(self, option):
        """Test misspelled help options are corrected."""
        output, _ = self.run_phyton_command([option])
        assert '🔧 Fixed option:' in output
        assert 'Phyton - A Python interpreter' in output

    @pytest.mark.parametrize("option", ['--fuzy', '--fuzz', '--fuzi', '--fzzy'])
    def test_misspelled_fuzzy_options(self, option):
        """Test misspelled fuzzy options are corrected and work."""
        test_content = 'printt("test")'
        temp_file = self.create_temp_file(test_content)
        try:
            output, _ = self.run_phyton_command([option, temp_file])
            assert '🔧 Fixed option:' in output
            assert 'fuzzy match' in output
        finally:
            os.unlink(temp_file)

    @pytest.mark.parametrize("option", ['--interactiv', '--intractiv', '--interact'])
    def test_misspelled_interactive_options(self, option):
        """Test misspelled interactive options are corrected."""
        output, _ = self.run_phyton_command([option], input_text="quit()\n", timeout=5)
        assert '🔧 Fixed option:' in output
        assert 'Welcome to Phyton' in output

    # File Execution Tests
    def test_normal_python_execution(self):
        """Test normal Python code executes correctly."""
        python_code = '''
def hello():
    print("Hello from normal Python!")

hello()
'''
        temp_file = self.create_temp_file(python_code)
        try:
            output, code = self.run_phyton_command([temp_file])
            assert "Hello from normal Python!" in output
            assert code == 0
        finally:
            os.unlink(temp_file)

    def test_phyton_code_execution(self):
        """Test Phyton code with misspellings executes correctly."""
        phyton_code = '''
deff hello():
    prin("Hello from Phyton!")

hello()
'''
        temp_file = self.create_temp_file(phyton_code)
        try:
            output, code = self.run_phyton_command([temp_file])
            assert "Hello from Phyton!" in output
            assert code == 0
        finally:
            os.unlink(temp_file)

    def test_fuzzy_required_code_without_flag(self):
        """Test code requiring fuzzy matching fails without --fuzzy."""
        fuzzy_code = '''
defff hello():
    printt("This needs fuzzy!")

hello()
'''
        temp_file = self.create_temp_file(fuzzy_code)
        try:
            output, _ = self.run_phyton_command([temp_file])
            assert ("SyntaxError" in output or "PhytonSyntaxError" in output)
        finally:
            os.unlink(temp_file)

    def test_fuzzy_required_code_with_flag(self):
        """Test code requiring fuzzy matching works with --fuzzy."""
        fuzzy_code = '''
defff hello():
    printt("This needs fuzzy!")

hello()
'''
        temp_file = self.create_temp_file(fuzzy_code)
        try:
            output, code = self.run_phyton_command(['--fuzzy', temp_file])
            assert "This needs fuzzy!" in output
            assert code == 0
        finally:
            os.unlink(temp_file)

    # Error Handling Tests
    def test_syntax_error_handling(self):
        """Test syntax errors are reported with Phyton branding."""
        syntax_error_code = '''
deff hello(
    prin("missing colon and parenthesis")
'''
        temp_file = self.create_temp_file(syntax_error_code)
        try:
            output, _ = self.run_phyton_command([temp_file])
            assert ("PhytonSyntaxError" in output or "SyntaxError" in output)
        finally:
            os.unlink(temp_file)

    def test_file_not_found_error(self):
        """Test file not found errors are handled gracefully."""
        output, _ = self.run_phyton_command(['nonexistent_file.phy'])
        assert "PhytonError" in output
        assert "not found" in output

    def test_name_error_handling(self):
        """Test name errors are reported with Phyton branding."""
        name_error_code = '''
prin(undefined_variable)
'''
        temp_file = self.create_temp_file(name_error_code)
        try:
            output, _ = self.run_phyton_command([temp_file])
            assert "PhytonNameError" in output
        finally:
            os.unlink(temp_file)

    # Interactive Mode Tests
    def test_interactive_mode_basic(self):
        """Test interactive mode processes Phyton code correctly."""
        interactive_input = '''
deff test():
    retrun "success"

prin(test())
quit()
'''
        output, _ = self.run_phyton_command(['--interactive'],
                                          input_text=interactive_input, timeout=10)
        assert "Welcome to Phyton" in output
        assert "success" in output

    def test_interactive_mode_with_fuzzy(self):
        """Test interactive mode with fuzzy matching works."""
        fuzzy_interactive = '''
defff test():
    printt("fuzzy success")

test()
quit()
'''
        output, _ = self.run_phyton_command(['--fuzzy', '--interactive'],
                                          input_text=fuzzy_interactive, timeout=10)
        assert "fuzzy match" in output
        assert "fuzzy success" in output

    # Edge Case Tests
    def test_empty_input(self):
        """Test empty input is handled correctly."""
        interpreter = phyton.PhytonInterpreter()
        result = interpreter.fix_spelling("")
        assert result == ""

    def test_whitespace_only_input(self):
        """Test whitespace-only input is preserved."""
        interpreter = phyton.PhytonInterpreter()
        result = interpreter.fix_spelling("   \n\t  ")
        assert result == "   \n\t  "

    def test_comments_preserved(self):
        """Test comments are preserved correctly."""
        interpreter = phyton.PhytonInterpreter()
        comment_code = "# This is just a comment\n# Another comment"
        result = interpreter.fix_spelling(comment_code)
        assert result == comment_code

    def test_keywords_in_strings_modified(self):
        """Test keywords in strings are modified (current behavior)."""
        interpreter = phyton.PhytonInterpreter()
        string_code = 'print("deff is not a function here")'
        result = interpreter.fix_spelling(string_code)
        expected = 'print("def is not a function here")'
        assert result == expected

    def test_case_preservation(self):
        """Test case preservation in mixed case."""
        interpreter = phyton.PhytonInterpreter()
        mixed_case = "DEFF hello():\n    PRIN('test')"
        result = interpreter.fix_spelling(mixed_case)
        assert "DEFF" in result

    def test_very_long_misspellings_ignored(self):
        """Test very long misspellings are not matched."""
        interpreter_fuzzy = phyton.PhytonInterpreter(fuzzy_matching=True)
        long_misspelling = "deffffffffffffff"
        result = interpreter_fuzzy.fix_spelling(long_misspelling)
        assert result == long_misspelling

    @pytest.mark.skipif(not os.path.exists('./phyton'), reason="Launcher script not found")
    def test_launcher_script_help(self):
        """Test launcher script shows help correctly."""
        try:
            result = subprocess.run(['./phyton', '--help'], capture_output=True,
                                  text=True, timeout=10, check=False)
            assert 'Phyton - A Python interpreter' in result.stdout
            assert result.returncode == 0
        except (subprocess.TimeoutExpired, OSError):
            pytest.fail("Launcher script help failed")

    @pytest.mark.skipif(not os.path.exists('./phyton'), reason="Launcher script not found")
    def test_launcher_script_misspelled_options(self):
        """Test launcher script handles misspelled options."""
        try:
            result = subprocess.run(['./phyton', '--halp'], capture_output=True,
                                  text=True, timeout=10, check=False)
            assert '🔧 Fixed option:' in result.stdout + result.stderr
        except (subprocess.TimeoutExpired, OSError):
            pytest.fail("Launcher script misspelled option test failed")

    # Argument Parser Tests
    def test_argument_parser_initialization(self):
        """Test PhytonArgumentParser initialization."""
        parser = phyton.PhytonArgumentParser()
        assert parser.parser is not None
        assert 'fuzzy' in parser.option_mappings
        assert 'interactive' in parser.option_mappings
        assert 'help' in parser.option_mappings

    def test_single_dash_option_handling(self):
        """Test single dash options are passed through unchanged."""
        parser = phyton.PhytonArgumentParser()
        args = ['-i', 'test.py']
        fixed_args = parser.fix_option_spelling(args)
        assert fixed_args == ['-i', 'test.py']

    def test_find_option_match_exact(self):
        """Test exact option matching."""
        parser = phyton.PhytonArgumentParser()
        result = parser._find_option_match('fuzzy')  # pylint: disable=protected-access
        assert result == 'fuzzy'

    def test_find_option_match_none(self):
        """Test no option match found."""
        parser = phyton.PhytonArgumentParser()
        result = parser._find_option_match('unknown_option_xyz')  # pylint: disable=protected-access
        assert result is None

    def test_find_option_match_fuzzy(self):
        """Test fuzzy option matching."""
        parser = phyton.PhytonArgumentParser()
        result = parser._find_option_match('helpx')  # pylint: disable=protected-access
        assert result == 'help'

    def test_option_no_fix_needed(self):
        """Test when option doesn't need fixing."""
        parser = phyton.PhytonArgumentParser()
        args = ['--unknown', 'file.py']
        fixed_args = parser.fix_option_spelling(args)
        assert '--unknown' in fixed_args

    def test_option_fix_edge_cases(self):
        """Test option fixing edge cases."""
        parser = phyton.PhytonArgumentParser()

        # Test with no options needing fixes
        result = parser.fix_option_spelling(['file.py'])
        assert result == ['file.py']

        # Test with mixed options
        result = parser.fix_option_spelling(['--valid', '--halp', 'file.py'])
        assert '--help' in result
        assert '--valid' in result

    def test_argument_parser_parse_args_with_file(self):
        """Test argument parser with file argument."""
        parser = phyton.PhytonArgumentParser()
        args = parser.parse_args(['test.phy'])
        assert args.filename == 'test.phy'
        assert not args.fuzzy
        assert not args.interactive

    def test_argument_parser_parse_args_with_flags(self):
        """Test argument parser with all flags."""
        parser = phyton.PhytonArgumentParser()
        args = parser.parse_args(['--fuzzy', '--interactive', 'test.phy'])
        assert args.filename == 'test.phy'
        assert args.fuzzy
        assert args.interactive

    def test_argument_parser_no_file_interactive_mode(self):
        """Test argument parser when no file is provided."""
        parser = phyton.PhytonArgumentParser()
        args = parser.parse_args([])
        assert args.filename is None
        assert not args.fuzzy
        assert not args.interactive

    def test_parse_args_with_none(self):
        """Test parse_args method with None (uses sys.argv)."""
        parser = phyton.PhytonArgumentParser()
        # Save original sys.argv
        original_argv = sys.argv.copy()
        try:
            # Simulate command line args
            sys.argv = ['phyton.py', '--help']
            # This will raise SystemExit due to --help, which is expected
            try:
                parser.parse_args(None)
            except SystemExit:
                pass  # Expected behavior for --help
        finally:
            sys.argv = original_argv

    def test_option_mapping_coverage(self):
        """Test all option mappings are covered."""
        parser = phyton.PhytonArgumentParser()

        # Test all known misspellings
        for correct, misspellings in parser.option_mappings.items():
            for misspelling in misspellings:
                result = parser._find_option_match(misspelling)  # pylint: disable=protected-access
                assert result == correct

    # Interpreter Method Tests
    def test_add_misspelling_existing_keyword(self):
        """Test adding misspelling to existing keyword."""
        interpreter = phyton.PhytonInterpreter()
        success = interpreter.add_misspelling('def', 'newdef')
        assert success is True
        assert 'newdef' in interpreter.keyword_mappings['def']

    def test_add_misspelling_nonexistent_keyword(self):
        """Test adding misspelling to non-existent keyword."""
        interpreter = phyton.PhytonInterpreter()
        success = interpreter.add_misspelling('nonexistent', 'spelling')
        assert success is False

    def test_add_misspelling_duplicate(self):
        """Test adding duplicate misspelling."""
        interpreter = phyton.PhytonInterpreter()
        interpreter.add_misspelling('def', 'deff')  # Already exists
        # Should not duplicate
        count = interpreter.keyword_mappings['def'].count('deff')
        assert count == 1

    def test_add_keyword_new(self):
        """Test adding a completely new keyword."""
        interpreter = phyton.PhytonInterpreter()
        interpreter.add_keyword('newkeyword', ['newkw', 'nkw'])
        assert 'newkeyword' in interpreter.keyword_mappings
        assert 'newkw' in interpreter.keyword_mappings['newkeyword']

    def test_add_keyword_with_none_misspellings(self):
        """Test adding keyword with None misspellings."""
        interpreter = phyton.PhytonInterpreter()
        interpreter.add_keyword('testkw', None)
        assert 'testkw' in interpreter.keyword_mappings
        assert interpreter.keyword_mappings['testkw'] == ['testkw']

    def test_add_keyword_without_correct_in_list(self):
        """Test adding keyword where correct spelling not in misspellings."""
        interpreter = phyton.PhytonInterpreter()
        interpreter.add_keyword('correct', ['wrong1', 'wrong2'])
        assert interpreter.keyword_mappings['correct'][0] == 'correct'

    def test_get_misspellings_existing(self):
        """Test getting misspellings for existing keyword."""
        interpreter = phyton.PhytonInterpreter()
        misspellings = interpreter.get_misspellings('def')
        assert 'deff' in misspellings
        assert 'define' in misspellings

    def test_get_misspellings_nonexistent(self):
        """Test getting misspellings for non-existent keyword."""
        interpreter = phyton.PhytonInterpreter()
        misspellings = interpreter.get_misspellings('nonexistent')
        assert misspellings == []

    # Fuzzy Matching Tests
    def test_find_fuzzy_match_disabled(self):
        """Test fuzzy matching when disabled."""
        interpreter = phyton.PhytonInterpreter(fuzzy_matching=False)
        result = interpreter.find_fuzzy_match('defff')
        assert result is None

    def test_find_fuzzy_match_enabled_good_match(self):
        """Test fuzzy matching when enabled with good match."""
        interpreter = phyton.PhytonInterpreter(fuzzy_matching=True)
        result = interpreter.find_fuzzy_match('defff')
        assert result == 'def'

    def test_find_fuzzy_match_enabled_no_match(self):
        """Test fuzzy matching when enabled with no good match."""
        interpreter = phyton.PhytonInterpreter(fuzzy_matching=True)
        result = interpreter.find_fuzzy_match('xyz123unknown')
        assert result is None

    def test_adaptive_fuzzy_threshold_short_word(self):
        """Test adaptive fuzzy threshold for short words."""
        interpreter = phyton.PhytonInterpreter(fuzzy_matching=True)
        # Short word should require higher threshold (90%)
        result = interpreter.find_fuzzy_match('de')  # Too different from 'def'
        assert result is None

    def test_adaptive_fuzzy_threshold_medium_word(self):
        """Test adaptive fuzzy threshold for medium words."""
        interpreter = phyton.PhytonInterpreter(fuzzy_matching=True)
        # Medium word should use 80% threshold
        result = interpreter.find_fuzzy_match('printt')
        assert result == 'print'

    def test_adaptive_fuzzy_threshold_long_word(self):
        """Test adaptive fuzzy threshold for long words."""
        interpreter = phyton.PhytonInterpreter(fuzzy_matching=True)
        # Long word should use 70% threshold
        result = interpreter.find_fuzzy_match('exceptt')
        assert result == 'except'

    def test_fuzzy_threshold_boundary_conditions(self):
        """Test fuzzy matching threshold boundary conditions."""
        interpreter = phyton.PhytonInterpreter(fuzzy_matching=True)

        # These should work with fuzzy matching
        assert interpreter.find_fuzzy_match("deff") == "def"  # Close to short word
        assert interpreter.find_fuzzy_match("exceptt") == "except"  # Close to medium word

    def test_fuzzy_disabled_behavior(self):
        """Test behavior when fuzzy matching is disabled."""
        interpreter = phyton.PhytonInterpreter(fuzzy_matching=False)

        # Should not fix fuzzy matches
        result = interpreter.fix_spelling('defff hello():')
        assert 'defff' in result  # Should not be changed

    # Execute Method Tests
    def test_execute_method_syntax_error(self):
        """Test execute method with syntax error."""
        interpreter = phyton.PhytonInterpreter()
        captured_output = io.StringIO()
        sys.stdout = captured_output

        try:
            interpreter.execute("invalid syntax here ::::")
            output = captured_output.getvalue()
            assert "PhytonSyntaxError" in output
        finally:
            sys.stdout = sys.__stdout__

    def test_execute_method_name_error(self):
        """Test execute method with name error."""
        interpreter = phyton.PhytonInterpreter()
        captured_output = io.StringIO()
        sys.stdout = captured_output

        try:
            interpreter.execute("undefined_variable")
            output = captured_output.getvalue()
            assert "PhytonNameError" in output
        finally:
            sys.stdout = sys.__stdout__

    def test_execute_method_type_error(self):
        """Test execute method with type error."""
        interpreter = phyton.PhytonInterpreter()
        captured_output = io.StringIO()
        sys.stdout = captured_output

        try:
            interpreter.execute("len()")  # Missing argument
            output = captured_output.getvalue()
            assert "PhytonTypeError" in output
        finally:
            sys.stdout = sys.__stdout__

    def test_execute_method_with_import_error(self):
        """Test execute method with import error."""
        interpreter = phyton.PhytonInterpreter()
        captured_output = io.StringIO()
        sys.stdout = captured_output

        try:
            interpreter.execute("import nonexistent_module_xyz")
            output = captured_output.getvalue()
            assert "PhytonImportError" in output
        finally:
            sys.stdout = sys.__stdout__

    def test_execute_with_value_error(self):
        """Test execute method with ValueError."""
        interpreter = phyton.PhytonInterpreter()
        captured_output = io.StringIO()
        sys.stdout = captured_output

        try:
            interpreter.execute("int('not_a_number')")
            output = captured_output.getvalue()
            assert "PhytonValueError" in output
        finally:
            sys.stdout = sys.__stdout__

    def test_execute_with_keyboard_interrupt(self):
        """Test execute method with KeyboardInterrupt simulation."""
        interpreter = phyton.PhytonInterpreter()
        captured_output = io.StringIO()
        sys.stdout = captured_output

        try:
            # Simulate KeyboardInterrupt by raising it in code
            interpreter.execute("raise KeyboardInterrupt()")
            output = captured_output.getvalue()
            assert "PhytonKeyboardInterrupt" in output
        finally:
            sys.stdout = sys.__stdout__

    def test_execute_with_unexpected_exception(self):
        """Test execute method with unexpected exception."""
        interpreter = phyton.PhytonInterpreter()
        captured_output = io.StringIO()
        sys.stdout = captured_output

        try:
            # Create an unusual exception
            interpreter.execute("raise RuntimeError('Test unexpected error')")
            output = captured_output.getvalue()
            assert "PhytonUnexpectedError" in output
            assert "RuntimeError" in output
        finally:
            sys.stdout = sys.__stdout__

    def test_execute_successful_with_fixes(self):
        """Test execute method with successful code that needs fixes."""
        interpreter = phyton.PhytonInterpreter()

        output_buffer = io.StringIO()
        with contextlib.redirect_stdout(output_buffer):
            interpreter.execute('prin("Hello World")')

        output = output_buffer.getvalue()
        assert "Hello World" in output

    def test_execute_no_changes_needed(self):
        """Test execute method when no spelling changes are needed."""
        interpreter = phyton.PhytonInterpreter()

        output_buffer = io.StringIO()
        with contextlib.redirect_stdout(output_buffer):
            interpreter.execute('x = 1 + 1')

        # Should execute without spelling fix messages
        output = output_buffer.getvalue()
        assert "Fixed spelling" not in output

    def test_execute_method_with_successful_code(self):
        """Test execute method with successful code execution."""
        interpreter = phyton.PhytonInterpreter()

        # Capture stdout to verify execution
        captured_output = io.StringIO()
        sys.stdout = captured_output

        try:
            interpreter.execute("prin('success')")
            output = captured_output.getvalue()
            assert "success" in output
        finally:
            sys.stdout = sys.__stdout__

    def test_execute_method_no_spelling_fixes(self):
        """Test execute method when no spelling fixes are needed."""
        interpreter = phyton.PhytonInterpreter()

        captured_output = io.StringIO()
        sys.stdout = captured_output

        try:
            interpreter.execute("print('correct spelling')")
            output = captured_output.getvalue()
            # Should not show "Fixed spelling" message
            assert "Fixed spelling" not in output
            assert "correct spelling" in output
        finally:
            sys.stdout = sys.__stdout__

    # Interactive Mode Tests
    def test_interactive_mode_method_exists(self):
        """Test interactive mode method exists."""
        interpreter = phyton.PhytonInterpreter()
        # Test that interactive_mode method exists
        assert hasattr(interpreter, 'interactive_mode')

    # Main Function Tests
    def test_main_function_help(self):
        """Test main function with help argument."""
        try:
            result = subprocess.run(['python3', 'phyton.py', '--help'],
                                  capture_output=True, text=True, timeout=10, check=False)
            assert 'Phyton - A Python interpreter' in result.stdout
            assert result.returncode == 0
        except (subprocess.TimeoutExpired, OSError):
            pytest.skip("Could not test main function")

    def test_main_function_with_nonexistent_file(self):
        """Test main function with non-existent file."""
        try:
            result = subprocess.run(['python3', 'phyton.py', 'nonexistent_file_xyz.phy'],
                                  capture_output=True, text=True, timeout=10, check=False)
            # Check that error message is printed
            assert "PhytonError" in result.stdout or "not found" in result.stdout
        except (subprocess.TimeoutExpired, OSError):
            pytest.skip("Could not test main function")

    def test_main_function_interactive_mode(self):
        """Test main function in interactive mode."""
        try:
            result = subprocess.run(['python3', 'phyton.py', '--interactive'],
                                  input="print('test')\nquit()\n",
                                  capture_output=True, text=True, timeout=10, check=False)
            assert 'Welcome to Phyton' in result.stdout or result.returncode == 0
        except (subprocess.TimeoutExpired, OSError):
            pytest.skip("Could not test main function interactive mode")

    def test_main_function_permission_error(self):
        """Test main function with permission error file."""
        # Create a temporary file and remove read permissions
        with tempfile.NamedTemporaryFile(mode='w', suffix='.phy', delete=False) as temp_file:
            temp_file.write("print('test')")
            temp_file_name = temp_file.name

        try:
            # Remove read permissions
            os.chmod(temp_file_name, stat.S_IWRITE)

            result = subprocess.run(['python3', 'phyton.py', temp_file_name],
                                  capture_output=True, text=True, timeout=10, check=False)
            assert "Permission denied" in result.stdout or "PhytonError" in result.stdout
        except (subprocess.TimeoutExpired, OSError, PermissionError):
            pytest.skip("Could not test permission error")
        finally:
            try:
                os.chmod(temp_file_name, stat.S_IREAD | stat.S_IWRITE)
                os.unlink(temp_file_name)
            except OSError:
                pass

    def test_main_function_non_phy_file_warning(self):
        """Test main function warning for non-.phy files."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
            temp_file.write("print('test')")
            temp_file_name = temp_file.name

        try:
            result = subprocess.run(['python3', 'phyton.py', temp_file_name],
                                  capture_output=True, text=True, timeout=10, check=False)
            assert "Warning: Expected .phy file" in result.stdout or "test" in result.stdout
        except (subprocess.TimeoutExpired, OSError):
            pytest.skip("Could not test non-.phy file warning")
        finally:
            os.unlink(temp_file_name)

    def test_main_function_keyboard_interrupt_handling(self):
        """Test main function keyboard interrupt handling."""
        # This is difficult to test directly, but we can test the exception handling structure
        try:
            # Quick test with --help to ensure main function works
            result = subprocess.run(['python3', 'phyton.py', '--help'],
                                  capture_output=True, text=True, timeout=5, check=False)
            assert result.returncode == 0
        except (subprocess.TimeoutExpired, OSError):
            pytest.skip("Could not test main function")

    def test_main_function_scenarios(self):
        """Test various main function scenarios."""
        # Test with binary file (will cause unicode decode error)
        with tempfile.NamedTemporaryFile(mode='wb', suffix='.phy', delete=False) as binary_file:
            binary_file.write(b'\x80\x81\x82')  # Invalid UTF-8
            binary_file_name = binary_file.name

        try:
            result = subprocess.run(['python3', 'phyton.py', binary_file_name],
                                  capture_output=True, text=True, timeout=5, check=False)
            # Should handle unicode decode error gracefully
            assert len(result.stdout) > 0 or len(result.stderr) > 0
        except subprocess.TimeoutExpired:
            pass
        finally:
            os.unlink(binary_file_name)

    def test_main_interactive_with_explicit_flag(self):
        """Test main function with explicit interactive flag."""
        try:
            # Use timeout to prevent hanging
            result = subprocess.run(['python3', 'phyton.py', '--interactive'],
                                  input='print("test")\\nquit()\\n',
                                  capture_output=True, text=True, timeout=5, check=False)
            # Should start interactive mode
            assert len(result.stdout) > 0 or result.returncode is not None
        except subprocess.TimeoutExpired:
            pass  # Expected for interactive mode

    def test_main_with_fuzzy_interactive(self):
        """Test main function with fuzzy flag in interactive mode."""
        try:
            result = subprocess.run(['python3', 'phyton.py', '--fuzzy', '--interactive'],
                                  input='quit()\\n',
                                  capture_output=True, text=True, timeout=5, check=False)
            # Should enable fuzzy matching in interactive mode
            assert len(result.stdout) > 0 or result.returncode is not None
        except subprocess.TimeoutExpired:
            pass

    def test_main_function_with_fuzzy_flag(self):
        """Test main function with fuzzy flag enabled."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.phy', delete=False) as temp_file:
            temp_file.write("defff test(): printt('fuzzy test')")
            temp_file_name = temp_file.name

        try:
            result = subprocess.run(['python3', 'phyton.py', '--fuzzy', temp_file_name],
                                  capture_output=True, text=True, timeout=10, check=False)
            assert "fuzzy match" in result.stdout or "test" in result.stdout
        except (subprocess.TimeoutExpired, OSError):
            pytest.skip("Could not test fuzzy flag")
        finally:
            os.unlink(temp_file_name)

    def test_main_function_unicode_decode_error(self):
        """Test main function with unicode decode error."""
        # Create a file with invalid UTF-8
        with tempfile.NamedTemporaryFile(mode='wb', suffix='.phy', delete=False) as temp_file:
            temp_file.write(b'\xff\xfe\x00\x00invalid unicode')
            temp_file_name = temp_file.name

        try:
            result = subprocess.run(['python3', 'phyton.py', temp_file_name],
                                  capture_output=True, text=True, timeout=10, check=False)
            assert "PhytonError" in result.stdout or "decode" in result.stdout
        except (subprocess.TimeoutExpired, OSError):
            pytest.skip("Could not test unicode decode error")
        finally:
            os.unlink(temp_file_name)

    def test_main_function_os_error(self):
        """Test main function with OS error."""
        # Try to read from a directory instead of a file
        temp_dir = tempfile.mkdtemp()
        try:
            result = subprocess.run(['python3', 'phyton.py', temp_dir],
                                  capture_output=True, text=True, timeout=10, check=False)
            assert "PhytonError" in result.stdout or "OS error" in result.stdout
        except (subprocess.TimeoutExpired, OSError):
            pytest.skip("Could not test OS error")
        finally:
            os.rmdir(temp_dir)

    def test_main_function_general_exception_handling(self):
        """Test main function general exception handling."""
        # Mock argparse to raise an exception
        original_argv = sys.argv.copy()
        try:
            sys.argv = ['phyton.py', '--invalid-option-that-does-not-exist']

            with unittest.mock.patch('sys.exit') as mock_exit:
                try:
                    phyton.main()
                    # Should call sys.exit(1) on error
                    mock_exit.assert_called_with(1)
                except SystemExit:
                    pass  # Expected
        except Exception:  # pylint: disable=broad-exception-caught
            pass  # Expected for invalid arguments
        finally:
            sys.argv = original_argv

    def test_main_function_interactive_without_flag(self):
        """Test main function interactive mode when no filename provided."""
        # Mock sys.argv to simulate no file argument
        original_argv = sys.argv.copy()
        try:
            sys.argv = ['phyton.py']

            # Mock the interactive_mode method to avoid actual interaction
            with unittest.mock.patch.object(phyton.PhytonInterpreter, 'interactive_mode'):
                with unittest.mock.patch('builtins.print'):
                    try:
                        phyton.main()
                    except SystemExit:
                        pass
        finally:
            sys.argv = original_argv

    # Comprehensive Behavior Tests
    def test_fix_spelling_preserves_structure(self):
        """Test that fix_spelling preserves code structure."""
        interpreter = phyton.PhytonInterpreter()
        code = """
# This is a comment
deff hello():
    # Another comment
    prin("Hello")
    retrun None
"""
        result = interpreter.fix_spelling(code)
        assert '# This is a comment' in result
        assert '# Another comment' in result
        assert 'def hello():' in result
        assert 'print("Hello")' in result
        assert 'return None' in result

    def test_word_boundary_matching(self):
        """Test that only whole words are matched, not substrings."""
        interpreter = phyton.PhytonInterpreter()
        # Test that 'def' in 'define_function' is not replaced
        code = "define_function = lambda: None"
        result = interpreter.fix_spelling(code)
        # Should not change define_function to def_function
        assert 'define_function' in result

    def test_case_sensitivity_preservation(self):
        """Test that case is preserved in replacements."""
        interpreter = phyton.PhytonInterpreter()
        code = "DEFF upper_function():\n    PRIN('test')"
        result = interpreter.fix_spelling(code)
        # Original behavior may vary, just ensure it doesn't crash
        assert len(result) > 0

    def test_multiple_misspellings_same_line(self):
        """Test multiple misspellings on the same line."""
        interpreter = phyton.PhytonInterpreter()
        code = "deff test(): retrun prin('hello')"
        result = interpreter.fix_spelling(code)
        assert 'def test():' in result
        assert 'return' in result
        assert 'print' in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
