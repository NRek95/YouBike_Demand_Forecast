import os


def add_suffix_to_filenames(folder_path, suffix_to_add):
    """
    Renames all files in a specified folder by adding a suffix before the extension.

    Args:
        folder_path (str): The path to the folder containing the files.
        suffix_to_add (str): The suffix to add to the filenames (e.g., "_site").
    """
    print(f"Scanning folder: {folder_path}")

    # Check if the folder exists
    if not os.path.isdir(folder_path):
        print(f"Error: Folder not found at '{folder_path}'")
        return

    # Get a list of all files in the directory
    try:
        filenames = os.listdir(folder_path)
    except Exception as e:
        print(f"Error reading directory: {e}")
        return

    renamed_count = 0
    for filename in filenames:
        # Construct the full path to the file
        old_file_path = os.path.join(folder_path, filename)

        # Ensure it's a file and not a directory
        if os.path.isfile(old_file_path):
            # Split the filename into its name and extension
            file_name_part, file_extension = os.path.splitext(filename)

            # Check if the file already contains the suffix to avoid double-renaming
            if suffix_to_add in file_name_part:
                print(f"Skipping '{filename}' as it already contains the suffix.")
                continue

            # Create the new filename
            new_filename = f"{file_name_part}{suffix_to_add}{file_extension}"
            new_file_path = os.path.join(folder_path, new_filename)

            # Rename the file
            try:
                os.rename(old_file_path, new_file_path)
                print(f"Renamed '{filename}' to '{new_filename}'")
                renamed_count += 1
            except Exception as e:
                print(f"Could not rename '{filename}'. Error: {e}")

    print(f"\nFinished. Renamed {renamed_count} files.")


# --- HOW TO USE ---
# 1. The path below has been updated for you.
target_folder = '/Users/nikolairekow/Documents/Master_WI/Thesis/sources/stationsnapshot/slots'

# 2. Set the suffix you want to add.
suffix = '_slot'

# 3. Run the script.
add_suffix_to_filenames(target_folder, suffix)
