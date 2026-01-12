# M3WAL

> Material 3 Wallpaper-based Color Scheme Generator

Generate beautiful Material 3 color schemes from your wallpapers and apply them system-wide to your Linux desktop.

## Features

- Extract Material 3 color schemes from any wallpaper
- Auto-detect light/dark mode based on wallpaper brightness
- 7 Material Color Variants (Content, Vibrant, Expressive, etc.)
- Export to multiple formats (JSON, CSS)
- Template system for custom config generation
- **Two operation modes:** Generator-only or Full ricing mode
- Automatic wallpaper setting with `feh`
- Deploy configs to multiple applications automatically
- **Parallel template processing** for faster execution
- **RGB color format support** for KDE and other applications
- **Hook scripts system** for custom actions
- **Improved terminal color contrast** for light mode
- **GTK theme reloading** via gsettings and xsettingsd

## Installation

### From PyPI 

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
- `xsettingsd` - for GTK theme reloading
- `gsettings` - for GNOME/GTK theme management

## Quick Start

```bash
# Basic usage (auto-detect mode, uses config default)
m3wal /path/to/wallpaper.jpg

# Generator-only mode (no system changes)
m3wal wallpaper.jpg --generator-only

# Full mode (apply all configurations)
m3wal wallpaper.jpg --full

# Specify mode and variant
m3wal wallpaper.jpg --mode dark --variant VIBRANT
```

## Usage

### Command Line

```bash
m3wal <wallpaper_path> [options]
```

**Options:**

| Option | Short | Description |
|--------|-------|-------------|
| `--mode` | `-m` | Color scheme mode: `light`, `dark`, or `auto` |
| `--variant` | `-v` | Material 3 variant (see below) |
| `--generator-only` | `-g` | Only generate colors, skip ricing |
| `--full` | `-f` | Apply all configurations (ricing mode) |

**Variants:**
- `CONTENT` (default) - Based on wallpaper content
- `VIBRANT` - More saturated colors
- `EXPRESSIVE` - Maximum chroma
- `NEUTRAL` - Subdued, neutral colors
- `TONALSPOT` - Single accent color
- `FIDELITY` - Closest to source color
- `MONOCHROME` - Grayscale palette

### Operation Modes

M3WAL now supports two operation modes:

#### 1. Generator Mode (`--generator-only` or `-g`)
Only generates color schemes without applying them to your system:
- Analyzes wallpaper
- Generates color scheme
- Exports JSON and CSS files
- Creates palette preview
- **No system modifications**

Perfect for:
- Testing color schemes
- Generating colors for manual use
- CI/CD pipelines
- Color scheme preview

#### 2. Full Mode (`--full` or `-f`)
Generates colors AND applies them system-wide:
- All generator mode features
- Applies colors to all templates
- Deploys configs to applications
- Reloads GTK themes
- Runs hook scripts
- Applies Xresources
- Sets wallpaper with feh
- Creates wallpaper symlink
- Runs post scripts

Perfect for:
- Complete rice setup
- Automatic theming
- Daily wallpaper changes

### Configuration

Config file: `~/.config/m3-colors/m3-colors.conf`

```ini
[General]
mode = auto
variant = CONTENT
brightness_threshold = 128
operation_mode = full  # 'generator' or 'full'

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

[Hook.Scripts]
enabled = true
scripts = reload-apps.sh, notify.sh
scripts_dir = ~/.config/m3-colors/hooks
```

**New Configuration Options:**

- `operation_mode`: Default operation mode when no flag is specified
  - `generator`: Only generate colors
  - `full`: Generate and apply (default)

- **Hook Scripts:** Custom scripts that run with color environment variables
  - Enable with `[Hook.Scripts]` section
  - Scripts receive all colors as environment variables (e.g., `$M3_PRIMARY`)
  - Access metadata: `$M3_MODE`, `$M3_WALLPAPER`

### Templates

Create custom templates in `~/.config/m3-colors/templates/`

**Example template** (`myapp.conf.template`):

```
background={{m3surface}}
foreground={{m3onSurface}}
primary={{m3primary}}
accent={{m3secondary}}

# RGB format (for KDE)
background_rgb={{m3surface_rgb}}
```

**Available color variables:**

