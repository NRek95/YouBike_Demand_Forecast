import pandas as pd
import glob
import os

# --- Configuration ---
# This script assumes it is run from the project root directory,
# and that your data is in a subfolder named 'data/'.
DATA_DIR = 'data/'

# --- 1. Create the Clean Site Information Lookup Table ---
print("--- Step 1: Consolidating Site Information ---")

# Find all files in the data directory that match the "*_site.csv" pattern.
site_files_pattern = os.path.join(DATA_DIR, '*_site.csv')
all_site_files = glob.glob(site_files_pattern)

if not all_site_files:
    print(f"Error: No site files found in '{DATA_DIR}'. Please check the path and filenames.")
else:
    print(f"Found {len(all_site_files)} site files to process.")

    # Load all site files into one large DataFrame.
    all_sites_df = pd.concat((pd.read_csv(file) for file in all_site_files), ignore_index=True)

    # LOGIC: Create the master list. By sorting and then dropping duplicates
    # while keeping the 'last' entry, we ensure that for each station ('sno'),
    # we are using its most recently recorded information.
    sites_info_df = all_sites_df.sort_values('sno').drop_duplicates(subset='sno', keep='last')

    print(f"Created a clean lookup table with {len(sites_info_df)} unique stations.")

# --- 2. Load the Time-Series Slots Data ---
print("\n--- Step 2: Loading Slots Data ---")

# Find all files matching the "*_slots.csv" pattern.
slot_files_pattern = os.path.join(DATA_DIR, '*_slot.csv')
all_slot_files = glob.glob(slot_files_pattern)

if not all_slot_files:
    print(f"Error: No slot files found in '{DATA_DIR}'. Please check the path and filenames.")
else:
    print(f"Found {len(all_slot_files)} slot files to process.")

    # Load all slot files into one large DataFrame.
    slots_df = pd.concat((pd.read_csv(file) for file in all_slot_files), ignore_index=True)

    print(f"Loaded a total of {len(slots_df)} time-stamped slot records.")

# --- 3. Perform the Final Merge ---
print("\n--- Step 3: Merging Site and Slot Data ---")

# We perform a 'left' merge. This takes every row from the detailed 'slots_df'
# and adds the matching static information from our clean 'sites_info_df'.
if 'slots_df' in locals() and 'sites_info_df' in locals():
    # Convert infoTime to datetime objects for proper sorting and analysis
    slots_df['infoTime'] = pd.to_datetime(slots_df['infoTime'])

    # Perform the merge
    final_df = pd.merge(slots_df, sites_info_df, on='sno', how='left')

    # Sort the final dataset by station and time for chronological order.
    final_df = final_df.sort_values(by=['sno', 'infoTime']).reset_index(drop=True)

    print("Merge complete. Your master dataset is ready.")
    print("\nPreview of the final master DataFrame:")
    print(final_df.head())

    # --- 4. Save the Master Dataset (Recommended) ---
    # It's a good practice to save this final, clean dataset to a new file.
    # This way, you don't have to re-run this consolidation script every time.
    output_path = os.path.join(DATA_DIR, 'consolidated_youbike_data.csv')
    final_df.to_csv(output_path, index=False)
    print(f"\nMaster dataset has been saved to: '{output_path}'")

else:
    print("\nHalting script because one or both data sources could not be loaded.")

