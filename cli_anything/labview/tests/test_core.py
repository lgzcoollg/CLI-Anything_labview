import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Add the parent directory to sys.path to allow imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

from cli_anything.labview.core import project
from cli_anything.labview.core import vi
from cli_anything.labview.utils import labview_backend

class TestLabVIEWBackend(unittest.TestCase):
    
    @patch('subprocess.run')
    @patch('cli_anything.labview.utils.labview_backend.find_labview_cli')
    def test_run_operation_success(self, mock_find, mock_run):
        mock_find.return_value = "/path/to/LabVIEWCLI"
        mock_run.return_value = MagicMock(returncode=0, stdout="Success", stderr="")
        
        result = labview_backend.run_operation("TestOp", ["-Arg", "Value"])
        
        self.assertTrue(result["success"])
        self.assertEqual(result["stdout"], "Success")
        mock_run.assert_called_with(
            ["/path/to/LabVIEWCLI", "-OperationName", "TestOp", "-Arg", "Value"],
            capture_output=True,
            text=True,
            check=False
        )

    @patch('cli_anything.labview.utils.labview_backend.find_labview_cli')
    def test_run_operation_not_found(self, mock_find):
        mock_find.return_value = None
        result = labview_backend.run_operation("TestOp")
        self.assertFalse(result["success"])
        self.assertIn("LabVIEW CLI executable not found", result["error"])

class TestCore(unittest.TestCase):
    
    @patch('cli_anything.labview.utils.labview_backend.run_operation')
    @patch('os.path.exists')
    def test_project_build(self, mock_exists, mock_run):
        mock_exists.return_value = True
        mock_run.return_value = {"success": True}
        
        project.build("/path/to/project.lvproj", "MySpec", target="My Computer")
        
        mock_run.assert_called_with(
            "ExecuteBuildSpec",
            ["-ProjectPath", "/path/to/project.lvproj", "-TargetName", "My Computer", "-BuildSpecName", "MySpec"],
            year=None
        )

    @patch('cli_anything.labview.utils.labview_backend.run_operation')
    @patch('os.path.exists')
    def test_vi_run(self, mock_exists, mock_run):
        mock_exists.return_value = True
        mock_run.return_value = {"success": True}
        
        vi.run("/path/to/test.vi", ["arg1", "arg2"])
        
        mock_run.assert_called_with(
            "RunVI",
            ["-VIPath", "/path/to/test.vi", "arg1", "arg2"],
            year=None
        )

if __name__ == '__main__':
    unittest.main()
