import click
from rich import print
from rich.prompt import Prompt
from rich.table import Table
from rich.console import Console
from modules.base import *
from datetime import datetime
import json
import os
@click.group()
def cli():
    pass

#############################################
#             PROJECT FUNCTIONS             #
#############################################
@cli.group()
def project():
    """Manage projects."""
    pass


@project.command()
@click.argument('name', type=click.STRING)
@click.option("--duration", "-d", type=click.INT, default=0)
@click.option("--time_done", "-t", type=click.INT, default=0)
@click.option("--status", "-s", type=click.Choice(["active", "inactive"]), default="active")
@click.option("--force", "-f", is_flag=True, help="Force existing project overwrite.", default=False)
def add(name, duration, status, force, time_done):
    """Add a new project."""
    if duration < 0:
        print("[red]Error: Duration must be a positive integer.[/red]")
        return
    project_data = {
        "name": name,
        "time_done": time_done,
        "duration": duration,
        "status": status
    }
    save_to_json("./data/projects.json", name, "project", project_data, overwrite=force)

@project.command()
@click.option("--status", "-s", type=click.Choice(["active", "inactive"]))
def list(status):
    """List projects."""
    projects = json_fetch("./data/projects.json", "project")
    if not projects: return print(f"[red]No projects found.[/red]")
    
    if status:
        projects = {k: v for k, v in projects.items() if v["status"] == status}
        if not projects: return print(f"[red]No projects found with status '{status}'[/red]")
    
    # Create a table to display the projects
    table = Table(title="Projects")
    #table.add_column("ID", justify="left", style="cyan")
    table.add_column("Name", justify="left", style="magenta")
    table.add_column("Duration", justify="right", style="green")
    table.add_column("Time Done", justify="right", style="green")
    table.add_column("Status", justify="center", style="yellow")
    table.add_column("Element Type", justify="center", style="blue")
    for project_id, project in projects.items():
        table.add_row(
            #project_id,
            project["name"],
            str(project["duration"]),
            str(project["time_done"]),
            project["status"],
            project["element_type"]
        )
    console = Console()
    console.print(table)

@project.command()
@click.argument('names', type=click.STRING, nargs=-1)
@click.option("--force", "-f", is_flag=True, help="Force existing project overwrite.", default=False)
def delete(force, names : tuple):
    """Delete projects."""
    if not names:
        print("[red]Error: No project names provided.[/red]")
        return
    # Check if the user wants to delete all projects
    if "all" in names:
        input = Prompt.ask(
            "[yellow]Warning: You are about to delete all projects.\nDo you want to proceed (y/N)?[/yellow]",
            choices=["y", "n"],
            default="n", show_default=False, show_choices=False
        )
        if input == "n":
            print("[red]Operation cancelled.[/red]")
            return
        json_delete("./data/projects.json", names, force=force)
    else:
        json_delete("./data/projects.json", names, force=force)



#############################################
#            SESSSION FUNCTIONS             #
#############################################
@cli.group()
def session():
    """Manage sessions."""
    pass

@session.command()
@click.argument('project', type=click.STRING)
@click.argument('name', type=click.STRING)
@click.option("--duration", "-d", type=click.INT, default=0)
@click.option("--date", "-t", type=click.STRING, default="today")
def add(project, name, duration, date):
    """Add a new session."""
    if date == "today":
        date = datetime.now().strftime("%Y-%m-%d")
    else:
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            print("[red]Error: Invalid date format. Use YYYY-MM-DD.[/red]")

    session_id = f"{name}_{date}_{duration}"
    session_data = {
        "name": name,
        "project": project,
        "duration": duration,
        "date": date,
    }
    add_out = add_session_to_project(session_id, project, element_type="session")
    



if __name__ == "__main__":
    cli()