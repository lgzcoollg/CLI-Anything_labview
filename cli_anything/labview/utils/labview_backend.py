import os
import shutil
import subprocess
import json
import platform
import glob

LABVIEW_YEARS = ["2025", "2024", "2023", "2022", "2021", "2020", "2019"]

def find_labview_cli(year=None):
    """
    Finds the LabVIEWCLI executable.
    
    Priority:
    1. LABVIEW_CLI_PATH environment variable
    2. Specific year (if provided)
    3. Newest installed version
    """
    # 1. Environment variable
    env_path = os.environ.get("LABVIEW_CLI_PATH")
    if env_path and os.path.exists(env_path):
        return env_path
        
    system = platform.system()
    
    if system == "Darwin": # macOS
        base_paths = [
            "/Applications/National Instruments/LabVIEW {year} 64-bit/LabVIEWCommunity.app/Contents/MacOS/LabVIEWCLI",
            "/Applications/National Instruments/LabVIEW {year}/LabVIEWCommunity.app/Contents/MacOS/LabVIEWCLI",
            "/Applications/National Instruments/LabVIEW {year} 64-bit/LabVIEW CLI/LabVIEWCLI",
            "/Applications/National Instruments/LabVIEW {year}/LabVIEW CLI/LabVIEWCLI",
            "/Library/Application Support/National Instruments/LabVIEW CLI/LabVIEWCLI"  # Common location
        ]
        
        candidates = []
        if year:
            years_to_check = [str(year)]
        else:
            years_to_check = LABVIEW_YEARS
            
        for y in years_to_check:
            for p in base_paths:
                path = p.format(year=y)
                if os.path.exists(path):
                    if year: return path
                    candidates.append(path)
        
        if candidates:
            return candidates[0] # Return the first found (newest year)
            
        # Fallback: Use mdfind to search for LabVIEWCLI
        try:
            mdfind_cmd = ["mdfind", "-name", "LabVIEWCLI"]
            result = subprocess.run(mdfind_cmd, capture_output=True, text=True)
            if result.returncode == 0:
                paths = result.stdout.strip().split('\n')
                for p in paths:
                    if p.endswith("/LabVIEWCLI") and os.access(p, os.X_OK):
                        return p
        except Exception:
            pass
            
    elif system == "Windows":
        # Windows paths usually look like:
        # C:\Program Files\National Instruments\LabVIEW 2020\LabVIEW CLI\LabVIEWCLI.exe
        base_paths = [
            r"C:\Program Files\National Instruments\LabVIEW {year}\LabVIEW CLI\LabVIEWCLI.exe",
            r"C:\Program Files (x86)\National Instruments\LabVIEW {year}\LabVIEW CLI\LabVIEWCLI.exe"
        ]
        
        if year:
            years_to_check = [str(year)]
        else:
            years_to_check = LABVIEW_YEARS

        for y in years_to_check:
            for p in base_paths:
                path = p.format(year=y)
                if os.path.exists(path):
                    return path

    return None

def run_operation(operation_name, args=None, year=None, verbose=False):
    """
    Runs a LabVIEW CLI operation.
    
    Args:
        operation_name (str): The operation name (e.g., RunVI, ExecuteBuildSpec).
        args (list): List of arguments for the operation.
        year (str): Specific LabVIEW year to use.
        verbose (bool): Whether to print command output.
        
    Returns:
        dict: Result of the operation including stdout, stderr, and return code.
    """
    cli_path = find_labview_cli(year)
    if not cli_path:
        return {
            "success": False,
            "error": "LabVIEW CLI executable not found. Set LABVIEW_CLI_PATH or install LabVIEW (2019+).",
            "command": "find_labview_cli"
        }
        
    # Command structure: LabVIEWCLI -OperationName <Name> [Args]
    cmd = [cli_path, "-OperationName", operation_name]
    
    if args:
        cmd.extend(args)
        
    if verbose:
        print(f"Executing: {' '.join(cmd)}")
        
    try:
        # LabVIEW CLI often returns non-zero even on success if VI returns error?
        # We need to capture output to analyze.
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False
        )
        
        success = result.returncode == 0
        # Sometimes LabVIEW CLI prints errors to stdout too
        
        return {
            "success": success,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
            "command": " ".join(cmd)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "command": " ".join(cmd)
        }
