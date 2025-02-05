import asyncio
from datetime import datetime
import json
import os
import typer
from deepsink.scripts.data_gen import build_pipeline
from deepsink.scripts.data_upload import upload_to_hub
from datasets import Dataset, load_dataset
from rich.console import Console
from rich.table import Table

app = typer.Typer(pretty_exceptions_enable=False)


async def _upload(dataset: Dataset, repo_name: str, append: bool = False):
    max_retries = 5
    for attempt in range(max_retries):
        try:
            upload_to_hub(dataset, repo_name, append=append)
            break
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            print(f"Upload attempt {attempt + 1} failed: {str(e)}")
            print(f"Retrying... ({attempt + 2}/{max_retries})")
            await asyncio.sleep(2**attempt)


@app.command()
def build(
    repo_name: str,
    batch_num: int = typer.Option(32, help="Number of batches to generate"),
    batch_size: int = typer.Option(4, help="Size of each batch"),
    save_local: str | None = typer.Option(
        None,
        help="Directory to save intermediate batches. If None, batches are not saved locally",
    ),
    append: bool = typer.Option(True, help="Whether to append to existing dataset"),
):
    """
    Generate synthetic data and upload it to Hugging Face Hub.
    If save_local is provided, saves intermediate batches to the specified directory.
    """

    async def _async_build():
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        batch: list[tuple[str, str, str]] = []

        # Create local save directory if specified
        if save_local:
            save_dir = os.path.join(save_local, timestamp.replace(":", "_"))
            os.makedirs(save_dir, exist_ok=True)

        for i in range(batch_num):
            print(f"Building batch {i}...")
            temp_batch = await asyncio.gather(
                *[build_pipeline() for _ in range(batch_size)], return_exceptions=True
            )
            for item in temp_batch:
                if isinstance(item, BaseException):
                    print(f"Error in batch {i}: {item}")
                    continue
            temp_batch = [
                item for item in temp_batch if not isinstance(item, BaseException)
            ]
            batch.extend(temp_batch)

            # Save intermediate batch as JSON if save_local is specified
            if save_local:
                batch_data = [
                    {
                        "topic": item[0],
                        "think": item[1],
                        "content": item[2],
                    }
                    for item in temp_batch
                ]
                json_path = os.path.join(save_dir, f"batch_{i}.json")  # type: ignore
                with open(json_path, "w", encoding="utf-8") as f:
                    json.dump(batch_data, f, ensure_ascii=False, indent=2)

        # Create final dataset
        batch_dataset = Dataset.from_dict(
            {
                "topic": [item[0] for item in batch],
                "think": [item[1] for item in batch],
                "content": [item[2] for item in batch],
                "type": ["synthetic"] * len(batch),
                "datetime": [timestamp] * len(batch),
            }
        )

        await _upload(batch_dataset, repo_name, append=append)

    asyncio.run(_async_build())


@app.command()
def recover(
    repo_name: str,
    local_dir: str = typer.Argument(..., help="Directory containing saved batch files"),
    append: bool = typer.Option(True, help="Whether to append to existing dataset"),
):
    """
    Recover data from locally saved batch files and upload to Hugging Face Hub.
    Expects JSON files in the format saved by the main command.
    """

    async def _async_recover():
        if not os.path.exists(local_dir):
            raise typer.BadParameter(f"Directory {local_dir} does not exist")

        batch_files = [f for f in os.listdir(local_dir) if f.endswith(".json")]
        if not batch_files:
            raise typer.BadParameter(f"No JSON files found in {local_dir}")

        all_data = []
        timestamp = os.path.basename(local_dir).replace("_", ":")

        for batch_file in batch_files:
            file_path = os.path.join(local_dir, batch_file)
            with open(file_path, "r", encoding="utf-8") as f:
                batch_data = json.load(f)
                all_data.extend(batch_data)

        # Create dataset from recovered data
        batch_dataset = Dataset.from_dict(
            {
                "topic": [item["topic"] for item in all_data],
                "think": [item["think"] for item in all_data],
                "content": [item["content"] for item in all_data],
                "type": ["synthetic"] * len(all_data),
                "datetime": [timestamp] * len(all_data),
            }
        )

        await _upload(batch_dataset, repo_name, append=append)

    asyncio.run(_async_recover())


@app.command()
def sample(
    repo_name: str,
    n_samples: int = typer.Option(1, help="Number of samples to display"),
):
    """
    Download dataset from Hugging Face Hub and display sample entries.
    """

    async def _async_sample():
        try:
            dataset: Dataset = load_dataset(repo_name)["train"]  # type: ignore

            # Get total dataset size
            total_size = len(dataset)
            console = Console()
            console.print(
                f"\nTotal entries in dataset: {total_size}", style="bold green"
            )

            # Ensure n_samples doesn't exceed dataset size
            rel_n_samples = min(n_samples, total_size)

            console.print(
                f"\nDisplaying {rel_n_samples} sample(s):\n", style="bold blue"
            )

            # Create table with columns for each field
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Topic", style="cyan")
            table.add_column("Think", style="cyan")
            table.add_column("Content", style="cyan")
            table.add_column("Type", style="cyan")
            table.add_column("Datetime", style="cyan")

            # Add rows for each sample
            for i in range(rel_n_samples):
                sample = dataset[i]
                table.add_row(
                    sample["topic"],
                    sample["think"],
                    sample["content"],
                    sample["type"],
                    sample["datetime"],
                )

            console.print(table)

        except Exception as e:
            console = Console()
            console.print(f"Error loading dataset: {str(e)}", style="bold red")

    asyncio.run(_async_sample())


@app.command()
def to_csv(
    repo_name: str,
    output_path: str = typer.Argument(..., help="Path to save the CSV file"),
):
    """
    Download dataset from Hugging Face Hub and save it as a CSV file.
    Combines 'think' and 'content' into a formatted 'output' column.
    """
    try:
        dataset: Dataset = load_dataset(repo_name)["train"]  # type: ignore

        # Transform the dataset to create the new output column
        def format_output(example):
            return {
                "topic": example["topic"],
                "output": f"<think>\n{example['think']}\n</think>\n\n{example['content']}",
            }

        dataset = dataset.map(format_output)
        dataset = dataset.select_columns(["topic", "output"])

        # Ensure the output directory exists
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

        # Convert to CSV
        dataset.to_csv(output_path, index=False)

        console = Console()
        console.print(
            f"\nDataset successfully saved to: {output_path}", style="bold green"
        )
        console.print(f"Total entries saved: {len(dataset)}", style="bold green")

    except Exception as e:
        console = Console()
        console.print(f"Error converting dataset to CSV: {str(e)}", style="bold red")


if __name__ == "__main__":
    app()
