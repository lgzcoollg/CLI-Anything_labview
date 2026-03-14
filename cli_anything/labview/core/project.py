from cli_anything.labview.utils import labview_backend
import os

def build(project_path, build_spec_name, target="My Computer", year=None):
    """
    Builds a specific build specification in a LabVIEW project.
    """
    if not os.path.exists(project_path):
        return {"success": False, "error": f"Project file not found: {project_path}"}
        
    return labview_backend.run_operation(
        "ExecuteBuildSpec",
        [
            "-ProjectPath", os.path.abspath(project_path),
            "-TargetName", target,
            "-BuildSpecName", build_spec_name
        ],
        year=year
    )

def close(project_path, year=None):
    """
    Closes a LabVIEW project (custom operation, may not exist by default).
    LabVIEW CLI automatically closes projects after operations usually.
    """
    pass
