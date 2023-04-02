from rich.console import Console
from rich.table import Table


def show_list_dict(data: list[dict[str, any]]):
    if not data:
        return
    elif not isinstance(data[0], dict):
        return

    table = Table()
    header = list(data[0].keys())
    for column in header:
        table.add_column(column)

    for row in data:
        table.add_row(*[str(item) for item in row.values()])

    console = Console()
    console.print(table)
