import tkinter as tk
from tkinter import ttk, StringVar, filedialog, messagebox, Canvas
import os
from pathlib import Path
import datetime
import sys
import pandas as pd
import re
import io
import zipfile
import matplotlib as mpl
import string
import textwrap

def get_screen_geometry():
    """Get the geometry of all available screens"""
    root = tk.Tk()
    root.withdraw()  # Hide the temporary window
    
    # Get primary screen dimensions
    primary_width = root.winfo_screenwidth()
    primary_height = root.winfo_screenheight()
    
    # Get all screen dimensions using _tkinter.tcl_call
    try:
        # This gets info about all screens
        screens_info = root.tk.call('wm', 'maxsize', '.')
        all_screens_width = screens_info[0]
        all_screens_height = screens_info[1]
    except:
        # Fallback to primary screen if can't get all screens
        all_screens_width = primary_width
        all_screens_height = primary_height
    
    root.destroy()
    return primary_width, primary_height, all_screens_width, all_screens_height

class SplashScreen:
    def __init__(self, parent):
        self.root = tk.Toplevel(parent)
        self.root.overrideredirect(True)
        self.root.attributes('-alpha', 0.9)
        self.root.attributes('-topmost', True)
        
        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Window dimensions
        width = 400
        height = 200
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        # Create frame
        frame = ttk.Frame(self.root, relief='raised', borderwidth=2)
        frame.pack(fill='both', expand=True)
        
        # Add title
        title = ttk.Label(
            frame, 
            text="Montana Species Distribution Mapper",
            font=('Helvetica', 16, 'bold'),
            foreground='dark green'
        )
        title.pack(pady=20)
        
        # Add loading text
        self.status = ttk.Label(
            frame,
            text="Initializing...",
            font=('Helvetica', 10)
        )
        self.status.pack(pady=10)
        
        # Add progress bar
        self.progress = ttk.Progressbar(
            frame,
            mode='indeterminate',
            length=300
        )
        self.progress.pack(pady=20)
        self.progress.start(10)
        
        self.root.update()
    
    def update_status(self, message):
        self.status.config(text=message)
        self.root.update()
    
    def destroy(self):
        self.root.destroy()

class ToastNotification:
    def __init__(self, parent):
        self.parent = parent
        
    def show_toast(self, message, duration=3000, error=False):
        # Create toast window
        toast = tk.Toplevel(self.parent)
        toast.withdraw()  # Hide initially for position calculation
        
        # Remove window decorations
        toast.overrideredirect(True)
        
        # Create frame with border
        frame = ttk.Frame(toast, style='Toast.TFrame')
        frame.pack(fill='both', expand=True)
        
        # Add message with icon
        msg_frame = ttk.Frame(frame)
        msg_frame.pack(pady=10, padx=20)
        
        # Icon and color based on type
        if error:
            icon_text = "✕"
            icon_color = 'red'
            msg_color = 'red'
        else:
            icon_text = "✓"
            icon_color = 'green'
            msg_color = 'black'
        
        # Icon label
        icon_label = ttk.Label(msg_frame, text=icon_text, font=('Helvetica', 14, 'bold'), foreground=icon_color)
        icon_label.pack(side='left', padx=(0, 10))
        
        # Message with color
        msg_label = ttk.Label(msg_frame, text=message, font=('Helvetica', 10), foreground=msg_color)
        msg_label.pack(side='left')
        
        # Position toast at bottom right of main window
        toast.update_idletasks()  # Update to get actual size
        main_x = self.parent.winfo_x()
        main_y = self.parent.winfo_y()
        main_width = self.parent.winfo_width()
        main_height = self.parent.winfo_height()
        
        toast_width = toast.winfo_width()
        toast_height = toast.winfo_height()
        
        x = main_x + main_width - toast_width - 20
        y = main_y + main_height - toast_height - 20
        
        toast.geometry(f"+{x}+{y}")
        toast.deiconify()  # Show the toast
        
        # Destroy after duration
        toast.after(duration, toast.destroy)

