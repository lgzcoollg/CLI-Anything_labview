import click
import json
import os
import sys
from cli_anything.labview.core import project as project_core
from cli_anything.labview.core import vi as vi_core
from cli_anything.labview.utils import labview_backend

@click.group()
@click.option("--year", help="LabVIEW version year (e.g. 2024)")
@click.option("--json", "json_output", is_flag=True, help="Output as JSON")
@click.pass_context
def cli(ctx, year, json_output):
    """
    LabVIEW CLI Harness.
    Control LabVIEW projects and VIs from the command line.
    """
    ctx.ensure_object(dict)
    ctx.obj = ctx.obj or {}
    ctx.obj["year"] = year
    ctx.obj["json"] = json_output

@cli.group()
def project():
    """Project management commands."""
    pass

@project.command("build")
@click.argument("project_path", type=click.Path(exists=True))
@click.argument("build_spec")
@click.option("--target", default="My Computer", help="Target name (default: My Computer)")
@click.pass_context
def project_build(ctx, project_path, build_spec, target):
    """Execute a build specification in a LabVIEW project."""
    result = project_core.build(project_path, build_spec, target, ctx.obj.get("year"))
    
    if ctx.obj.get("json"):
        click.echo(json.dumps(result, indent=2))
    else:
        if result.get("success"):
            click.echo(f"Build successful: {build_spec}")
            if result.get("stdout"):
                click.echo(result["stdout"])
        else:
            click.echo(f"Build failed: {result.get('error')}", err=True)
            if result.get("stderr"):
                click.echo(result["stderr"], err=True)
            if result.get("stdout"):
                click.echo(result["stdout"])

@cli.group()
def vi():
    """VI execution commands."""
    pass

@vi.command("run")
@click.argument("vi_path", type=click.Path(exists=True))
@click.argument("args", nargs=-1)
@click.pass_context
def vi_run(ctx, vi_path, args):
    """Run a LabVIEW VI with optional arguments."""
    result = vi_core.run(vi_path, list(args), ctx.obj.get("year"))
    
    if ctx.obj.get("json"):
        click.echo(json.dumps(result, indent=2))
    else:
        if result.get("success"):
            click.echo(f"VI execution successful: {vi_path}")
            if result.get("stdout"):
                click.echo(result["stdout"])
        else:
            click.echo(f"VI execution failed: {result.get('error')}", err=True)
            if result.get("stderr"):
                click.echo(result["stderr"], err=True)

@cli.command("locate")
@click.pass_context
def locate(ctx):
    """Locate the LabVIEW CLI executable."""
    path = labview_backend.find_labview_cli(ctx.obj.get("year"))
    result = {"path": path, "found": path is not None}
    
    if ctx.obj.get("json"):
        click.echo(json.dumps(result, indent=2))
    else:
        if path:
            click.echo(f"LabVIEW CLI found at: {path}")
        else:
            click.echo("LabVIEW CLI not found.", err=True)
            click.echo("Please ensure LabVIEW is installed or set LABVIEW_CLI_PATH.")

def main():
    cli(obj={})

if __name__ == "__main__":
    main()
