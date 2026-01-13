"""
M3WAL: Wallpaper to Material 3 Color Scheme Generator
Version: Official Library (material-color-utilities)

Install: pip install material-color-utilities Pillow
"""

import os 
import subprocess
import json
import sys
from pathlib import Path

from material_color_utilities import Variant, hex_from_argb, theme_from_image
from PIL import Image

class M3Color:
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
            'operation_mode': 'full',  
            'templates_dir': 'templates',
            'cache_dir': '~/.cache/m3-colors',
            'config_dir': '~/.config/m3-colors',
            'set_wallpaper': 'true',
            'apply_xresources': 'true',
            'generate_palette_preview': 'true',
            'run_post_script': 'true',
            'create_symlink': 'true',
            'script_path': 'm3wal-post.sh',
            'scripts_dir': '~/.config/m3-colors/hooks',
            'hook_scripts_enabled': 'false',
            'hook_scripts': 'eww.sh'
        }
        
        config = configparser.ConfigParser()
        
        if config_file.exists():
            config.read(config_file)
            
            # Update missing options
            if not config.has_option('General', 'operation_mode'):
                if not config.has_section('General'):
                    config.add_section('General')
                config.set('General', 'operation_mode', defaults['operation_mode'])
            
            # Add Hooks section if missing
            if not config.has_section('Hooks'):
                config.add_section('Hooks')
                config.set('Hooks', 'scripts_dir', defaults['scripts_dir'])
            
            # Add Hook.Scripts section if missing
            if not config.has_section('Hook.Scripts'):
                config.add_section('Hook.Scripts')
                config.set('Hook.Scripts', 'enabled', defaults['hook_scripts_enabled'])
                config.set('Hook.Scripts', 'scripts', defaults['hook_scripts'])
            
            # Save updated config
            with open(config_file, 'w') as f:
                config.write(f)
        else:
            # make default config
            config['General'] = {
                'mode': defaults['mode'],
                'variant': defaults['variant'],
                'brightness_threshold': defaults['brightness_threshold'],
                'operation_mode': defaults['operation_mode']
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
            config['Hooks'] = {
                'scripts_dir': defaults['scripts_dir']
            }
            config['Hook.Scripts'] = {
                'enabled': defaults['hook_scripts_enabled'],
                'scripts': defaults['hook_scripts']
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

        all_colors = {**m3_colors, **terminal_colors}
       
        for key in list(all_colors.keys()):
            value = all_colors[key]
            if isinstance(value, int):
                all_colors[key] = hex_from_argb(value)

         # Add RGB format for KDE
        for key, value in list(all_colors.items()):
            if not key.endswith('_rgb'):
                rgb = self._argb_to_rgb(value)
                all_colors[f"{key}_rgb"] = f"{rgb[0]},{rgb[1]},{rgb[2]}"

        return all_colors                  

    def _generate_terminal_colors(self, scheme):
        """Generate 16 terminal colors from M3 palette with better contrast"""
        
        if self.mode == "dark":
            # Dark mode: tetap gunakan mapping lama
            return {
                "term0": scheme.surface_dim,
                "term1": scheme.on_error,
                "term2": scheme.outline_variant,
                "term3": scheme.on_primary_fixed_variant,
                "term4": scheme.on_primary,
                "term5": scheme.surface_container_highest,
                "term6": scheme.primary_container,
                "term7": scheme.inverse_primary,
                "term8": scheme.inverse_surface,
                "term9": scheme.error,
                "term10": scheme.tertiary_fixed,
                "term11": scheme.primary_fixed,
                "term12": scheme.primary,
                "term13": scheme.tertiary,
                "term14": scheme.tertiary_fixed_dim,
                "term15": scheme.on_surface,
            }
        else:
            # Light mode: gunakan warna yang lebih kontras
            return {
                "term0": scheme.surface_container_highest,  
                "term1": scheme.error,                       
                "term2": scheme.on_tertiary_fixed_variant,                
                "term3": scheme.on_secondary_fixed_variant,          
                "term4": scheme.primary,                  
                "term5": scheme.secondary,                
                "term6": scheme.outline,    
                "term7": scheme.on_surface_variant,       
                "term8": scheme.tertiary,          
                "term9": scheme.on_error_container,       
                "term10": scheme.tertiary_fixed_dim,      
                "term11": scheme.on_primary_fixed_variant,
                "term12": scheme.on_primary_container,    
                "term13": scheme.on_secondary_container,     
                "term14": scheme.primary_fixed_dim,                                                  
                "term15": scheme.surface_dim,                
            }

    def _argb_to_rgb(self, argb_color):
        """Convert ARGB integer to RGB tuple"""
        if isinstance(argb_color, int):
            hex_color = hex_from_argb(argb_color)
        else:
            hex_color = argb_color
        
        color_clean = hex_color.replace('#', '')
        return tuple(int(color_clean[j:j+2], 16) for j in (0, 2, 4))

    def preview_colors(self):
        """Print color preview"""
        if not self.theme:
            raise ValueError("Generate scheme first!")

        colors = self._extract_colors()

        print(f"\nColor Preview ({self.mode} mode):")
        print(
            f"Source: {hex_from_argb(self.source_color) if isinstance(self.source_color, int) else self.source_color}"
        )
        print(f"\nPrimary: {colors['m3primary']}")
        print(f"Secondary: {colors['m3secondary']}")
        print(f"Tertiary: {colors['m3tertiary']}")
        print(f"Surface: {colors['m3surface']}")
        print(f"Error: {colors['m3error']}")

        print(f"\nTerminal Colors:")
        for i in range(16):
            print(f"term{i}: {colors[f'term{i}']}")

    def export_json(self, output_path=None, variant="CONTENT"):
        """Export scheme to JSON"""
        if not self.theme:
            raise ValueError("Generate scheme first!")
        colors = self._extract_colors()
        
        # Save to ~/.config/m3-colors/output only
        config_dir = Path.home() / ".config" / "m3-colors" / "output"
        config_dir.mkdir(parents=True, exist_ok=True)
        wallpaper_name = Path(self.wallpaper_path).stem
        config_path = config_dir / f"{wallpaper_name}_{variant}_scheme.json"
        
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
        
        with open(config_path, "w") as f:
            json.dump(output, f, indent=2)
        
        print(f"Exported to: {config_path}")
        return str(config_path)

    def export_css(self, output_path=None, variant="CONTENT"):
        """Export scheme to CSS variables"""
        if not self.theme:
            raise ValueError("Generate scheme first!")
        colors = self._extract_colors()
        
        # Save to ~/.config/m3-colors/output
        config_dir = Path.home() / ".config" / "m3-colors" / "output"
        config_dir.mkdir(parents=True, exist_ok=True)
        wallpaper_name = Path(self.wallpaper_path).stem
        
        if output_path is None:
            output_path = config_dir / f"{wallpaper_name}_{variant}_scheme.css"
        
        # Generate CSS content
        css_content = f"""/* Material 3 Color Scheme - {variant} */
    /* Generated from: {wallpaper_name} */
    /* Mode: {self.mode} */

    :root {{
    /* Source Color */
    --source-color: {hex_from_argb(self.source_color) if isinstance(self.source_color, int) else self.source_color};
    
    /* Primary Colors */
    --primary: {colors['m3primary']};
    --on-primary: {colors['m3onPrimary']};
    --primary-container: {colors['m3primaryContainer']};
    --on-primary-container: {colors['m3onPrimaryContainer']};
    --primary-fixed: {colors['m3primaryFixed']};
    --primary-fixed-dim: {colors['m3primaryFixedDim']};
    --on-primary-fixed: {colors['m3onPrimaryFixed']};
    --on-primary-fixed-variant: {colors['m3onPrimaryFixedVariant']};
    
    /* Secondary Colors */
    --secondary: {colors['m3secondary']};
    --on-secondary: {colors['m3onSecondary']};
    --secondary-container: {colors['m3secondaryContainer']};
    --on-secondary-container: {colors['m3onSecondaryContainer']};
    --secondary-fixed: {colors['m3secondaryFixed']};
    --secondary-fixed-dim: {colors['m3secondaryFixedDim']};
    --on-secondary-fixed: {colors['m3onSecondaryFixed']};
    --on-secondary-fixed-variant: {colors['m3onSecondaryFixedVariant']};
    
    /* Tertiary Colors */
    --tertiary: {colors['m3tertiary']};
    --on-tertiary: {colors['m3onTertiary']};
    --tertiary-container: {colors['m3tertiaryContainer']};
    --on-tertiary-container: {colors['m3onTertiaryContainer']};
    --tertiary-fixed: {colors['m3tertiaryFixed']};
    --tertiary-fixed-dim: {colors['m3tertiaryFixedDim']};
    --on-tertiary-fixed: {colors['m3onTertiaryFixed']};
    --on-tertiary-fixed-variant: {colors['m3onTertiaryFixedVariant']};
    
    /* Error Colors */
    --error: {colors['m3error']};
    --on-error: {colors['m3onError']};
    --error-container: {colors['m3errorContainer']};
    --on-error-container: {colors['m3onErrorContainer']};
    
    /* Surface Colors */
    --surface: {colors['m3surface']};
    --on-surface: {colors['m3onSurface']};
    --surface-variant: {colors['m3surfaceVariant']};
    --on-surface-variant: {colors['m3onSurfaceVariant']};
    --surface-dim: {colors['m3surfaceDim']};
    --surface-bright: {colors['m3surfaceBright']};
    --surface-container-lowest: {colors['m3surfaceContainerLowest']};
    --surface-container-low: {colors['m3surfaceContainerLow']};
    --surface-container: {colors['m3surfaceContainer']};
    --surface-container-high: {colors['m3surfaceContainerHigh']};
    --surface-container-highest: {colors['m3surfaceContainerHighest']};
    
    /* Outline Colors */
    --outline: {colors['m3outline']};
    --outline-variant: {colors['m3outlineVariant']};
    
    /* Inverse Colors */
    --inverse-surface: {colors['m3inverseSurface']};
    --inverse-on-surface: {colors['m3inverseOnSurface']};
    --inverse-primary: {colors['m3inversePrimary']};
    
    /* Shadow & Scrim */
    --shadow: {colors['m3shadow']};
    --scrim: {colors['m3scrim']};
    }}
    """
        
        # Write to file
        with open(output_path, "w") as f:
            f.write(css_content)
        
        print(f"Exported CSS to: {output_path}")
        return str(output_path)

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

    def generate_all_variants_preview(self, output_path=None):
        """Generate preview semua variant dalam satu gambar"""
        if not self.theme:
            raise ValueError("Generate scheme first!")
        
        try:
            from PIL import Image, ImageDraw, ImageFont
        except ImportError:
            print("PIL/Pillow not installed. Install: pip install Pillow")
            return None
        
        # Semua variant yang akan di-generate
        variants = ['TONALSPOT', 'VIBRANT', 'EXPRESSIVE', 'NEUTRAL', 
                    'FIDELITY', 'CONTENT', 'MONOCHROME']
        
        # Konfigurasi - lebih rapat
        cell_width = 45
        cell_height = 35
        colors_per_row = 16
        variant_spacing = 15  # Lebih rapat
        header_height = 18    # Lebih rapat
        
        # SEMUA warna M3
        color_keys = [
            # Primary
            'm3primary', 'm3onPrimary', 'm3primaryContainer', 'm3onPrimaryContainer',
            'm3primaryFixed', 'm3primaryFixedDim', 'm3onPrimaryFixed', 'm3onPrimaryFixedVariant',
            # Secondary
            'm3secondary', 'm3onSecondary', 'm3secondaryContainer', 'm3onSecondaryContainer',
            'm3secondaryFixed', 'm3secondaryFixedDim', 'm3onSecondaryFixed', 'm3onSecondaryFixedVariant',
            # Tertiary
            'm3tertiary', 'm3onTertiary', 'm3tertiaryContainer', 'm3onTertiaryContainer',
            'm3tertiaryFixed', 'm3tertiaryFixedDim', 'm3onTertiaryFixed', 'm3onTertiaryFixedVariant',
            # Error
            'm3error', 'm3onError', 'm3errorContainer', 'm3onErrorContainer',
            # Surface
            'm3surface', 'm3onSurface', 'm3surfaceVariant', 'm3onSurfaceVariant',
            'm3surfaceDim', 'm3surfaceBright', 'm3surfaceContainerLowest', 'm3surfaceContainerLow',
            'm3surfaceContainer', 'm3surfaceContainerHigh', 'm3surfaceContainerHighest',
            # Outline
            'm3outline', 'm3outlineVariant',
            # Inverse
            'm3inverseSurface', 'm3inverseOnSurface', 'm3inversePrimary',
            # Shadow & Scrim
            'm3shadow', 'm3scrim',
        ]
        
        # Tambah terminal colors
        color_keys.extend([f'term{i}' for i in range(16)])
        
        rows_per_variant = (len(color_keys) + colors_per_row - 1) // colors_per_row
        variant_height = header_height + (rows_per_variant * cell_height)
        
        # Total image size
        img_width = cell_width * colors_per_row
        img_height = len(variants) * (variant_height + variant_spacing)
        
        # Create image
        img = Image.new('RGB', (img_width, img_height), '#1a1a1a')
        draw = ImageDraw.Draw(img)
        
        # Try load font - lebih kecil
        try:
            font = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 12)
        except:
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 12)
            except:
                font = ImageFont.load_default()
        
        # Generate untuk setiap variant
        for v_idx, variant in enumerate(variants):
            y_offset = v_idx * (variant_height + variant_spacing)
            
            # Generate scheme untuk variant ini
            current_mode = self.mode
            self.generate_scheme(mode=current_mode, variant=variant)
            colors = self._extract_colors()
            
            # Draw header - lebih rapat
            draw.text((5, y_offset + 3), f"{variant} ({current_mode})", 
                    fill='white', font=font)
            
            # Draw colors
            for c_idx, color_key in enumerate(color_keys):
                if color_key not in colors:
                    continue
                
                col = c_idx % colors_per_row
                row = c_idx // colors_per_row
                
                x = col * cell_width
                y = y_offset + header_height + (row * cell_height)
                
                # Convert to RGB
                color_value = colors[color_key]
                if isinstance(color_value, int):
                    hex_color = hex_from_argb(color_value)
                else:
                    hex_color = color_value
                
                color_clean = hex_color.replace('#', '')
                rgb = tuple(int(color_clean[j:j+2], 16) for j in (0, 2, 4))
                
                # Draw rectangle
                draw.rectangle([x, y, x + cell_width, y + cell_height], 
                            fill=rgb, outline='#ddd')
        
        # Save
        if output_path is None:
            output_dir = Path.home() / ".config" / "m3-colors" / "sample"
            output_dir.mkdir(parents=True, exist_ok=True)
            wallpaper_name = Path(self.wallpaper_path).stem
            output_path = output_dir / f"{wallpaper_name}_all_variants.png"
        
        img.save(output_path)
        print(f"All variants preview saved: {output_path}")
        
        return str(output_path)

