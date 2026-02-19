import json
import logging
from dotenv import load_dotenv

load_dotenv()

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, RichLog, Button, LoadingIndicator, Static
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.worker import Worker, WorkerState
from agent.graph import agent
from agent.prediction import train_and_predict

logging.basicConfig(level=logging.ERROR)


def extract_json(text: str) -> dict:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    start = text.find('{')
    end = text.rfind('}')
    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(text[start:end + 1])
        except json.JSONDecodeError:
            pass

    return {"orders": [], "error": "could not parse model response", "raw": text[:200]}


def run(query: str) -> str:
    result = agent.invoke({"messages": [("user", query)]})

    output = ""
    for msg in reversed(result["messages"]):
        if msg.content and msg.content.strip():
            output = msg.content
            break

    return json.dumps(extract_json(output), indent=2)


def build_stats_panel() -> str:
    s = train_and_predict()
    return (
        f"[bold white]📊 Order Intelligence[/bold white]\n"
        f"──────────────────────\n"
        f"[cyan]Predicted Next Order:[/cyan]  [bold yellow]${s['predicted_next_order']}[/bold yellow]\n"
        f"[cyan]Trend:[/cyan]                 {s['trend']}\n"
        f"[cyan]Avg Order Total:[/cyan]       [green]${s['average_order_total']}[/green]\n"
        f"[cyan]R² Score:[/cyan]              {s['r_squared']}\n"
        f"[cyan]Orders Analyzed:[/cyan]       {s['orders_analyzed']}\n"
        f"──────────────────────\n"
        f"[dim]linear regression over\norders 1001 → 1025[/dim]"
    )


class RaftApp(App):
    CSS = """
    Screen { background: #1a1a2e; }
    #main-layout { height: 100%; }
    #left-panel { width: 75%; height: 100%; }
    #right-panel {
        width: 25%;
        height: 100%;
        border: solid #4a4a8a;
        margin: 1;
        padding: 1;
    }
    #log {
        border: solid #4a4a8a;
        margin: 1;
        padding: 1;
        height: 80%;
    }
    #query  { border: solid #4a4a8a; margin: 1; width: 65%; }
    #submit { margin: 1; width: 14%; }
    #clear  { margin: 1; width: 14%; }
    #spinner { height: 1; margin-left: 2; display: none; }
    #spinner.visible { display: block; }
    Horizontal { height: auto; }
    LoadingIndicator { height: 1; }
    """

    BINDINGS = [Binding("ctrl+c", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Horizontal(id="main-layout"):
            with Vertical(id="left-panel"):
                yield RichLog(id="log", markup=True)
                with Horizontal():
                    yield LoadingIndicator(id="spinner")
                with Horizontal():
                    yield Input(placeholder="Enter your order query...", id="query")
                    yield Button("Submit", id="submit", variant="primary")
                    yield Button("Clear", id="clear", variant="error")
            with Vertical(id="right-panel"):
                yield Static(build_stats_panel(), id="stats", markup=True)
        yield Footer()

    def on_mount(self):
        log = self.query_one("#log", RichLog)
        log.write("[bold green]Raft Order Agent ready.[/bold green]")
        log.write("[dim]25 orders loaded — try: 'Show Ohio orders over $500' or 'Show all orders from Texas'[/dim]\n")
        self.query_one(Input).focus()

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "clear":
            log = self.query_one("#log", RichLog)
            log.clear()
            log.write("[bold green]Log cleared.[/bold green]")
        elif event.button.id == "submit":
            self._submit_query()

    def on_input_submitted(self, event: Input.Submitted):
        self._submit_query()

    def _submit_query(self):
        query = self.query_one(Input).value.strip()
        if not query:
            return

        log = self.query_one("#log", RichLog)
        log.write(f"[bold yellow]Query:[/bold yellow] {query}")
        self.query_one(Input).value = ""
        self.query_one(Input).disabled = True
        self.query_one("#submit", Button).disabled = True
        self.query_one("#spinner").add_class("visible")

        def do_run(q=query):
            return run(q)

        self.run_worker(do_run, exclusive=True, thread=True, name=query)

    def on_worker_state_changed(self, event: Worker.StateChanged):
        if event.state == WorkerState.SUCCESS:
            result = event.worker.result
            log = self.query_one("#log", RichLog)

            try:
                orders = json.loads(result).get("orders", [])
                if orders:
                    total_val = sum(o.get("total", 0) for o in orders)
                    avg_val = total_val / len(orders)
                    log.write(
                        f"[bold green]✓ {len(orders)} order(s) found[/bold green] | "
                        f"[cyan]Total: ${total_val:,.2f}[/cyan] | "
                        f"[cyan]Avg: ${avg_val:,.2f}[/cyan]"
                    )
                else:
                    log.write("[dim]No orders matched.[/dim]")
            except Exception:
                pass

            log.write(f"[bold cyan]Result:[/bold cyan]\n{result}\n")
            self._reset_ui()

        elif event.state == WorkerState.ERROR:
            self.query_one("#log", RichLog).write(f"[bold red]Error:[/bold red] {event.worker.error}")
            self._reset_ui()

    def _reset_ui(self):
        self.query_one("#spinner").remove_class("visible")
        self.query_one(Input).disabled = False
        self.query_one("#submit", Button).disabled = False
        self.query_one(Input).focus()


if __name__ == "__main__":
    RaftApp().run()