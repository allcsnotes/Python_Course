from rich.console import Console
from rich.table import Table

table = Table(title="Courses")
table.add_column("Course")
table.add_column("Price")
table.add_row("Python", "999")
table.add_row("SQL Basics", "499")

console = Console()
console.print(table)