class MainApplication:
    def __init__(self):
        # Create and hide the root window
        self.root = tk.Tk()
        
        # Set the application icon
        if getattr(sys, 'frozen', False):
            # If running as exe
            base_dir = sys._MEIPASS
        else:
            # If running as script
            base_dir = os.path.dirname(os.path.abspath(__file__))
        
        icon_path = os.path.join(base_dir, "app_icon.ico")
        if os.path.exists(icon_path):
            self.root.iconbitmap(icon_path)
        
        # Get screen information
        self.primary_width, self.primary_height, self.all_screens_width, self.all_screens_height = get_screen_geometry()
        
        # Allow the window to be moved to any screen
        self.root.attributes('-alpha', 1.0)  # Ensure window is visible
        self.root.attributes('-topmost', False)  # Don't force window to stay on top
        
        # Hide initially for setup
        self.root.withdraw()
        
        # Initialize variables
        self.gdf = None
        self.pd = None
        self.gpd = None
        self.plt = None
        self.FigureCanvasTkAgg = None
        
        # Show splash screen
        self.splash = SplashScreen(self.root)
        
        # Start loading sequence
        self.root.after(100, self.load_step_1)
        
        # Start the event loop
        self.root.mainloop()
    
    def load_step_1(self):
        """Load pandas"""
        try:
            self.splash.update_status("From Billings to Bozeman...")
            import pandas as pd
            self.pd = pd
            self.root.after(100, self.load_step_2)
        except Exception as e:
            self.show_error(f"Error loading pandas: {str(e)}")
    
    def load_step_2(self):
        """Load geopandas"""
        try:
            self.splash.update_status("Spanning the Big Sky Country...")
            import geopandas as gpd
            self.gpd = gpd
            self.root.after(100, self.load_step_3)
        except Exception as e:
            self.show_error(f"Error loading geopandas: {str(e)}")
    
    def load_step_3(self):
        """Load matplotlib"""
        try:
            self.splash.update_status("Mapping Montana's vast landscapes...")
            import matplotlib.pyplot as plt
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
            self.plt = plt
            self.FigureCanvasTkAgg = FigureCanvasTkAgg
            self.root.after(100, self.load_step_4)
        except Exception as e:
            self.show_error(f"Error loading matplotlib: {str(e)}")
    
    def load_step_4(self):
        """Load shapefile"""
        try:
            self.splash.update_status("Connecting all 56 counties...")
            self.load_shapefile()
            self.root.after(100, self.show_analysis_screen)
        except Exception as e:
            self.show_error(f"Error loading shapefile: {str(e)}")
    
    def show_analysis_screen(self):
        """Show the analysis screen after splash"""
        self.splash.destroy()
        AnalysisScreen(self.root, self)
    
    def show_error(self, message):
        """Show error message and exit"""
        if hasattr(self, 'splash'):
            self.splash.destroy()
        messagebox.showerror("Error", message)
        self.root.quit()
        sys.exit(1)
    
    def load_shapefile(self):
        try:
            # Get the application's base directory
            if getattr(sys, 'frozen', False):
                base_dir = sys._MEIPASS
            else:
                base_dir = os.path.dirname(os.path.abspath(__file__))
            
            shapefile_path = os.path.join(base_dir, "MontanaCounties_shp", "County.shp")
            
            if not os.path.exists(shapefile_path):
                raise FileNotFoundError(
                    f"Shapefile not found at:\n{shapefile_path}\n\n"
                    "Please ensure the MontanaCounties_shp folder is in the correct location."
                )
                
            self.gdf = self.gpd.read_file(shapefile_path)
            self.gdf.columns = self.gdf.columns.str.strip()
            self.gdf["County"] = self.gdf["NAME"].str.strip().str.lower()
            self.gdf["Color"] = "white"
            
        except Exception as e:
            raise Exception(f"Error loading shapefile:\n{str(e)}\n\nPlease ensure the shapefile is not corrupted and try again.")