**Material 3 Colors:**
- Primary: `m3primary`, `m3onPrimary`, `m3primaryContainer`, `m3onPrimaryContainer`, `m3primaryFixed`, `m3primaryFixedDim`, `m3onPrimaryFixed`, `m3onPrimaryFixedVariant`
- Secondary: `m3secondary`, `m3onSecondary`, `m3secondaryContainer`, `m3onSecondaryContainer`, `m3secondaryFixed`, `m3secondaryFixedDim`, `m3onSecondaryFixed`, `m3onSecondaryFixedVariant`
- Tertiary: `m3tertiary`, `m3onTertiary`, `m3tertiaryContainer`, `m3onTertiaryContainer`, `m3tertiaryFixed`, `m3tertiaryFixedDim`, `m3onTertiaryFixed`, `m3onTertiaryFixedVariant`
- Error: `m3error`, `m3onError`, `m3errorContainer`, `m3onErrorContainer`
- Surface: `m3surface`, `m3onSurface`, `m3surfaceVariant`, `m3onSurfaceVariant`, `m3surfaceDim`, `m3surfaceBright`, `m3surfaceContainerLowest`, `m3surfaceContainerLow`, `m3surfaceContainer`, `m3surfaceContainerHigh`, `m3surfaceContainerHighest`
- Outline: `m3outline`, `m3outlineVariant`
- Inverse: `m3inverseSurface`, `m3inverseOnSurface`, `m3inversePrimary`
- Other: `m3shadow`, `m3scrim`

**Terminal Colors:** `term0` to `term15`

**RGB Format:** Add `_rgb` suffix to any color (e.g., `m3primary_rgb` outputs `255,0,128`)

**Metadata:** `wallpaper_path`, `mode`, `source_color`

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
    },
    {
      "source": "gtkrc",
      "destination": "~/.local/share/themes/FlatColor/gtk-2.0/gtkrc"
    }
  ]
}
```

### Hook Scripts

Create custom hook scripts in `~/.config/m3-colors/hooks/`:

**Example hook script** (`reload-apps.sh`):

```bash
#!/bin/bash

# Colors are available as environment variables
echo "Primary color: $M3_M3PRIMARY"
echo "Mode: $M3_MODE"
echo "Wallpaper: $M3_WALLPAPER"

# Reload applications
killall -USR1 kitty
i3-msg reload
notify-send "Theme Updated" "Applied $M3_MODE mode"
```

**Available environment variables in hook scripts:**
- `M3_MODE` - Current mode (light/dark)
- `M3_WALLPAPER` - Wallpaper path
- `M3_M3PRIMARY`, `M3_M3SECONDARY`, etc. - All color values (uppercase)
- All RGB values: `M3_M3PRIMARY_RGB`, etc.

Enable hook scripts in config:
```ini
[Hook.Scripts]
enabled = true
scripts = reload-apps.sh, notify.sh
scripts_dir = ~/.config/m3-colors/hooks
```

### Post Script

Add custom actions in `~/.config/m3-colors/m3wal-post.sh`:

```bash
#!/bin/bash
# Reload applications
killall -USR1 kitty
i3-msg reload
```

The difference between **Hook Scripts** and **Post Script**:
- **Hook Scripts**: Run with color environment variables, multiple scripts supported
- **Post Script**: Single script, runs at the end, no environment variables

## Output Files

Generated files are saved in two locations:

### `~/.config/m3-colors/output/`
- `{wallpaper}_{variant}_scheme.json` - Full color scheme
- `{wallpaper}_{variant}_scheme.css` - CSS variables

### `~/.config/m3-colors/sample/`
- `{wallpaper}_{variant}_palette.png` - Visual palette preview (16x grid)

### `~/.cache/m3-colors/`
- Template-generated config files
- Deployed to applications via deploy.json

### `~/.config/m3-colors/`
- `current_wallpaper` - Symlink to current wallpaper

## Supported Applications

Out of the box templates for:

- **Terminals:** Kitty, Alacritty, TTY
- **WM/DE:** i3, Polybar, Waybar, Dunst
- **Editors:** Neovim, Zathura
- **Launchers:** Rofi
- **Music:** RMPC
- **Themes:** GTK 2/3/4, KDE
- **X11:** Xresources

## Python API

```python
from m3wal import M3WAL, M3Color

