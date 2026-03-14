# LabVIEW CLI Test Plan

## 1. Unit Tests (Mocked Backend)
- **Objective**: Verify that the CLI correctly constructs arguments for `LabVIEWCLI`.
- **Method**: Mock `subprocess.run` in `labview_backend.run_operation`.
- **Cases**:
  - `project build`: Verify `-OperationName ExecuteBuildSpec` and arguments.
  - `vi run`: Verify `-OperationName RunVI` and arguments.
  - `locate`: Verify path resolution logic.

## 2. E2E Tests (Requires LabVIEW)
- **Objective**: Verify real execution against a local LabVIEW installation.
- **Prerequisites**: LabVIEW 2019+ installed, `LabVIEWCLI` available.
- **Cases**:
  - Run a simple "Hello World" VI.
  - Build a dummy project.
  - Verify return codes and output parsing.

## 3. Manual Verification
- Install the package: `pip install -e .`
- Run `cli-anything-labview locate`
- Run `cli-anything-labview vi run ./test.vi`