class AnalysisScreen:
    def __init__(self, parent, main_app):
        self.root = tk.Toplevel(parent)
        self.root.title("Montana Species Distribution Mapper")
        
        # Allow the window to be moved to any screen
        self.root.attributes('-alpha', 1.0)
        self.root.attributes('-topmost', False)
        
        # Store main_app reference
        self.main_app = main_app
        
        # Get dependencies from main_app
        self.pd = main_app.pd
        self.plt = main_app.plt
        self.FigureCanvasTkAgg = main_app.FigureCanvasTkAgg
        
        # Set window icon
        if getattr(sys, 'frozen', False):
            base_dir = sys._MEIPASS
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(base_dir, "app_icon.ico")
        if os.path.exists(icon_path):
            self.root.iconbitmap(icon_path)
        
        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Set initial size
        self.root.geometry(f"{screen_width}x{screen_height}")
        
        # Ensure window can be moved and resized
        self.root.resizable(True, True)
        self.root.minsize(800, 600)
        
        # Initialize variables
        self.map_canvas = None
        self.current_fig = None
        
        # Initialize StringVar variables
        self.color_var = StringVar(self.root)
        self.selected_family = StringVar(self.root)
        self.selected_genus = StringVar(self.root)
        self.selected_file_var = StringVar(self.root)
        
        # Set default values
        self.color_var.set("grey")
        self.selected_file_var.set("No file selected")
        
        # Create toast notification instance
        self.toast = ToastNotification(self.root)
        
        # Initialize pandas DataFrame
        self.df = self.pd.DataFrame()
        
        # Get the shapefile data from parent
        self.gdf = main_app.gdf.copy()
        
        # Add attributes for pagination and storing generated maps
        self.generated_maps = []  # List of (species, fig) tuples
        self.current_page = 0
        self.maps_per_page = 15
        
        # Initialize GUI
        self.initialize_gui()
        
        # Bind window state change
        self.root.bind("<Configure>", self.on_window_resize)

    def standardize_county_names(self, county_series):
        """
        Standardize county names by:
        1. Converting '&' to 'and'
        2. Stripping whitespace
        3. Converting to lowercase
        """
        return county_series.str.strip().str.lower().str.replace('&', 'and')

    def get_figure_number(self, map_index):
        """
        Calculate figure number based on map index.
        Maps 1-26: Figure 1A, 1B, 1C, ..., 1Z
        Maps 27-52: Figure 2A, 2B, 2C, ..., 2Z
        Maps 53-78: Figure 3A, 3B, 3C, ..., 3Z
        And so on...
        """
        # Calculate which group of 26 this map belongs to (1-based)
        group_number = (map_index // 26) + 1
        
        # Calculate position within the group (0-25)
        position_in_group = map_index % 26
        
        # Convert position to letter (A-Z)
        letter = string.ascii_uppercase[position_in_group]
        
        return f"Figure {group_number}{letter}."

    def load_excel(self):
        path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
        if not path:
            return
        
        # Show loading dialog
        loading_window = tk.Tk()
        loading_window.title("Loading")
        screen_width = loading_window.winfo_screenwidth()
        screen_height = loading_window.winfo_screenheight()
        window_width = 300
        window_height = 100
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        loading_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        loading_window.overrideredirect(True)
        
        frame = ttk.Frame(loading_window, padding="20", relief="raised")
        frame.pack(fill='both', expand=True)
        
        loading_label = ttk.Label(frame, text="Loading file...\nPlease wait", font=('Helvetica', 10))
        loading_label.pack(pady=10)
        
        progress = ttk.Progressbar(frame, mode='indeterminate')
        progress.pack(fill='x', pady=5)
        progress.start(10)
        
        loading_window.update()
        
        try:
            # Load the Excel file
            self.df = self.pd.read_excel(path, sheet_name=0)
            
            # Now continue with column processing
            self.df.columns = self.df.columns.str.strip()
            
            # Get just the filename from the path
            filename = path.split('/')[-1]
            
            # Validate required columns
            required_columns = ["county", "family", "genus", "species"]
            missing_columns = [col for col in required_columns if col not in self.df.columns]
            
            if missing_columns:
                progress.stop()
                loading_window.destroy()
                self.selected_file_var.set("No file selected")
                messagebox.showerror("Error", 
                    f"Missing required columns: {', '.join(missing_columns)}\n\n"
                    "The following columns are required:\n"
                    "- county: for mapping locations\n"
                    "- family: for taxonomic classification\n"
                    "- genus: for taxonomic classification\n"
                    "- species: for taxonomic classification\n\n"
                    "Please check your Excel file and try again."
                )
                return
            
            # Process the data
            # First standardize county names
            self.df["county"] = self.standardize_county_names(self.df["county"])
            
            # Process other columns
            for col in ["family", "genus", "species"]:
                self.df[col] = self.df[col].astype(str).str.strip().str.lower()
            
            # Get valid Montana counties from shapefile
            valid_counties = set(self.standardize_county_names(self.gdf["County"]))
            
            # Filter DataFrame to only include valid Montana counties
            montana_records = self.df[self.df["county"].isin(valid_counties)]
            
            if len(montana_records) == 0:
                progress.stop()
                loading_window.destroy()
                self.selected_file_var.set("No file selected")
                messagebox.showerror("Error", 
                    "No valid Montana county records found in the Excel file.\n\n"
                    "Please check that your data contains Montana county records."
                )
                return
            
            # Replace the main DataFrame with only Montana records
            self.df = montana_records
            
            # Calculate statistics using Montana records
            num_records = len(montana_records)
            num_families = len(montana_records["family"].unique())
            num_genera = len(montana_records["genus"].unique())
            num_species = len(montana_records["species"].unique())
            num_counties = len(montana_records["county"].unique())
            
            # Get valid families (non-empty/non-null values)
            valid_families = sorted(montana_records["family"].dropna().unique())
            valid_families = [f for f in valid_families if str(f).strip() and str(f).lower() != 'nan']
            family_values = [f.title() for f in valid_families]
            self.family_dropdown["values"] = family_values
            self.family_dropdown.set("")  # No default selection
            # Clear Genus dropdown
            self.genus_dropdown["values"] = []
            self.genus_dropdown.set("")
            
            # Update file info display
            self.selected_file_var.set(f"✓ {filename}\n{num_records:,} Montana records loaded")
            
            # Stop progress bar and close loading window
            progress.stop()
            loading_window.destroy()
            
            # Show success message with detailed statistics
            messagebox.showinfo("Success", 
                f"File loaded successfully!\n\n"
                f"Montana Dataset Summary:\n"
                f"• Total Records: {num_records:,}\n"
                f"• Unique Families: {num_families}\n"
                f"• Unique Genera: {num_genera}\n"
                f"• Unique Species: {num_species}\n"
                f"• Counties Covered: {num_counties}\n\n"
                "Please select a Family to continue."
            )
            
            print("✅ Excel file loaded successfully!")
            
        except Exception as e:
            progress.stop()
            loading_window.destroy()
            self.selected_file_var.set("No file selected")
            error_message = str(e)
            if "No sheet named" in error_message:
                error_message = "Invalid Excel file format. Please ensure your data is in the first sheet."
            elif "Invalid file" in error_message:
                error_message = "Invalid file format. Please ensure you're uploading a valid Excel (.xlsx) file."
            
            messagebox.showerror("Error", 
                f"Error loading file:\n{error_message}\n\n"
                "Please check your Excel file format and try again."
            )
    
    def update_genus_dropdown(self, event=None):
        family = self.selected_family.get().strip()
        
        if not family:
            self.genus_dropdown["values"] = []
            self.genus_dropdown.set("")
            return
        
        filtered = self.df[self.df["family"].str.title() == family]
        valid_genera = sorted(filtered["genus"].dropna().unique())
        valid_genera = [g for g in valid_genera if str(g).strip() and str(g).lower() != 'nan']
        genus_values = [g.title() for g in valid_genera]
        self.genus_dropdown["values"] = genus_values
        self.genus_dropdown.set("")
    
    def is_valid_color(self, color):
        """Validate if a color string is a valid matplotlib color"""
        try:
            # Convert color to RGB
            self.plt.matplotlib.colors.to_rgb(color)
            return True
        except ValueError:
            return False

    def validate_colors(self):
        """Validate selected color"""
        color = self.color_var.get()
        
        if not self.is_valid_color(color):
            error_msg = f"Invalid color detected: '{color}'"
            self.toast.show_toast(error_msg, duration=5000, error=True)
            return False
        return True

    def on_color_change(self, event=None):
        """Validate colors when they change"""
        self.validate_colors()

    def generate_map(self):
        if self.map_canvas:
            self.map_canvas.get_tk_widget().destroy()
        # Validate colors first
        if not self.validate_colors():
            return
        fam = self.selected_family.get().strip()
        gen = self.selected_genus.get().strip()
        if not fam or fam == "Select Family" or not gen or gen == "Select Genus":
            messagebox.showerror("Missing Input", "Please select Family and Genus.")
            return
        # Show loading dialog
        loading_window = tk.Tk()
        loading_window.title("Generating Maps")
        screen_width = loading_window.winfo_screenwidth()
        screen_height = loading_window.winfo_screenheight()
        window_width = 400
        window_height = 150
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        loading_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        loading_window.overrideredirect(True)
        frame = ttk.Frame(loading_window, padding="20", relief="raised")
        frame.pack(fill='both', expand=True)
        loading_label = ttk.Label(frame, text="Generating maps for all species...\nPlease wait", font=('Helvetica', 10))
        loading_label.pack(pady=10)
        progress = ttk.Progressbar(frame, mode='indeterminate')
        progress.pack(fill='x', pady=5)
        progress.start(10)
        loading_window.update()
        try:
            # Start with base DataFrame
            filtered = self.df
            # Apply family filter
            if fam == "All":
                filtered = filtered[filtered["family"].notna() & (filtered["family"].str.strip() != "")]
            elif fam == "Not Specified":
                filtered = filtered[filtered["family"].isna() | (filtered["family"].str.strip() == "")]
            else:
                filtered = filtered[filtered["family"].str.lower() == fam.lower()]
            # Apply genus filter
            if gen == "All":
                filtered = filtered[filtered["genus"].notna() & (filtered["genus"].str.strip() != "")]
            elif gen == "Not Specified":
                filtered = filtered[filtered["genus"].isna() | (filtered["genus"].str.strip() == "")]
            else:
                filtered = filtered[filtered["genus"].str.lower() == gen.lower()]
            # Get unique species
            unique_species = filtered["species"].dropna().unique()
            unique_species = [sp for sp in unique_species if str(sp).strip() and str(sp).lower() != 'nan']
            if len(unique_species) == 0:
                progress.stop()
                loading_window.destroy()
                messagebox.showerror("No Data", "No species found for the selected Family and Genus combination.")
                return
            # Clear previous maps
            self.generated_maps = []
            self.current_page = 0
            # Create a set of valid county names from the shapefile for quick lookup
            valid_counties = set(self.standardize_county_names(self.gdf["County"]))
            # Track unmatched counties to report to user
            unmatched_counties = set()
            # Generate map for each species
            for i, species in enumerate(unique_species):
                # Update loading message
                loading_label.config(text=f"Generating map {i+1} of {len(unique_species)}...\nSpecies: {species}")
                loading_window.update()
                # Filter data for this species
                species_data = filtered[filtered["species"].str.lower() == species.lower()]
                if len(species_data) == 0:
                    continue
                # Create map for this species
                gdf_copy = self.gdf.copy()
                gdf_copy["Color"] = "white"
                # Mark counties with records for this species
                for county in species_data["county"].unique():
                    county_lower = self.standardize_county_names(pd.Series([county])).iloc[0]
                    if county_lower in valid_counties:
                        mask = self.standardize_county_names(gdf_copy["County"]) == county_lower
                        gdf_copy.loc[mask, "Color"] = self.color_var.get()
                    else:
                        unmatched_counties.add(county)
                # Create figure for this species
                fig = self.plt.figure(figsize=(8, 6))
                # Create main map axis
                ax = fig.add_axes([0.1, 0.2, 0.8, 0.6])
                gdf_copy.boundary.plot(ax=ax, linewidth=0.5, edgecolor="black")
                gdf_copy.plot(ax=ax, color=gdf_copy["Color"], alpha=0.6)
                # Add title
                title = f"{fam.title()} > {gen.title()} > {species.title()}"
                ax.set_title(title, fontsize=10, pad=15, wrap=True)
                ax.axis("off")
                # Add caption below the map
                rec = species_data.iloc[0]
                genus = str(rec.get('genus', '')).strip().title()
                subgenus = str(rec.get('subgenus', '')).strip().title() if 'subgenus' in rec and pd.notna(rec['subgenus']) else ''
                sp_epithet = str(rec.get('species', '')).strip().lower()
                # Use the new figure numbering system
                fig_number = self.get_figure_number(i)
                caption = f"{fig_number} " + r"$\it{{{genus}}}$"
                if subgenus:
                    caption += r" ($\it{{{subgenus[1:-1]}}}$)"
                caption += r" $\it{{{sp_epithet}}}$"
                ax.text(0.01, -0.13, caption, ha='left', va='top', fontsize=11, fontname='Times New Roman', transform=ax.transAxes, wrap=True)
                # Adjust layout
                fig.subplots_adjust(bottom=0.15, top=0.85)
                # Store the map
                self.generated_maps.append((species, fig))
                self.plt.close(fig)
            # Report any unmatched counties
            if unmatched_counties:
                print("\nWarning: The following counties in your Excel file don't match the shapefile counties:")
                print("-------------------------------------------------------------------------")
                for county in sorted(unmatched_counties):
                    print(f"• {county}")
                print("\nValid Montana county names:")
                print("--------------------------------")
                for county in sorted(valid_counties):
                    print(f"• {county}")
                print("-------------------------------------------------------------------------\n")
                messagebox.showwarning("County Name Mismatch",
                    f"Some counties in your Excel file don't match the shapefile counties.\n\n"
                    f"Number of unmatched counties: {len(unmatched_counties)}\n\n"
                    f"Please check the console output for details and ensure county names match exactly."
                )
            # Stop progress and close loading window
            progress.stop()
            loading_window.destroy()
            # Show success message
            messagebox.showinfo("Success", 
                f"Generated {len(self.generated_maps)} maps for {len(unique_species)} species!\n\n"
                f"Family: {fam.title()}\n"
                f"Genus: {gen.title()}\n"
                f"Species Count: {len(unique_species)}"
            )
            # Display the first page
            self.show_current_page()
            # Enable download buttons
            self.download_current_button.config(state="normal")
            self.download_all_button.config(state="normal")
            # Enable pagination buttons if there are more than 15 maps
            if len(self.generated_maps) > self.maps_per_page:
                self.next_button.config(state="normal")
            print(f"✅ Generated {len(self.generated_maps)} maps successfully!")
        except Exception as e:
            progress.stop()
            loading_window.destroy()
            messagebox.showerror("Error", 
                f"Error generating maps:\n{str(e)}\n\n"
                "Please try again."
            )
    
    def download_current_page(self):
        import datetime
        from pathlib import Path
        import re
        import string
        # Get maps for current page
        start = self.current_page * self.maps_per_page
        end = self.current_page + self.maps_per_page
        maps_to_save = self.generated_maps[start:end]
        if not maps_to_save:
            return
        downloads_path = str(Path.home() / "Downloads")
        fam = self.selected_family.get().strip().title()
        gen = self.selected_genus.get().strip().title()
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
        page_num = self.current_page + 1
        filename = f"Megachile-{gen}-{timestamp}_page{page_num}.tiff"
        file_path = os.path.join(downloads_path, filename)
        try:
            mpl.rcParams['font.family'] = 'serif'
            mpl.rcParams['font.serif'] = ['Times New Roman', 'Times', 'DejaVu Serif', 'serif']
            fig = self.plt.figure(figsize=(13.2, 19))
            fig.suptitle(f"{fam} > {gen}", fontsize=18, fontweight='bold', y=0.99)
            cols = 3
            rows = 5
            for idx in range(rows * cols):
                ax = fig.add_subplot(rows, cols, idx + 1)
                if idx < len(maps_to_save):
                    species, species_fig = maps_to_save[idx]
                    fam_val = self.selected_family.get().strip()
                    gen_val = self.selected_genus.get().strip()
                    filtered = self.df
                    if fam_val == "All":
                        filtered = filtered[filtered["family"].notna() & (filtered["family"].str.strip() != "")]
                    elif fam_val == "Not Specified":
                        filtered = filtered[filtered["family"].isna() | (filtered["family"].str.strip() == "")]
                    else:
                        filtered = filtered[filtered["family"].str.lower() == fam_val.lower()]
                    if gen_val == "All":
                        filtered = filtered[filtered["genus"].notna() & (filtered["genus"].str.strip() != "")]
                    elif gen_val == "Not Specified":
                        filtered = filtered[filtered["genus"].isna() | (filtered["genus"].str.strip() == "")]
                    else:
                        filtered = filtered[filtered["genus"].str.lower() == gen_val.lower()]
                    species_data = filtered[filtered["species"].str.lower() == species.lower()]
                    gdf_copy = self.gdf.copy()
                    gdf_copy["Color"] = "white"
                    valid_counties = set(self.standardize_county_names(gdf_copy["County"]))
                    for county in species_data["county"].unique():
                        county_lower = self.standardize_county_names(pd.Series([county])).iloc[0]
                        if county_lower in valid_counties:
                            mask = self.standardize_county_names(gdf_copy["County"]) == county_lower
                            gdf_copy.loc[mask, "Color"] = self.color_var.get()
                    gdf_copy.boundary.plot(ax=ax, linewidth=0.7, edgecolor="black")
                    gdf_copy.plot(ax=ax, color=gdf_copy["Color"], alpha=0.6)
                    ax.axis("off")
                    # --- Caption formatting ---
                    # Calculate global index for this map
                    global_index = self.current_page * self.maps_per_page + idx
                    fig_number = self.get_figure_number(global_index)
                    # Get genus, subgenus, species from DataFrame (first record for this species)
                    rec = species_data.iloc[0]
                    genus = str(rec.get('genus', '')).strip().title()
                    subgenus = str(rec.get('subgenus', '')).strip().title() if 'subgenus' in rec and pd.notna(rec['subgenus']) else ''
                    sp_epithet = str(rec.get('species', '')).strip().lower()
                    # First line: Figure label (normal) and scientific name (italic), both Times New Roman, visually centered
                    fig_label = f"{fig_number} "
                    sci_label = f"{genus} {sp_epithet}"
                    ax.text(0.5, -0.10, fig_label, ha='right', va='bottom', fontsize=11, fontname='Times New Roman', fontstyle='normal', transform=ax.transAxes)
                    ax.text(0.5, -0.10, sci_label, ha='left', va='bottom', fontsize=11, fontname='Times New Roman', fontstyle='italic', transform=ax.transAxes)
                    # Second line: summary
                    num_specimens = len(species_data)
                    num_counties = species_data['county'].nunique()
                    summary = f"in MT, {num_specimens} specimen{'s' if num_specimens != 1 else ''} in {num_counties} count{'ies' if num_counties != 1 else 'y'}."
                    ax.text(0.5, -0.16, summary, ha='center', va='bottom', fontsize=11, fontname='Times New Roman', transform=ax.transAxes)
                else:
                    ax.axis("off")
            fig.tight_layout(pad=0.01)
            fig.subplots_adjust(hspace=0.0, wspace=0.0, bottom=0.04, top=0.98)
            fig.savefig(file_path, format="tiff", dpi=300, bbox_inches='tight')
            self.plt.close(fig)
            self.toast.show_toast(f'Current page saved as {filename} in Downloads!')
            print(f"✅ Current page saved as single TIFF: {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving current page:\n{str(e)}\n\nPlease try again.")

    def download_all_maps(self):
        import datetime
        from pathlib import Path
        import zipfile
        import re
        import string
        if not self.generated_maps:
            return
        downloads_path = str(Path.home() / "Downloads")
        fam = self.selected_family.get().strip().title()
        gen = self.selected_genus.get().strip().title()
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
        zip_filename = f"Megachile-{gen}-{timestamp}.zip"
        zip_path = os.path.join(downloads_path, zip_filename)
        try:
            mpl.rcParams['font.family'] = 'serif'
            mpl.rcParams['font.serif'] = ['Times New Roman', 'Times', 'DejaVu Serif', 'serif']
            tiffs = []
            total_maps = len(self.generated_maps)
            pages = (total_maps + self.maps_per_page - 1) // self.maps_per_page
            for page in range(pages):
                start = page * self.maps_per_page
                end = min(start + self.maps_per_page, total_maps)
                maps_to_save = self.generated_maps[start:end]
                fig = self.plt.figure(figsize=(13.2, 19))
                fig.suptitle(f"{fam} > {gen}", fontsize=18, fontweight='bold', y=0.99)
                cols = 3
                rows = 5
                for idx in range(rows * cols):
                    ax = fig.add_subplot(rows, cols, idx + 1)
                    if idx < len(maps_to_save):
                        species, species_fig = maps_to_save[idx]
                        fam_val = self.selected_family.get().strip()
                        gen_val = self.selected_genus.get().strip()
                        filtered = self.df
                        if fam_val == "All":
                            filtered = filtered[filtered["family"].notna() & (filtered["family"].str.strip() != "")]
                        elif fam_val == "Not Specified":
                            filtered = filtered[filtered["family"].isna() | (filtered["family"].str.strip() == "")]
                        else:
                            filtered = filtered[filtered["family"].str.lower() == fam_val.lower()]
                        if gen_val == "All":
                            filtered = filtered[filtered["genus"].notna() & (filtered["genus"].str.strip() != "")]
                        elif gen_val == "Not Specified":
                            filtered = filtered[filtered["genus"].isna() | (filtered["genus"].str.strip() == "")]
                        else:
                            filtered = filtered[filtered["genus"].str.lower() == gen_val.lower()]
                        species_data = filtered[filtered["species"].str.lower() == species.lower()]
                        gdf_copy = self.gdf.copy()
                        gdf_copy["Color"] = "white"
                        valid_counties = set(self.standardize_county_names(gdf_copy["County"]))
                        for county in species_data["county"].unique():
                            county_lower = self.standardize_county_names(pd.Series([county])).iloc[0]
                            if county_lower in valid_counties:
                                mask = self.standardize_county_names(gdf_copy["County"]) == county_lower
                                gdf_copy.loc[mask, "Color"] = self.color_var.get()
                        gdf_copy.boundary.plot(ax=ax, linewidth=0.7, edgecolor="black")
                        gdf_copy.plot(ax=ax, color=gdf_copy["Color"], alpha=0.6)
                        ax.axis("off")
                        # Calculate global index for this map
                        global_index = page * self.maps_per_page + idx
                        fig_number = self.get_figure_number(global_index)
                        rec = species_data.iloc[0]
                        genus = str(rec.get('genus', '')).strip().title()
                        subgenus = str(rec.get('subgenus', '')).strip().title() if 'subgenus' in rec and pd.notna(rec['subgenus']) else ''
                        sp_epithet = str(rec.get('species', '')).strip().lower()
                        if subgenus:
                            sci_name = rf"$\it{{{genus}}}$ ($\it{{{subgenus}}}$) $\it{{{sp_epithet}}}$"
                        else:
                            sci_name = rf"$\it{{{genus}}}$ $\it{{{sp_epithet}}}$"
                        mapInfo = f"{fig_number} {sci_name}"
                        ax.text(0.5, -0.10, mapInfo, ha='center', va='bottom', fontsize=11, fontname='Times New Roman', transform=ax.transAxes)
                        num_specimens = len(species_data)
                        num_counties = species_data['county'].nunique()
                        summary = f"in MT, {num_specimens} specimen{'s' if num_specimens != 1 else ''} in {num_counties} count{'ies' if num_counties != 1 else 'y'}."
                        ax.text(0.5, -0.16, summary, ha='center', va='bottom', fontsize=11, fontname='Times New Roman', transform=ax.transAxes)
                    else:
                        ax.axis("off")
                fig.tight_layout(pad=0.01)
                fig.subplots_adjust(hspace=0.0, wspace=0.0, bottom=0.04, top=0.98)
                buf = io.BytesIO()
                tiff_name = f"Megachile-{gen}-{timestamp}_page{page+1}.tiff"
                fig.savefig(buf, format="tiff", dpi=300, bbox_inches='tight')
                self.plt.close(fig)
                buf.seek(0)
                tiffs.append((tiff_name, buf.read()))
            with zipfile.ZipFile(zip_path, 'w') as zf:
                for tiff_name, tiff_bytes in tiffs:
                    zf.writestr(tiff_name, tiff_bytes)
            self.toast.show_toast(f'All maps saved as {zip_filename} in Downloads!')
            print(f"✅ All maps saved as ZIP: {zip_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving all maps:\n{str(e)}\n\nPlease try again.")

    def on_window_resize(self, event=None):
        try:
            # Get current window dimensions
            current_width = self.root.winfo_width()
            current_height = self.root.winfo_height()
            
            # Only process if we have valid dimensions
            if current_width <= 1 or current_height <= 1:
                return
                
            # Store current dimensions for restoring from maximize
            if not hasattr(self, 'last_valid_size'):
                self.last_valid_size = {
                    'width': current_width,
                    'height': current_height,
                    'x': self.root.winfo_x(),
                    'y': self.root.winfo_y()
                }
            
            # Update panels if needed
            self.update_panel_sizes()
                
        except Exception as e:
            print(f"Warning: Resize handling error: {str(e)}")  # For debugging
            pass  # Silently handle any errors during resize

    def update_panel_sizes(self):
        try:
            current_width = self.root.winfo_width()
            
            # Calculate new left panel width (20% of window width, max 300px)
            new_left_width = min(300, max(200, int(current_width * 0.2)))
            
            # Update left panel container if it exists
            if hasattr(self, 'left_panel_container'):
                self.left_panel_container.configure(width=new_left_width)
            
            # Update scroll canvas if it exists and has content
            if hasattr(self, 'scroll_canvas'):
                try:
                    # Only update if canvas exists and has content
                    if self.scroll_canvas.find_all():
                        self.scroll_canvas.configure(width=new_left_width-20)
                        self.scroll_canvas.itemconfig(
                            self.scroll_canvas.find_all()[0],
                            width=new_left_width-20
                        )
                except tk.TclError:
                    pass  # Handle case where canvas is being destroyed
            
            # Redraw map if it exists
            if hasattr(self, 'map_canvas') and self.map_canvas:
                try:
                    self.map_canvas.draw()
                except Exception:
                    pass  # Handle any drawing errors silently
                    
            # Force geometry update
            self.root.update_idletasks()
                
        except Exception as e:
            print(f"Warning: Panel update error: {str(e)}")  # For debugging
            pass  # Silently handle any errors

    def initialize_gui(self):
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TLabel', font=('Helvetica', 10))
        style.configure('TButton', font=('Helvetica', 10))
        style.configure('Header.TLabel', font=('Helvetica', 12, 'bold'))
        style.configure('Title.TLabel', font=('Helvetica', 24, 'bold'))  # Increased from 16 to 24
        style.configure('Back.TButton', 
                       font=('Helvetica', 10, 'bold'),
                       padding=8)
        
        # Create main container with padding
        main_container = ttk.Frame(self.root, padding="20")
        main_container.pack(fill='both', expand=True)
        
        # Title
        title_frame = ttk.Frame(main_container)
        title_frame.pack(fill='x', pady=(0, 20))
        title_label = ttk.Label(
            title_frame, 
            text="Montana Species Distribution Mapper", 
            style='Title.TLabel',
            foreground='dark green'
        )
        title_label.pack()
        
        # Calculate left and right panel widths based on screen size
        screen_width = self.root.winfo_screenwidth()
        left_panel_width = min(300, int(screen_width * 0.2))  # 20% of screen width or 300px, whichever is smaller
        
        # Create left panel for controls with scrollbar
        self.left_panel_container = ttk.Frame(main_container, width=left_panel_width)  # Start with default width
        self.left_panel_container.pack(side='left', fill='y', padx=(0, 20))
        self.left_panel_container.pack_propagate(False)  # Prevent the frame from shrinking
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.left_panel_container)
        scrollbar.pack(side='right', fill='y')
        
        # Create canvas for scrollable content with matching background
        bg_color = style.lookup('TFrame', 'background')  # Get ttk frame background color
        if not bg_color:  # Fallback if style lookup fails
            bg_color = self.left_panel_container.cget('background')
        self.scroll_canvas = Canvas(
            self.left_panel_container,
            yscrollcommand=scrollbar.set,
            width=left_panel_width-20,
            bg=bg_color,
            highlightthickness=0  # Remove border
        )
        self.scroll_canvas.pack(side='left', fill='y')
        
        scrollbar.config(command=self.scroll_canvas.yview)
        
        # Create frame for controls inside canvas
        left_panel = ttk.Frame(self.scroll_canvas)
        self.scroll_canvas.create_window((0, 0), window=left_panel, anchor='nw', width=left_panel_width-20)
        
        # Excel Load Section
        excel_frame = ttk.LabelFrame(left_panel, text="Data Input", padding="10")
        excel_frame.pack(fill='x', pady=(0, 20))
        
        # Create a frame for the button and file info
        file_info_frame = ttk.Frame(excel_frame)
        file_info_frame.pack(fill='x', expand=True)
        
        # Load button
        load_button = ttk.Button(
            file_info_frame, 
            text="Load Excel File", 
            command=self.load_excel, 
            style='TButton'
        )
        load_button.pack(fill='x', pady=(0, 5))
        
        # File info label
        file_label = ttk.Label(
            file_info_frame, 
            textvariable=self.selected_file_var,
            style='FileInfo.TLabel',
            wraplength=250
        )
        file_label.pack(fill='x')
        
        # Configure style for file info
        style.configure('FileInfo.TLabel', 
                       font=('Helvetica', 9),
                       foreground='dark green')
        
        # Color Selection Section
        color_frame = ttk.LabelFrame(left_panel, text="Color Settings", padding="10")
        color_frame.pack(fill='x', pady=(0, 20))
        
        # Common color options
        color_options = ["red", "blue", "grey", "black", "yellow", "purple", "orange", "pink", "brown"]
        
        # Color input
        ttk.Label(color_frame, text="Enter Color:", style='TLabel').pack(fill='x')
        color_combo = ttk.Combobox(
            color_frame, 
            textvariable=self.color_var, 
            values=color_options,
            state="normal"
        )
        color_combo.pack(fill='x', pady=(0, 10))
        color_combo.bind('<<ComboboxSelected>>', self.on_color_change)
        color_combo.bind('<Return>', self.on_color_change)
        color_combo.bind('<FocusOut>', self.on_color_change)
        
        # Add helper text for custom colors
        helper_label = ttk.Label(
            color_frame, 
            text="Tip: You can type any valid color name or hex code (e.g., #FF5733)",
            style='TLabel',
            wraplength=250
        )
        helper_label.pack(fill='x', pady=(5, 0))
        
        # Species Selection Section
        species_frame = ttk.LabelFrame(left_panel, text="Species Selection", padding="10")
        species_frame.pack(fill='x', pady=(0, 20))
        
        # Family
        ttk.Label(species_frame, text="Family:", style='TLabel').pack(fill='x')
        self.family_dropdown = ttk.Combobox(species_frame, textvariable=self.selected_family, state="readonly")
        self.family_dropdown.pack(fill='x', pady=(0, 10))
        
        # Genus
        ttk.Label(species_frame, text="Genus:", style='TLabel').pack(fill='x')
        self.genus_dropdown = ttk.Combobox(species_frame, textvariable=self.selected_genus, state="readonly")
        self.genus_dropdown.pack(fill='x', pady=(0, 10))
        
        # Button Section
        button_frame = ttk.Frame(left_panel)
        button_frame.pack(fill='x', pady=(0, 20))
        
        # Style configuration for buttons
        style.configure('Action.TButton', 
                       font=('Helvetica', 10, 'bold'),
                       padding=10)
        
        generate_button = ttk.Button(
            button_frame, 
            text="Generate Maps", 
            command=self.generate_map, 
            style='Action.TButton'
        )
        generate_button.pack(fill='x', pady=(0, 5))
        
        # In initialize_gui, after the button section, add pagination and download buttons
        self.pagination_frame = ttk.Frame(left_panel)
        self.pagination_frame.pack(fill='x', pady=(0, 10))
        self.prev_button = ttk.Button(self.pagination_frame, text='Previous', command=self.show_prev_page, state='disabled')
        self.prev_button.pack(side='left', padx=5)
        self.next_button = ttk.Button(self.pagination_frame, text='Next', command=self.show_next_page, state='disabled')
        self.next_button.pack(side='left', padx=5)

        self.download_current_button = ttk.Button(left_panel, text='Download Current Page (Single TIFF)', command=self.download_current_page, state='disabled')
        self.download_current_button.pack(fill='x', pady=(0, 5))
        self.download_all_button = ttk.Button(left_panel, text='Download All Maps (ZIP)', command=self.download_all_maps, state='disabled')
        self.download_all_button.pack(fill='x', pady=(0, 5))
        
        # Create right panel for map display with dynamic width
        self.right_panel = ttk.Frame(main_container)
        self.right_panel.pack(side='left', fill='both', expand=True)
        
        # Bind resize event to the main update function
        self.root.bind('<Configure>', self.on_window_resize)
        
        # Store initial window size
        self.last_valid_size = {
            'width': self.root.winfo_width(),
            'height': self.root.winfo_height(),
            'x': self.root.winfo_x(),
            'y': self.root.winfo_y()
        }
        
        # Configure scrolling
        def on_configure(event):
            self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox('all'))
        
        left_panel.bind('<Configure>', on_configure)
        
        # Enable mousewheel scrolling
        def on_mousewheel(event):
            self.scroll_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        self.scroll_canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        # Bind dropdowns
        self.family_dropdown.bind("<<ComboboxSelected>>", self.update_genus_dropdown)
        # self.genus_dropdown.bind("<<ComboboxSelected>>", self.update_genus_dropdown)

    def show_current_page(self):
        # Remove previous map display
        for widget in self.right_panel.winfo_children():
            widget.destroy()
        # Get maps for current page
        start = self.current_page * self.maps_per_page
        end = self.current_page * self.maps_per_page + self.maps_per_page
        maps_to_show = self.generated_maps[start:end]
        if not maps_to_show:
            no_maps_label = ttk.Label(self.right_panel, text="No maps to display. Please generate maps first.", 
                                    font=('Helvetica', 12), foreground='gray')
            no_maps_label.pack(expand=True)
            return
        # Create a frame to hold canvas and scrollbars
        canvas_frame = ttk.Frame(self.right_panel)
        canvas_frame.pack(fill='both', expand=True)
        # Create canvas and scrollbars
        canvas = tk.Canvas(canvas_frame, borderwidth=0, highlightthickness=0)
        vscrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        hscrollbar = ttk.Scrollbar(canvas_frame, orient="horizontal", command=canvas.xview)
        canvas.configure(yscrollcommand=vscrollbar.set, xscrollcommand=hscrollbar.set)
        # Grid placement
        canvas.grid(row=0, column=0, sticky='nsew')
        vscrollbar.grid(row=0, column=1, sticky='ns')
        hscrollbar.grid(row=1, column=0, sticky='ew')
        canvas_frame.grid_rowconfigure(0, weight=1)
        canvas_frame.grid_columnconfigure(0, weight=1)
        # Responsive grid: always 3 columns, shrink/grow images to fit
        cols = 3
        rows = (len(maps_to_show) + cols - 1) // cols
        panel_width = self.right_panel.winfo_width()
        if panel_width < 600:
            panel_width = 600
        margin = 40
        img_width = (panel_width - margin * 2) // cols
        img_height = int(img_width * 0.75)
        grid_frame = ttk.Frame(canvas)
        grid_window = canvas.create_window((0, 0), window=grid_frame, anchor="nw")
        for idx, (species, fig) in enumerate(maps_to_show):
            row = idx // cols
            col = idx % cols
            buf = io.BytesIO()
            fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
            buf.seek(0)
            import PIL.Image, PIL.ImageTk
            img = PIL.Image.open(buf)
            img = img.resize((img_width, img_height), PIL.Image.Resampling.LANCZOS)
            tk_img = PIL.ImageTk.PhotoImage(img)
            map_frame = ttk.Frame(grid_frame, relief='raised', borderwidth=1)
            map_frame.grid(row=row*2, column=col, padx=8, pady=8, sticky='nsew')
            map_label = ttk.Label(map_frame, image=tk_img)
            map_label.image = tk_img
            map_label.pack(pady=(5, 0))
            caption = fig.texts[0].get_text() if fig.texts else ''
            cap_label = ttk.Label(map_frame, text=caption, font=('Helvetica', 9, 'italic'), 
                                wraplength=img_width-10, justify='center')
            cap_label.pack(pady=(5, 10))
        for i in range(cols):
            grid_frame.grid_columnconfigure(i, weight=1)
        # Update navigation buttons
        self.prev_button.config(state='normal' if self.current_page > 0 else 'disabled')
        total_pages = (len(self.generated_maps) - 1) // self.maps_per_page
        self.next_button.config(state='normal' if self.current_page < total_pages else 'disabled')
        # Add page info
        if self.generated_maps:
            page_info = ttk.Label(self.right_panel, 
                                text=f"Page {self.current_page + 1} of {total_pages + 1} ({len(maps_to_show)} of {len(self.generated_maps)} maps)",
                                font=('Helvetica', 10), foreground='gray')
            page_info.pack(side='bottom', pady=5)
        # Configure scrolling region and dynamic width
        def on_configure(event=None):
            canvas.configure(scrollregion=canvas.bbox('all'))
            new_width = self.right_panel.winfo_width()
            if new_width < 600:
                new_width = 600
            canvas.itemconfig(grid_window, width=new_width)
        grid_frame.bind('<Configure>', on_configure)

    def show_next_page(self):
        total_pages = (len(self.generated_maps) - 1) // self.maps_per_page
        if self.current_page < total_pages:
            self.current_page += 1
            self.show_current_page()

    def show_prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.show_current_page()

if __name__ == "__main__":
    app = MainApplication()