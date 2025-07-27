# Phyton 🌱

**Phyton** (Greek for "plant") - A Python interpreter that accepts multiple spellings of keywords, designed to confuse bad spellers!

![Phyton](phyton.gif)

## Features

- Accepts common misspellings of Python keywords
- Interactive REPL mode
- File execution mode
- Friendly error messages
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
# Using Python directly
python3 phyton.py examples/quick_start.phy

# Using the launcher script (recommended)
./phyton examples/quick_start.phy
```

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