# Generator mode (M3Color class)
m3 = M3Color("wallpaper.jpg")
analysis = m3.analyze_wallpaper()
colors = m3.generate_scheme(mode="dark", variant="VIBRANT")
m3.export_json(variant="VIBRANT")
m3.export_css(variant="VIBRANT")
m3.generate_palette_preview()

# Full mode (M3WAL class - extends M3Color)
m3wal = M3WAL("wallpaper.jpg")
m3wal.analyze_wallpaper()
m3wal.generate_scheme(mode="dark", variant="CONTENT")

# Apply to all templates (parallel processing)
generated_files = m3wal.apply_all_templates()

# Deploy configs
m3wal.deploy_configs()

# Reload GTK theme
m3wal.reload_gtk_theme()

# Run hook scripts
m3wal.run_hook_scripts()

# Apply Xresources
m3wal.apply_xresources()

# Set wallpaper
m3wal.set_wallpaper()

# Create symlink
m3wal.create_wallpaper_symlink()

# Run post script
m3wal.run_post_script()
```

## Examples

```bash
# Auto mode with content variant (uses config default)
m3wal ~/Pictures/sunset.jpg

# Generator-only mode (no system changes)
m3wal ~/Pictures/sunset.jpg -g

# Full mode with dark theme and vibrant colors
m3wal ~/Pictures/landscape.jpg --full --mode dark --variant VIBRANT

# Light mode with expressive variant
m3wal ~/Pictures/abstract.jpg -f -m light -v EXPRESSIVE

# Auto-detect mode, apply everything
m3wal ~/Pictures/wallpaper.jpg --full
```

## How It Works

### Generator Mode Flow:
1. **Analyze** wallpaper brightness to determine light/dark mode
2. **Extract** dominant colors using Material Color Utilities
3. **Generate** complete Material 3 color scheme (50+ colors)
4. **Export** JSON and CSS files to `~/.config/m3-colors/output/`
5. **Create** visual palette preview (16-color grid)

### Full Mode Flow:
1. All generator mode steps
2. **Apply** colors to all templates (parallel processing with ThreadPoolExecutor)
3. **Deploy** configs to target applications via deploy.json
4. **Reload** GTK themes (gsettings + xsettingsd)
5. **Execute** hook scripts with color environment variables
6. **Apply** Xresources with xrdb
7. **Set** wallpaper with feh
8. **Create** symlink to current wallpaper
9. **Run** post script for additional actions

## Performance Improvements

- **Parallel template processing:** Uses ThreadPoolExecutor with up to 4 workers for I/O-bound tasks
- **Single color extraction:** Colors are extracted once and reused across all operations
- **Efficient RGB conversion:** RGB values pre-calculated and cached with `_rgb` suffix
- **Optimized palette preview:** 16-column grid layout with dynamic row calculation

## Terminal Colors

The terminal color mapping has been improved for better contrast:

**Dark Mode:** Uses original high-contrast mapping
**Light Mode:** Enhanced with better visibility:
- `term0`: Surface container (background)
- `term1-6`: Primary, secondary, and tertiary variants
- `term7`: On surface variant (foreground)
- `term8-15`: Accent colors with proper contrast

## GTK Theme Reloading

M3WAL automatically reloads GTK themes using two methods:

1. **gsettings:** Toggles GTK theme to trigger reload
2. **xsettingsd:** Restarts xsettingsd daemon with new config

This ensures GTK applications pick up theme changes without restart.

## Troubleshooting

### Templates not found
Ensure templates exist in `~/.config/m3-colors/templates/`

### Wallpaper not setting
Check if `feh` is installed: `which feh`

### GTK theme not reloading
1. Check if xsettingsd config exists: `~/.config/xsettingsd/xsettingsd.conf`
2. Verify xsettingsd is installed: `which xsettingsd`
3. Check gsettings: `gsettings get org.gnome.desktop.interface gtk-theme`

### Hook scripts not running
1. Ensure scripts have execute permission: `chmod +x ~/.config/m3-colors/hooks/*.sh`
2. Enable in config: `[Hook.Scripts] enabled = true`
3. Check script paths in config

### Operation mode confusion
- Use `--generator-only` for color generation only
- Use `--full` for complete rice setup
- Or set default in config: `operation_mode = generator` or `full`

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