class M3WAL(M3Color):
    def __init__(self, wallpaper_path, config=None):
        super().__init__(wallpaper_path, config)

    def apply_all_templates(self, templates_dir=None, output_dir=None):
        """Apply colors to all templates - OPTIMIZED VERSION"""
        if not self.theme:
            raise ValueError("Generate scheme first!")

        if output_dir is None:
            output_dir = Path.home() / ".cache" / "m3-colors"

        if templates_dir is None:
            try:
                import pkg_resources
                templates_dir = pkg_resources.resource_filename('m3wal', 'templates')
            except:
                templates_dir = Path.home() / ".config" / "m3-colors" / "templates"
        
        templates_path = Path(templates_dir)
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Find all template files
        template_files = list(templates_path.glob("*.template"))

        if not template_files:
            print(f"No template files found in {templates_dir}/")
            return []

        # ===== OPTIMIZATION: Extract colors ONCE =====
        colors = self._extract_colors()
        
        # Add metadata
        colors["wallpaper_path"] = self.wallpaper_path
        colors["mode"] = self.mode
        colors["source_color"] = (
            hex_from_argb(self.source_color)
            if isinstance(self.source_color, int)
            else self.source_color
        )

        # ===== OPTIMIZATION: Process templates in parallel =====
        from concurrent.futures import ThreadPoolExecutor, as_completed
        
        def process_template(template_file):
            """Process single template file"""
            try:
                # Read template
                with open(template_file, 'r') as f:
                    content = f.read()
                
                # Replace all placeholders
                for key, value in colors.items():
                    content = content.replace(f'{{{{{key}}}}}', str(value))
                
                # Write output
                output_filename = template_file.stem
                output_file = output_path / output_filename
                
                with open(output_file, 'w') as f:
                    f.write(content)
                
                return (True, template_file.name, str(output_file))
                
            except Exception as e:
                return (False, template_file.name, str(e))

        generated_files = []
        
        print(f"\nApplying colors to {len(template_files)} templates...")
        
        # Process with ThreadPoolExecutor (max 4 workers untuk I/O bound tasks)
        with ThreadPoolExecutor(max_workers=4) as executor:
            # Submit all tasks
            future_to_template = {
                executor.submit(process_template, tf): tf 
                for tf in template_files
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_template):
                success, name, result = future.result()
                
                if success:
                    generated_files.append(result)
                    print(f"✓ {name} → {result}")
                else:
                    print(f"✗ {name}: {result}")

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
        print(f"Created symlink → {symlink_path}")

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

    def run_hook_scripts(self):
        """Run external hook scripts with color env vars"""
        if not self.config.has_section('Hook.Scripts'):
            return
        
        if not self.config.getboolean('Hook.Scripts', 'enabled', fallback=False):
            return
        
        scripts_dir = Path(self.config.get('Hooks', 'scripts_dir', 
                        fallback='~/.config/m3-colors/hooks')).expanduser()
        
        if not scripts_dir.exists():
            return
        
        scripts = self.config.get('Hook.Scripts', 'scripts', fallback='').split(',')
        scripts = [s.strip() for s in scripts if s.strip()]
        
        # Prepare environment variables
        colors = self._extract_colors()
        env = os.environ.copy()
        env.update({
            'M3_MODE': self.mode,
            'M3_WALLPAPER': self.wallpaper_path,
            **{f'M3_{k.upper()}': str(v) for k, v in colors.items()}
        })
        
        for script_name in scripts:
            script_path = scripts_dir / script_name
            if script_path.exists() and script_path.is_file():
                print(f"\n[HOOK] Running script: {script_name}")
                try:
                    subprocess.run(['bash', str(script_path)], env=env, check=True)
                    print(f"✓ Success")
                except Exception as e:
                    print(f"✗ Failed: {e}")

    def reload_gtk_theme(self):
        """Reload GTK theme using xsettingsd"""
        import subprocess
        import shutil
        from pathlib import Path
        
        # Method 1: gsettings 
        theme_name = "FlatColor"
        try:
            # Toggle theme untuk trigger reload
            subprocess.run(["gsettings", "set", "org.gnome.desktop.interface", "gtk-theme", "Adwaita"], 
                        stderr=subprocess.DEVNULL)
            subprocess.run(["gsettings", "set", "org.gnome.desktop.interface", "gtk-theme", theme_name],
                        stderr=subprocess.DEVNULL)
            print("Reloaded theme via gsettings")
        except:
            pass
        
        # Method 2: Restart xsettingsd
        if shutil.which("xsettingsd"):
            try:
                # Kill xsettingsd lama
                subprocess.run(["pkill", "-x", "xsettingsd"], stderr=subprocess.DEVNULL)
                # Wait a second
                import time
                time.sleep(0.2)
                # Start xsettingsd baru TANPA timeout, biarkan running
                xsettingsd_config = str(Path.home() / ".config" / "xsettingsd" / "xsettingsd.conf")
                subprocess.Popen(["xsettingsd", "-c", xsettingsd_config],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL)
                print("Reloaded theme via xsettingsd")
            except Exception as e:
                print(f"Failed to reload xsettingsd: {e}")

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
            print(f"Applied Xresources")

    def set_wallpaper(self):
        """Set wallpaper using feh"""
        import subprocess

        wallpaper = Path(self.wallpaper_path).expanduser()
        if wallpaper.exists():
            subprocess.run(["feh", "--bg-fill", str(wallpaper)])
            print(f"Set wallpaper with feh")

    def apply_template(self, template_path, output_path, colors=None):
        """Apply colors to single template file
        
        Args:
            template_path: Path to template file
            output_path: Path to output file
            colors: Optional pre-extracted colors dict (untuk speed)
        """
        if not self.theme:
            raise ValueError("Generate scheme first!")

        # Use provided colors or extract new
        if colors is None:
            colors = self._extract_colors()
            
            # Add metadata
            colors["wallpaper_path"] = self.wallpaper_path
            colors["mode"] = self.mode
            colors["source_color"] = (
                hex_from_argb(self.source_color)
                if isinstance(self.source_color, int)
                else self.source_color
            )

        # Read template
        with open(template_path, "r") as f:
            template = f.read()

        # Replace all placeholders {{key}}
        for key, value in colors.items():
            template = template.replace(f"{{{{{key}}}}}", str(value))

        # Write output
        with open(output_path, "w") as f:
            f.write(template)

        return output_path

