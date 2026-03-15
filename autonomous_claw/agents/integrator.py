import time
from rich.console import Console
from autonomous_claw.memory.json_store import load_state
from autonomous_claw.agents.developer import process_next_task
from autonomous_claw.agents.qa_engineer import review_recent_task

console = Console()

def run_autonomous_loop(max_iterations: int = 5):
    """
    The 'Integrator' loop. It automatically orchestrates the Dev/QA loop without human input.
    """
    console.print("[bold purple]Integrator Agent taking control of the Autonomous Sprint Loop...[/bold purple]")
    
    for iteration in range(max_iterations):
        state = load_state()
        if not state or state.get("status") != "active":
            console.print("[bold yellow]Sprint is not active.[/bold yellow]")
            break

        tasks = state.get("tasks", [])
        
        # Check if all tasks are verified
        all_verified = all(t.get("status") == "verified" for t in tasks)
        if all_verified and tasks:
            console.print("[bold green]All tasks in the Sprint are VERIFIED! Sprint Complete.[/bold green]")
            state["status"] = "completed"
            from autonomous_claw.memory.json_store import save_state
            save_state(state)
            break
            
        # Determine next logical step based on state machine
        needs_dev = any(t.get("status") in ["todo", "failed"] for t in tasks)
        needs_qa = any(t.get("status") == "done" and t.get("qa_approved") is not True for t in tasks)

        if needs_dev:
            console.print(f"\n[bold blue]=== Iteration {iteration + 1}: Developer Agent Triggered ===[/bold blue]")
            result = process_next_task()
            console.print(result)
        elif needs_qa:
            console.print(f"\n[bold magenta]=== Iteration {iteration + 1}: QA Engineer Triggered ===[/bold magenta]")
            result = review_recent_task()
            console.print(result)
        else:
            console.print("[yellow]No tasks in actionable states. Reviewing sprint logic.[/yellow]")
            break
            
        # Brief pause between agent actions to prevent rate-limit spam and give read time
        time.sleep(2)
        
    console.print("\n[bold purple]Integrator finished autonomous loop.[/bold purple]")
