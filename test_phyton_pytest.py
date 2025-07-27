#!/usr/bin/env python3
"""
Pytest-compatible test suite for all Phyton features.
Tests keyword mapping, fuzzy matching, argument parsing, and error handling.
"""

import subprocess
import os
import tempfile
import pytest
import phyton


class TestPhytonFeatures:  # pylint: disable=too-many-public-methods
    """Pytest test class for Phyton features."""

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
        except OSError as e:
            return f"ERROR: {e}", -1

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


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
