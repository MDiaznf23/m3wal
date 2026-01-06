# M3WAL

> Material 3 Wallpaper-based Color Scheme Generator

Generate beautiful Material 3 color schemes from your wallpapers and apply them system-wide to your Linux desktop.

## Features

- Extract Material 3 color schemes from any wallpaper
- Auto-detect light/dark mode based on wallpaper brightness
- 7 Material Color Variants (Content, Vibrant, Expressive, etc.)
- Export to multiple formats (JSON, CSS, SCSS, Xresources, etc.)
- Template system for custom config generation
- Automatic wallpaper setting with `feh`
- Deploy configs to multiple applications automatically

## Installation

### From PyPI (Coming Soon)

```bash
pip install m3wal
```

### From Source

```bash
git clone https://github.com/MDiaznf23/m3wal.git
cd m3wal
pip install -e .
```

### Dependencies

```bash
pip install material-color-utilities Pillow
```

**Optional system dependencies:**
- `feh` - for setting wallpapers
- `xrdb` - for applying Xresources

## Quick Start

```bash
# Basic usage (auto-detect mode)
m3wal /path/to/wallpaper.jpg

# Specify mode
m3wal wallpaper.jpg dark

# Choose variant
m3wal wallpaper.jpg dark VIBRANT
```

## Usage

### Command Line

```bash
m3wal <wallpaper_path> [light|dark|auto] [variant]
```

**Variants:**
- `CONTENT` (default) - Based on wallpaper content
- `VIBRANT` - More saturated colors
- `EXPRESSIVE` - Maximum chroma
- `NEUTRAL` - Subdued, neutral colors
- `TONALSPOT` - Single accent color
- `FIDELITY` - Closest to source color
- `MONOCHROME` - Grayscale palette

### Configuration

Config file: `~/.config/m3-colors/m3-colors.conf`

```ini
[General]
mode = auto
variant = CONTENT
brightness_threshold = 128

[Paths]
templates_dir = templates
cache_dir = ~/.cache/m3-colors
config_dir = ~/.config/m3-colors

[Features]
set_wallpaper = true
apply_xresources = true
generate_palette_preview = true
run_post_script = true
create_symlink = true

[PostScript]
script_path = m3wal-post.sh
```

### Templates

Create custom templates in `~/.config/m3-colors/templates/`

**Example template** (`myapp.conf.template`):

```
background={{m3surface}}
foreground={{m3onSurface}}
primary={{m3primary}}
accent={{m3secondary}}
```

Available color variables:
- Material 3: `m3primary`, `m3secondary`, `m3tertiary`, `m3surface`, `m3error`, etc.
- Terminal: `term0` to `term15`
- Metadata: `wallpaper_path`, `mode`, `source_color`

### Deployment

Configure deployment in `~/.config/m3-colors/deploy.json`:

```json
{
  "deployments": [
    {
      "source": "colors-nvim.lua",
      "destination": "~/.config/nvim/lua/themes/material3.lua"
    },
    {
      "source": "kitty.conf",
      "destination": "~/.config/kitty/colors.conf"
    }
  ]
}
```

### Post Script

Add custom actions in `~/.config/m3-colors/m3wal-post.sh`:

```bash
#!/bin/bash
# Reload applications
killall -USR1 kitty
i3-msg reload
```

## Output Files

Generated files in `~/.cache/m3-colors/`:

- `colors.json` - Full color scheme
- `colors.Xresources` - X11 colors
- `colors.css` / `colors.scss` - Web stylesheets
- `colors.sh` - Shell script
- `kitty.conf`, `alacritty.toml` - Terminal configs
- `rofi.rasi` - Rofi theme
- And more...

## Supported Applications

Out of the box templates for:

- **Terminals:** Kitty, Alacritty, TTY
- **WM/DE:** i3, Polybar, Waybar, Dunst
- **Editors:** Neovim, Zathura
- **Launchers:** Rofi
- **Music:** RMPC
- **Themes:** GTK 2/3/4

## Python API

```python
from m3wal import M3WAL

# Initialize
m3 = M3WAL("wallpaper.jpg")

# Analyze wallpaper
analysis = m3.analyze_wallpaper()

# Generate scheme
colors = m3.generate_scheme(mode="dark", variant="VIBRANT")

# Export JSON
m3.export_json("output.json")

# Apply templates
m3.apply_all_templates()

# Generate preview
m3.generate_palette_preview()
```

## Examples

```bash
# Auto mode with content variant
m3wal ~/Pictures/sunset.jpg

# Force dark mode with vibrant colors
m3wal ~/Pictures/landscape.jpg dark VIBRANT

# Light mode with expressive variant
m3wal ~/Pictures/abstract.jpg light EXPRESSIVE
```

## How It Works

1. **Analyze** wallpaper brightness to determine light/dark mode
2. **Extract** dominant colors using Material Color Utilities
3. **Generate** complete Material 3 color scheme
4. **Apply** colors to all templates
5. **Deploy** configs to target applications
6. **Set** wallpaper and reload applications

## Contributing

Contributions welcome! Please feel free to submit a Pull Request.

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Credits

Built with [material-color-utilities](https://github.com/material-foundation/material-color-utilities) by Google.

## Links

- GitHub: https://github.com/MDiaznf23/m3wal
- PyPI: https://pypi.org/project/m3wal/
- Issues: https://github.com/MDiaznf23/m3wal/issues