def main():
    import argparse
    
    # Setup argument parser
    parser = argparse.ArgumentParser(
        description='M3WAL: Material 3 Color Scheme Generator from Wallpaper',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Required arguments
    parser.add_argument('wallpaper', help='Path to wallpaper image')

    # Color configuration
    color_group = parser.add_argument_group('color configuration')
    color_group.add_argument('--mode', '-m', choices=['light', 'dark', 'auto'], 
                            help='Color scheme mode (overrides config)')
    color_group.add_argument('--variant', '-v',
                            choices=['TONALSPOT', 'VIBRANT', 'EXPRESSIVE', 'NEUTRAL', 
                                    'FIDELITY', 'CONTENT', 'MONOCHROME'],
                            help='Material 3 variant (overrides config)')

    # Execution modes
    mode_group = parser.add_argument_group('execution modes')
    mode_group.add_argument('--generator-only', '-g', action='store_true',
                        help='Only generate colors, skip ricing')
    mode_group.add_argument('--full', '-f', action='store_true',
                        help='Apply all configurations')
    
    args = parser.parse_args()
    
    # Initialize - gunakan class sesuai mode
    wallpaper = args.wallpaper
    
    # Determine operation mode
    if args.generator_only:
        operation_mode = 'generator'
        m3wal = M3Color(wallpaper)
        print("[INFO] Using --generator-only flag")
    elif args.full:
        operation_mode = 'full'
        m3wal = M3WAL(wallpaper)
        print("[INFO] Using --full flag")
    else:
        # Use config default
        config_file = Path.home() / ".config" / "m3-colors" / "m3-colors.conf"
        print(f"[INFO] Using default config: {config_file}")
        
        temp_config = M3Color(wallpaper).config
        operation_mode = temp_config.get('General', 'operation_mode', fallback='full')
        
        if operation_mode == 'generator':
            m3wal = M3Color(wallpaper)
        else:
            m3wal = M3WAL(wallpaper)
        
        print(f"[INFO] Config operation_mode: {operation_mode}")
    
    # Override config with CLI args if provided
    mode = args.mode if args.mode else m3wal.config.get('General', 'mode', fallback='auto')
    variant = args.variant if args.variant else m3wal.config.get('General', 'variant', fallback='CONTENT')
    
    if args.mode:
        print(f"[INFO] Mode overridden by CLI: {mode}")
    if args.variant:
        print(f"[INFO] Variant overridden by CLI: {variant}")
    
    print(f"\nOperation Mode: {operation_mode}")
    print(f"="*50)
    
    # ===== CORE OPERATIONS (Always run) =====
    print("\n[CORE] Analyzing wallpaper...")
    analysis = m3wal.analyze_wallpaper()
    print(f"Brightness: {analysis['brightness']:.1f} (threshold: {m3wal.brightness_threshold})")
    print(f"Auto-detected mode: {analysis['mode']}")
    
    # Generate scheme
    if mode == "auto":
        mode = analysis["mode"]
    
    print(f"\n[CORE] Generating {mode} scheme with {variant} variant...")
    colors = m3wal.generate_scheme(mode, variant)
    print(f"Generated {len(colors)} colors")
    
    # Export to JSON
    print("\n[CORE] Exporting color scheme...")
    output = m3wal.export_json(variant=variant)
    output_css = m3wal.export_css(variant=variant)

    # Show preview
    print("\n[CORE] Color Preview:")
    m3wal.preview_colors()
    
    # Generate palette preview (if enabled)
    if m3wal.config.getboolean('Features', 'generate_palette_preview', fallback=True):
        print("\n[CORE] Generating palette preview...")
        m3wal.generate_palette_preview()
    
    # ===== RICING OPERATIONS (Only if full mode) =====
    if operation_mode == 'full':
        print(f"\n{'='*50}")
        print("[RICING] Applying configurations...")
        print(f"{'='*50}")
        
        # Apply to all templates
        cache_dir = Path(m3wal.config.get('Paths', 'cache_dir', fallback='~/.cache/m3-colors')).expanduser()
        generated_files = m3wal.apply_all_templates(output_dir=cache_dir)
        
        if generated_files:
            print(f"\nGenerated {len(generated_files)} config files")
        
        # Deploy configs
        print("\n[RICING] Deploying configs...")
        m3wal.deploy_configs()
        
        print("\n[RICING] Reloading GTK theme...")
        m3wal.reload_gtk_theme()
        
        # Run hook script
        print("\n[RICING] Run Hook Scripts...")
        m3wal.run_hook_scripts()
        
        # Apply Xresources
        if m3wal.config.getboolean('Features', 'apply_xresources', fallback=True):
            print("\n[RICING] Applying Xresources...")
            m3wal.apply_xresources()
        
        # Set wallpaper
        if m3wal.config.getboolean('Features', 'set_wallpaper', fallback=True):
            print("\n[RICING] Setting wallpaper...")
            m3wal.set_wallpaper()
        
        # Create wallpaper symlink
        if m3wal.config.getboolean('Features', 'create_symlink', fallback=True):
            print("\n[RICING] Creating wallpaper symlink...")
            m3wal.create_wallpaper_symlink()
        
        # Run post script
        if m3wal.config.getboolean('Features', 'run_post_script', fallback=True):
            script_path = m3wal.config.get('PostScript', 'script_path', fallback='m3wal-post.sh')
            # if relative path, merge with config_dir
            if not Path(script_path).is_absolute():
                config_dir = Path(m3wal.config.get('Paths', 'config_dir', fallback='~/.config/m3-colors')).expanduser()
                script_path = config_dir / script_path
            
            print("\n[RICING] Running post script...")
            m3wal.run_post_script(script_path)
    
    else:
        print(f"\n{'='*50}")
        print("[INFO] Generator-only mode: Ricing operations skipped")
        print(f"Use --full flag or set operation_mode='full' in config")
        print(f"to apply configurations to your system")
        print(f"{'='*50}")
    
    print(f"\nDone!")

if __name__ == "__main__":
    main()
