import typer
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

from autonomous_claw.agents.product_owner import generate_sprint_backlog
from autonomous_claw.core.utils import extract_json_from_markdown
from autonomous_claw.memory.json_store import init_new_sprint, load_state

app = typer.Typer(help="AutonomousClaw: A Zero-Human Software Development Orchestrator")
console = Console()

@app.command()
def start(prompt: str = typer.Argument(..., help="High-level project prompt (e.g., 'Build a task manager')")):
    """
    Initialize an Autonomous Sprint for a new or existing project.
    """
    console.print(Panel(f"[bold green]Starting Autonomous Sprint[/bold green]\nTarget: {prompt}", title="AutonomousClaw", expand=False))
    console.print("[cyan]The Product Owner is breaking down the prompt into a sprint backlog...[/cyan]")
    
    # Run the PO agent
    backlog_response = generate_sprint_backlog(prompt)
    
    try:
        # Parse into persistent state
        parsed_backlog = extract_json_from_markdown(backlog_response)
        init_new_sprint(parsed_backlog)
        console.print("[bold green]Sprint Backlog saved to local state successfully![/bold green]")
    except Exception as e:
        console.print(f"[bold red]Failed to parse Product Owner Output into JSON: {e}[/bold red]")
    
    # Render final output for human
    console.print(Panel(Markdown(backlog_response), title="Product Owner Agent - Sprint Backlog", border_style="blue"))

@app.command()
def status():
    """
    View the current status of the global context, agents, and sprint tracking.
    """
    state = load_state()
    if not state or state.get("status") != "active":
        console.print("[bold yellow]System Status:[/bold yellow] No active sprint.")
        return

    console.print(f"[bold green]Sprint Goal:[/bold green] {state.get('sprint_goal')}")
    console.print("[bold cyan]Tasks:[/bold cyan]")
    for idx, task in enumerate(state.get("tasks", [])):
        status_color = "green" if task.get("status") == "done" else "yellow" if task.get("status") == "in_progress" else "red"
        console.print(f" {idx + 1}. ({task.get('assigned_agent')}) [{status_color}]{task.get('status', 'todo').upper()}[/{status_color}] - {task.get('title')}")


from autonomous_claw.agents.developer import process_next_task
from autonomous_claw.agents.integrator import run_autonomous_loop

@app.command()
def act():
    """
    Commands the Developer Agent to look at 'our plan' and use the code skill to implement the next single task.
    """
    console.print(Panel("[bold green]Agent triggered to ACT on our plan...[/bold green]", title="Developer Agent", expand=False))
    result = process_next_task()
    console.print(result)

@app.command()
def auto(iterations: int = 5):
    """
    Triggers the Integrator Agent to run the Zero-Human Autonomous Sprint loop (Dev -> QA -> Repeat) up to `iterations` times.
    """
    run_autonomous_loop(max_iterations=iterations)

@app.command()
def config():
    """
    Configure LLM providers and local paths.
    """
    console.print("Configuration UI goes here.")

if __name__ == "__main__":
    app()
