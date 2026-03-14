from cli_anything.labview.utils import labview_backend
import os

def run(vi_path, args=None, year=None):
    """
    Runs a LabVIEW VI.
    
    Args:
        vi_path (str): Path to the .vi file.
        args (list): Additional arguments to pass to the VI.
        year (str): LabVIEW version.
    """
    if not os.path.exists(vi_path):
        return {"success": False, "error": f"VI file not found: {vi_path}"}
        
    cmd_args = ["-VIPath", os.path.abspath(vi_path)]
    if args:
        cmd_args.extend(args)
        
    return labview_backend.run_operation("RunVI", cmd_args, year=year)
