"""
M3WAL: Wallpaper to Material 3 Color Scheme Generator
Version: Official Library (material-color-utilities)

Install: pip install material-color-utilities Pillow
"""

import json
import sys
from pathlib import Path

from material_color_utilities import Variant, hex_from_argb, theme_from_image
from PIL import Image


class M3WAL:
    def __init__(self, wallpaper_path, config=None):
        self.wallpaper_path = wallpaper_path
        self.theme = None
        self.mode = None
        self.source_color = None
        self.config = config if config else self.load_config()
        self.brightness_threshold = int(self.config.get('General', 'brightness_threshold', fallback='128'))

    def load_config(self):
        """Load configuration from m3-colors.conf"""
        import configparser
        
        config_file = Path.home() / ".config" / "m3-colors" / "m3-colors.conf"
        
        # Default config
        defaults = {
            'mode': 'auto',
            'variant': 'CONTENT',
            'brightness_threshold': '128',
            'templates_dir': 'templates',
            'cache_dir': '~/.cache/m3-colors',
            'config_dir': '~/.config/m3-colors',
            'set_wallpaper': 'true',
            'apply_xresources': 'true',
            'generate_palette_preview': 'true',
            'run_post_script': 'true',
            'create_symlink': 'true',
            'script_path': 'm3wal-post.sh'
        }
        
        config = configparser.ConfigParser()
        
        if config_file.exists():
            config.read(config_file)
        else:
            # make default config
            config['General'] = {
                'mode': defaults['mode'],
                'variant': defaults['variant'],
                'brightness_threshold': defaults['brightness_threshold']
            }
            config['Paths'] = {
                'templates_dir': defaults['templates_dir'],
                'cache_dir': defaults['cache_dir'],
                'config_dir': defaults['config_dir']
            }
            config['Features'] = {
                'set_wallpaper': defaults['set_wallpaper'],
                'apply_xresources': defaults['apply_xresources'],
                'generate_palette_preview': defaults['generate_palette_preview'],
                'run_post_script': defaults['run_post_script'],
                'create_symlink': defaults['create_symlink']
            }
            config['PostScript'] = {
                'script_path': defaults['script_path']
            }
            
            config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(config_file, 'w') as f:
                config.write(f)
        
        return config

    def analyze_wallpaper(self):
        """Extract dominant color & detect brightness"""
        img = Image.open(self.wallpaper_path)

        # Detect brightness for auto mode
        grayscale = img.convert("L")
        pixels = grayscale.tobytes()
        avg_brightness = sum(pixels) / len(pixels)

        # Auto select light/dark mode based on threshold
        self.mode = "dark" if avg_brightness < self.brightness_threshold else "light"

        return {"brightness": avg_brightness, "mode": self.mode}

    def generate_scheme(self, mode=None, variant="CONTENT"):
        """Generate Material 3 color scheme"""
        if mode:
            self.mode = mode

        self.variant = variant

        # Map string to Variant enum
        variant_map = {
            "TONALSPOT": Variant.TONALSPOT,
            "VIBRANT": Variant.VIBRANT,
            "EXPRESSIVE": Variant.EXPRESSIVE,
            "NEUTRAL": Variant.NEUTRAL,
            "FIDELITY": Variant.FIDELITY,
            "CONTENT": Variant.CONTENT,
            "MONOCHROME": Variant.MONOCHROME,
        }

        variant_enum = variant_map.get(variant.upper(), Variant.CONTENT)

        # Generate theme from image
        img = Image.open(self.wallpaper_path)
        self.theme = theme_from_image(img, 0, variant_enum)

        # Get source color
        self.source_color = self.theme.source

        return self._extract_colors()

    def _extract_colors(self):
        """Extract all M3 colors + 16 terminal colors"""
        if not self.theme:
            raise ValueError("Generate scheme first!")

        # Select scheme based on mode
        scheme = (
            self.theme.schemes.dark if self.mode == "dark" else self.theme.schemes.light
        )

        m3_colors = {
            # Primary
            "m3primary": scheme.primary,
            "m3onPrimary": scheme.on_primary,
            "m3primaryContainer": scheme.primary_container,
            "m3onPrimaryContainer": scheme.on_primary_container,
            "m3primaryFixed": scheme.primary_fixed,
            "m3primaryFixedDim": scheme.primary_fixed_dim,
            "m3onPrimaryFixed": scheme.on_primary_fixed,
            "m3onPrimaryFixedVariant": scheme.on_primary_fixed_variant,
            # Secondary
            "m3secondary": scheme.secondary,
            "m3onSecondary": scheme.on_secondary,
            "m3secondaryContainer": scheme.secondary_container,
            "m3onSecondaryContainer": scheme.on_secondary_container,
            "m3secondaryFixed": scheme.secondary_fixed,
            "m3secondaryFixedDim": scheme.secondary_fixed_dim,
            "m3onSecondaryFixed": scheme.on_secondary_fixed,
            "m3onSecondaryFixedVariant": scheme.on_secondary_fixed_variant,
            # Tertiary
            "m3tertiary": scheme.tertiary,
            "m3onTertiary": scheme.on_tertiary,
            "m3tertiaryContainer": scheme.tertiary_container,
            "m3onTertiaryContainer": scheme.on_tertiary_container,
            "m3tertiaryFixed": scheme.tertiary_fixed,
            "m3tertiaryFixedDim": scheme.tertiary_fixed_dim,
            "m3onTertiaryFixed": scheme.on_tertiary_fixed,
            "m3onTertiaryFixedVariant": scheme.on_tertiary_fixed_variant,
            # Error
            "m3error": scheme.error,
            "m3onError": scheme.on_error,
            "m3errorContainer": scheme.error_container,
            "m3onErrorContainer": scheme.on_error_container,
            # Surface
            "m3surface": scheme.surface,
            "m3onSurface": scheme.on_surface,
            "m3surfaceVariant": scheme.surface_variant,
            "m3onSurfaceVariant": scheme.on_surface_variant,
            "m3surfaceDim": scheme.surface_dim,
            "m3surfaceBright": scheme.surface_bright,
            "m3surfaceContainerLowest": scheme.surface_container_lowest,
            "m3surfaceContainerLow": scheme.surface_container_low,
            "m3surfaceContainer": scheme.surface_container,
            "m3surfaceContainerHigh": scheme.surface_container_high,
            "m3surfaceContainerHighest": scheme.surface_container_highest,
            # Background (deprecated in M3 but kept for compatibility)
            "m3background": scheme.surface,
            "m3onBackground": scheme.on_surface,
            # Outline
            "m3outline": scheme.outline,
            "m3outlineVariant": scheme.outline_variant,
            # Inverse
            "m3inverseSurface": scheme.inverse_surface,
            "m3inverseOnSurface": scheme.inverse_on_surface,
            "m3inversePrimary": scheme.inverse_primary,
            # Shadow & Scrim
            "m3shadow": scheme.shadow,
            "m3scrim": scheme.scrim,
        }

        # Generate terminal colors
        terminal_colors = self._generate_terminal_colors(scheme)

        return {**m3_colors, **terminal_colors}

    def _generate_terminal_colors(self, scheme):
        """Generate 16 terminal colors from M3 palette"""
        return {
            # Normal colors
            "term0": scheme.surface_dim,  # Black
            "term1": scheme.error,  # Red
            "term2": scheme.tertiary,  # Green
            "term3": scheme.primary_fixed_dim,  # Yellow
            "term4": scheme.primary,  # Blue
            "term5": scheme.secondary,  # Magenta
            "term6": scheme.tertiary_container,  # Cyan
            "term7": scheme.on_surface,  # White
            # Bright colors
            "term8": scheme.surface_container_high,  # Bright Black
            "term9": scheme.error_container,  # Bright Red
            "term10": scheme.tertiary_fixed,  # Bright Green
            "term11": scheme.primary_fixed,  # Bright Yellow
            "term12": scheme.primary_container,  # Bright Blue
            "term13": scheme.secondary_container,  # Bright Magenta
            "term14": scheme.tertiary_fixed_dim,  # Bright Cyan
            "term15": scheme.surface_bright,  # Bright White
        }

    def apply_all_templates(self, templates_dir=None, output_dir=None):
        """Apply colors to all templates in templates directory"""
        if not self.theme:
            raise ValueError("Generate scheme first!")

        if output_dir is None:
            output_dir = Path.home() / ".cache" / "m3-colors"

        # Use package templates if not specified
        if templates_dir is None:
            try:
                import pkg_resources
                templates_dir = pkg_resources.resource_filename('m3wal', 'templates')
            except:
                # Fallback to config dir
                templates_dir = Path.home() / ".config" / "m3-colors" / "templates"
        
        templates_path = Path(templates_dir)
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Cari semua file .template
        template_files = list(templates_path.glob("*.template"))

        if not template_files:
            print(f"No template files found in {templates_dir}/")
            return []

        generated_files = []

        print(f"\nApplying colors to templates...")
        for template_file in template_files:
            # Hilangkan ekstensi .template untuk nama output
            output_filename = template_file.stem
            output_file = output_path / output_filename

            try:
                self.apply_template(template_file, output_file)
                generated_files.append(str(output_file))
                print(f"  ✓ {template_file.name} → {output_file}")
            except Exception as e:
                print(f"  ✗ {template_file.name}: {e}")

        return generated_files

    def create_wallpaper_symlink(self):
        """Create symlink to current wallpaper in ~/.config/m3-colors"""
        config_dir = Path.home() / ".config" / "m3-colors"
        config_dir.mkdir(parents=True, exist_ok=True)
    
        symlink_path = config_dir / "current_wallpaper"
        wallpaper_path = Path(self.wallpaper_path).resolve()
    
        # Delete old symlink if exist
        if symlink_path.exists() or symlink_path.is_symlink():
            symlink_path.unlink()
    
        # Make new symlink 
        symlink_path.symlink_to(wallpaper_path)
        print(f"  ✓ Created symlink → {symlink_path}")

    def load_deploy_config(self):
        """Load deployment mappings from config"""
        config_file = Path.home() / ".config" / "m3-colors" / "deploy.json"
        
        default_config = {
            "deployments": [
                {"source": "colors-nvim.lua", "destination": "~/.config/nvim/lua/themes/material3.lua"},
                {"source": "gtkrc", "destination": "~/.local/share/themes/FlatColor/gtk-2.0/gtkrc"},
                {"source": "gtk.css", "destination": "~/.local/share/themes/FlatColor/gtk-3.0/gtk.css"},
                {"source": "gtk.3.20", "destination": "~/.local/share/themes/FlatColor/gtk-3.20/gtk.css"}
            ]
        }
        
        if config_file.exists():
            with open(config_file, 'r') as f:
                return json.load(f)
        else:
            config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(config_file, 'w') as f:
                json.dump(default_config, f, indent=2)
            return default_config

    def deploy_configs(self):
        """Deploy configs based on deploy.json"""
        import shutil
        
        cache_dir = Path.home() / ".cache" / "m3-colors"
        config = self.load_deploy_config()
        
        for item in config.get("deployments", []):
            src = cache_dir / item["source"]
            dest = Path(item["destination"]).expanduser()
            
            if src.exists():
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dest)
                print(f"{item['source']} → {dest}")
            else:
                print(f"{item['source']} not found")

    def run_post_script(self, script_path=None):
        """Run post-generation script"""
        import subprocess

        if script_path is None:
            script_path = Path.home() / ".config" / "m3-colors" / "m3wal-post.sh"
        
        script = Path(script_path).expanduser()
        if script.exists():
            subprocess.run(["bash", str(script)])
            print(f"Executed {script.name}")    

    def apply_xresources(self):
        import subprocess

        xresources = Path.home() / ".cache" / "m3-colors" / "colors.Xresources"
        if xresources.exists():
            subprocess.run(["xrdb", "-merge", str(xresources)])
            print(f"  ✓ Applied Xresources")

    def export_json(self, output_path=None, variant="CONTENT"):
        """Export scheme to JSON"""
        if not self.theme:
            raise ValueError("Generate scheme first!")
        colors = self._extract_colors()

        # if output_path doesn't exist, make automatically
        if output_path is None:
            # make new folder output local if doesn't exist
            output_dir = Path("output")
            output_dir.mkdir(exist_ok=True)
            # get wallpaper file name 
            wallpaper_name = Path(self.wallpaper_path).stem
            # make new name file with variant
            output_path = output_dir / f"{wallpaper_name}_{variant}_scheme.json"

        output = {
            "wallpaper": self.wallpaper_path,
            "mode": self.mode,
            "variant": variant,
            "source_color": (
                hex_from_argb(self.source_color)
                if isinstance(self.source_color, int)
                else self.source_color
            ),
            "colors": colors,
        }

        # Save to output_path that has been made
        with open(output_path, "w") as f:
            json.dump(output, f, indent=2)

        # also save to ~/.config/m3-colors/output
        config_dir = Path.home() / ".config" / "m3-colors" / "output"
        config_dir.mkdir(parents=True, exist_ok=True)

        wallpaper_name = Path(self.wallpaper_path).stem
        config_path = config_dir / f"{wallpaper_name}_{variant}_scheme.json"

        with open(config_path, "w") as f:
            json.dump(output, f, indent=2)

        print(f"Exported to: {output_path}")
        print(f"Also saved to: {config_path}")

        return str(output_path)

    def set_wallpaper(self):
        """Set wallpaper using feh"""
        import subprocess

        wallpaper = Path(self.wallpaper_path).expanduser()
        if wallpaper.exists():
            subprocess.run(["feh", "--bg-fill", str(wallpaper)])
            print(f"  ✓ Set wallpaper with feh")

    def apply_template(self, template_path, output_path):
        """Apply colors to template file"""
        if not self.theme:
            raise ValueError("Generate scheme first!")

        colors = self._extract_colors()

        # Add metadata to dictionary colors
        colors["wallpaper_path"] = self.wallpaper_path
        colors["mode"] = self.mode
        colors["source_color"] = (
            hex_from_argb(self.source_color)
            if isinstance(self.source_color, int)
            else self.source_color
        )

        with open(template_path, "r") as f:
            template = f.read()

        # Replace {{m3primary}}, {{term0}}, {{wallpaper_path}}, etc.
        for key, value in colors.items():
            template = template.replace(f"{{{{{key}}}}}", str(value))

        with open(output_path, "w") as f:
            f.write(template)

        return output_path

    def generate_palette_preview(self, output_path=None):
        """Generate color palette preview image"""
        if not self.theme:
            raise ValueError("Generate scheme first!")
        try:
            from PIL import Image, ImageDraw, ImageFont
        except ImportError:
            print("PIL/Pillow not installed. Install: pip install Pillow")
            return None
        
        variant = self.variant if hasattr(self, 'variant') else 'CONTENT'
        colors_dict = self._extract_colors()
        
        # All sequence M3 color 
        all_colors = [
            # Primary colors
            'm3primary', 'm3onPrimary', 'm3primaryContainer', 'm3onPrimaryContainer',
            'm3primaryFixed', 'm3primaryFixedDim', 'm3onPrimaryFixed', 'm3onPrimaryFixedVariant',
            
            # Secondary colors
            'm3secondary', 'm3onSecondary', 'm3secondaryContainer', 'm3onSecondaryContainer',
            'm3secondaryFixed', 'm3secondaryFixedDim', 'm3onSecondaryFixed', 'm3onSecondaryFixedVariant',
            
            # Tertiary colors
            'm3tertiary', 'm3onTertiary', 'm3tertiaryContainer', 'm3onTertiaryContainer',
            'm3tertiaryFixed', 'm3tertiaryFixedDim', 'm3onTertiaryFixed', 'm3onTertiaryFixedVariant',
            
            # Error colors
            'm3error', 'm3onError', 'm3errorContainer', 'm3onErrorContainer',
            
            # Surface colors
            'm3surface', 'm3onSurface', 'm3surfaceVariant', 'm3onSurfaceVariant',
            'm3surfaceDim', 'm3surfaceBright', 'm3surfaceContainerLowest', 'm3surfaceContainerLow',
            'm3surfaceContainer', 'm3surfaceContainerHigh', 'm3surfaceContainerHighest',
            
            # Outline colors
            'm3outline', 'm3outlineVariant',
            
            # Inverse colors
            'm3inverseSurface', 'm3inverseOnSurface', 'm3inversePrimary',
            
            # Shadow & Scrim
            'm3shadow', 'm3scrim',
        ]
        
        # Terminal colors
        all_colors.extend([f'term{i}' for i in range(16)])
        
        # Filter 
        available_colors = [key for key in all_colors if colors_dict.get(key) is not None]
        
        # configuration grid
        MAX_COLS = 16
        cell_width = 80
        cell_height = 60
        
        # count how many column/row that we need
        total_colors = len(available_colors)
        num_rows = (total_colors + MAX_COLS - 1) // MAX_COLS  # Ceiling division
        
        # make image
        img_width = cell_width * MAX_COLS
        img_height = cell_height * num_rows
        img = Image.new('RGB', (img_width, img_height), 'white')
        draw = ImageDraw.Draw(img)
        
        # Draw every color
        for idx, color_key in enumerate(available_colors):
            color_value = colors_dict.get(color_key)
            if color_value is None:
                continue
            
            # count grid position
            col_idx = idx % MAX_COLS
            row_idx = idx // MAX_COLS
            
            # Convert ARGB to hex
            if isinstance(color_value, int):
                hex_color = hex_from_argb(color_value)
            else:
                hex_color = color_value
            
            # Remove # if exists
            color_clean = hex_color.replace('#', '')
            # Convert hex to RGB
            rgb = tuple(int(color_clean[j:j+2], 16) for j in (0, 2, 4))
            
            # Position
            x = col_idx * cell_width
            y = row_idx * cell_height
            
            # Draw rectangle
            draw.rectangle([x, y, x + cell_width, y + cell_height], fill=rgb)
        
        # Save
        if output_path is None:
            output_dir = Path.home() / ".config" / "m3-colors" / "sample"
            output_dir.mkdir(parents=True, exist_ok=True)
            wallpaper_name = Path(self.wallpaper_path).stem
            output_path = output_dir / f"{wallpaper_name}_{variant}_palette.png"
        
        img.save(output_path)
        print(f"Palette preview saved: {output_path}")
        
        return str(output_path)

    def preview_colors(self):
        """Print color preview"""
        if not self.theme:
            raise ValueError("Generate scheme first!")

        colors = self._extract_colors()

        print(f"\nColor Preview ({self.mode} mode):")
        print(
            f"  Source: {hex_from_argb(self.source_color) if isinstance(self.source_color, int) else self.source_color}"
        )
        print(f"\n  Primary: {colors['m3primary']}")
        print(f"  Secondary: {colors['m3secondary']}")
        print(f"  Tertiary: {colors['m3tertiary']}")
        print(f"  Surface: {colors['m3surface']}")
        print(f"  Error: {colors['m3error']}")

        print(f"\n  Terminal Colors:")
        for i in range(16):
            print(f"    term{i}: {colors[f'term{i}']}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python m3wal.py <wallpaper_path> [light|dark|auto] [variant]")
        print("\nVariants: TONALSPOT, VIBRANT, EXPRESSIVE, NEUTRAL, FIDELITY, CONTENT, MONOCHROME")
        print("Default: uses m3-colors.conf settings")
        sys.exit(1)

    wallpaper = sys.argv[1]
    
    # Initialize and load config
    m3wal = M3WAL(wallpaper)
    
    # Override config with CLI args if provided
    mode = sys.argv[2] if len(sys.argv) > 2 else m3wal.config.get('General', 'mode', fallback='auto')
    variant = sys.argv[3] if len(sys.argv) > 3 else m3wal.config.get('General', 'variant', fallback='CONTENT')

    # Analyze wallpaper
    print("Analyzing wallpaper...")
    analysis = m3wal.analyze_wallpaper()
    print(f"  Brightness: {analysis['brightness']:.1f} (threshold: {m3wal.brightness_threshold})")
    print(f"  Auto-detected mode: {analysis['mode']}")

    # Generate scheme
    if mode == "auto":
        mode = analysis["mode"]

    print(f"\nGenerating {mode} scheme with {variant} variant...")
    colors = m3wal.generate_scheme(mode, variant)
    print(f"  Generated {len(colors)} colors")

    # Export to JSON
    output = m3wal.export_json(variant=variant)
    print(f"\nExported to: {output}")

    # Apply to all templates
    cache_dir = Path(m3wal.config.get('Paths', 'cache_dir', fallback='~/.cache/m3-colors')).expanduser()
    generated_files = m3wal.apply_all_templates(output_dir=cache_dir)

    if generated_files:
        print(f"\n✨ Generated {len(generated_files)} config files")

    # Deploy configs
    print("\nDeploying configs...")
    m3wal.deploy_configs()

    # Apply Xresources
    if m3wal.config.getboolean('Features', 'apply_xresources', fallback=True):
        print("\nApplying Xresources...")
        m3wal.apply_xresources()

    # Set wallpaper
    if m3wal.config.getboolean('Features', 'set_wallpaper', fallback=True):
        print("\nSetting wallpaper...")
        m3wal.set_wallpaper()

    # Create wallpaper symlink
    if m3wal.config.getboolean('Features', 'create_symlink', fallback=True):
        print("\nCreating wallpaper symlink...")
        m3wal.create_wallpaper_symlink()

    # Run post script
    if m3wal.config.getboolean('Features', 'run_post_script', fallback=True):
        script_path = m3wal.config.get('PostScript', 'script_path', fallback='m3wal-post.sh')
        # if relative path, merge with config_dir
        if not Path(script_path).is_absolute():
            config_dir = Path(m3wal.config.get('Paths', 'config_dir', fallback='~/.config/m3-colors')).expanduser()
            script_path = config_dir / script_path
        
        print("\nRunning post script...")
        m3wal.run_post_script(script_path)

    # Show preview
    m3wal.preview_colors()

    # Generate palette preview
    if m3wal.config.getboolean('Features', 'generate_palette_preview', fallback=True):
        print("\nGenerating palette preview...")
        m3wal.generate_palette_preview()

if __name__ == "__main__":
    main()
