import os
import json
from rich import print
from rich.prompt import Prompt

def read_json(file):
    """Read data from a JSON file."""
    if os.path.exists(file):
        with open(file, "r") as f:
            existing_data = json.load(f)
    else:
        existing_data = {}
    return existing_data

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

def add_to_json(file, element_id, element_type, data, overwrite=False):
    """Add data to a JSON file."""
    existing_data = read_json(file)
    # Check if the element ID already exists
    if element_id in existing_data and not overwrite:
        # Prompt the user for confirmation
        input = Prompt.ask(
            f"[yellow]Warning: {element_type} - {element_id} already exists. Do you want to overwrite it (y/N)?[/yellow]",
            choices=["y", "n"],
            default="n", show_default=False, show_choices=False
        )
        if input == "y":
            print("[green]Overwriting existing data...[/green]")
        elif input == "n":
            print("[red]Operation cancelled.[/red]")
            return
    # Add the new data
    data["element_type"] = element_type
    existing_data[element_id] = data
    # Save the updated data to the file
    save_json(file, existing_data)    
    print(f"[green]{element_type.capitalize()} {element_id} added successfully.[/green]")

def add_to_project(session_id, project_id, duration, element_type="session"):
    """Add a session to a project."""
    projects_json = json_fetch("./data/projects.json", "project")
    if project_id not in projects_json:
        print(f"[red]Error: Project {project_id} not found.[/red]")
        return False
    if element_type == 'session':
        print(f"[green]Adding session {session_id} to project {project_id}...[/green]")
        print(f"[green]Duration: {duration} minutes[/green]")
        projects_json[project_id]["sessions"].append(session_id)
        projects_json[project_id]["time_done"] += duration
    else:
        return False # Add functionality for other element types
    save_json("./data/projects.json", projects_json)
    #save_to_json("./data/projects.json", project_id, "project", projects, overwrite=True)
    return True


def json_delete(file, element_ids, force=False):
    """Delete data from a JSON file."""
    if element_ids is None or len(element_ids) == 0:
        print("[red]Error: No element IDs provided.[/red]")
    if os.path.exists(file):
        with open(file, "r") as f:
            data = json.load(f)
        if force == False:
            Prompt.ask(
             f"[yellow]Warning: You are about to delete {len(element_ids)} elements.\nDo you want to proceed (y/N)?[/yellow]",
                choices=["y", "n"],
                default="n", show_default=False, show_choices=False
            )
        if input == "n":
            print("[red]Operation cancelled.[/red]")
            return
        # Delete the specified elements
        for element_id in element_ids:
            if element_id in data:
                del data[element_id]
                print(f"[green]{element_id} deleted successfully.[/green]")
            else:
                print(f"[red]Error: {element_id} not found.[/red]")
        with open(file, "w") as f:
            json.dump(data, f, indent=4)
    else:
        print("[red]No data found.[/red]")


def json_fetch(file, element_type='any'):
    """List data from a JSON file."""
    if os.path.exists(file):
        with open(file, "r") as f:
            data = json.load(f)
            if element_type != 'any':
                data = {k: v for k, v in data.items() if v["element_type"] == element_type}
    else:
        print("[red]No data found.[/red]")
    return data

def delete_project_content(project, element_type="session"):
    """Delete an element from a project."""
    projects_json = json_fetch("./data/projects.json", "project")
    if project not in projects_json:
        print(f"[red]Error: Project {project} not found.[/red]")
        return False
    if element_type == 'session':
        print(f"[green]Deleting all sessions from project {project}...[/green]")
        projects_json[project]["sessions"] = []
        projects_json[project]["time_done"] = 0
    else:
        pass # Add functionality for other element types
    save_json("./data/projects.json", projects_json)


def progress_bar(duration, done):
    perc_done = (done / duration) * 100
    bar_length = 30
    block = int(round(bar_length * perc_done / 100))
    progress = "#" * block + " " * (bar_length - block)
    return f"|{progress}| {perc_done:.0f}% "