# Phyton 🌱

**Phyton** (Greek for "plant") - A Python interpreter that accepts multiple spellings of keywords, designed to confuse bad spellers!

> Inspired by a [suggestion](https://www.linkedin.com/posts/mcovington_somebody-needs-to-invent-a-programming-language-activity-7354669004201893888-7tGV?utm_source=share&utm_medium=member_desktop&rcm=ACoAAAUp-sQBFZ55uKVqPbQV7WNOA1YRQW831JI) from Michael Covington.

![Phyton](phyton.gif)

## Features

- Accepts common misspellings of Python keywords
- Interactive REPL mode
- File execution mode
- Friendly error messages
- Fuzzy matching for unknown misspellings (optional)
- Supports creative variations like `prin` for `print`, `deff` for `def`, etc.

## Supported Misspellings

### Keywords

- `def` → `deff`, `define`, `defin`
- `if` → `iff`, `iif`
- `elif` → `elsif`, `elseif`, `else_if`
- `else` → `els`, `elze`
- `for` → `fore`, `four`, `fr`
- `while` → `wile`, `whyle`, `whil`
- `in` → `inn`, `iin`
- `return` → `retrun`, `retrn`, `ret`
- `import` → `imprt`, `imort`, `importt`
- `from` → `frm`, `fom`
- `as` → `az`, `ass`
- `class` → `clas`, `clss`, `klass`
- `try` → `tri`, `tyr`
- `except` → `exept`, `excpt`, `catch`
- `finally` → `finaly`, `finale`
- `with` → `wth`, `wit`
- `and` → `andd`, `adn`, `&`
- `or` → `orr`, `|`
- `not` → `nott`, `no`, `!`

### Built-ins

- `True` → `true`, `TRUE`, `tru`
- `False` → `false`, `FALSE`, `fals`
- `None` → `none`, `NONE`, `null`, `nil`
- `print` → `prin`, `prnt`, `pritn`

## Usage

### Interactive Mode

```bash
# Using Python directly
python3 phyton.py

# Using the launcher script
./phyton
```

### File Execution

```bash
# Using Python directly (fuzzy matching disabled by default)
python3 phyton.py examples/quick_start.phy

# Using the launcher script (recommended)
./phyton examples/quick_start.phy

# Enable fuzzy matching for unknown misspellings
python3 phyton.py --fuzzy examples/quick_start.phy
./phyton --fuzzy examples/quick_start.phy
```

### Command Line Options

Phyton accepts misspelled command line options too! Try these:

```bash
# These all work thanks to option misspelling correction:
./phyton --halp                    # → --help
./phyton --fuzy file.phy           # → --fuzzy  
./phyton --interactiv              # → --interactive
```

### Fuzzy Matching

Phyton includes **fuzzy matching** that can correct unknown misspellings not in the predefined dictionary:

```bash
# Default behavior - fuzzy matching disabled
python3 phyton.py your_file.phy

# Enable fuzzy matching for unknown misspellings
python3 phyton.py --fuzzy your_file.phy

# Interactive mode (fuzzy disabled by default)
python3 phyton.py --interactive
```

**Examples of fuzzy corrections:**
- `defff` → `def`
- `printt` → `print` 
- `prrint` → `print`

⚡ **Note:** Fuzzy matching is disabled by default for predictable behavior. Use `--fuzzy` to enable advanced spelling correction.

## Examples

All example files are located in the `examples/` folder with memorable names:

- **`quick_start.phy`** - Perfect first Phyton program
- **`hello_world.phy`** - Classic programming with misspellings  
- **`spelling_game.phy`** - Interactive spelling game
- **`advanced_features.phy`** - Complex programming constructs
- **`bad_spellers_paradise.phy`** - Maximum misspelling density
- **`spelling_nightmare.phy`** - Ultimate stress test

See `examples/README.md` for detailed descriptions and learning path.

## Examples

### Quick Start Example

```python
# This is valid Phyton code!
deff greet(name):
    prin(f"Hello, {name}!")

iff name == "World":
    greet("Phyton")
els:
    greet("Python")
```

### Advanced Example

```python
klass Plant:
    deff __init__(self, species):
        self.species = species
    
    deff grow(self):
        retrun f"{self.species} is growing! 🌿"

fore i inn range(3):
    plant = Plant(f"Plant {i}")
    prin(plant.grow())
```

For more examples, see the `examples/` folder!

## Quick Start

1. **Try the demo:** `./demo.sh` - Runs all 6 examples
2. **Start simple:** `./phyton examples/quick_start.phy`
3. **Go interactive:** `./phyton` for REPL mode
4. **Explore:** Check `examples/README.md` for learning path

## File Extensions

While Phyton can execute any `.py` file, we recommend using `.phy` extension for Phyton files to distinguish them from regular Python files.

## Contributing

Feel free to add more creative misspellings! The goal is to accept as many common typos and variations as possible while still being functional.

## Why?

Because everyone deserves to code, even if they can't spell "def" correctly! 🌱
