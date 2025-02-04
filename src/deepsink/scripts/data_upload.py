from datasets import Dataset, concatenate_datasets, load_dataset
import numpy as np
from huggingface_hub import login, HfApi
import pandas as pd
import typer
from datetime import datetime
import os
from typing import Optional


def generate_sample_data(num_samples: int = 100) -> pd.DataFrame:
    """Generate synthetic data for demonstration."""
    print(f"Generating {num_samples} sample data points...")
    data = {
        "text": [f"Sample text {i}" for i in range(num_samples)],
        "label": np.random.randint(0, 2, num_samples),
        "score": np.random.random(num_samples),
    }
    print("Sample data generation complete")
    return pd.DataFrame(data)


def upload_to_hub(
    dataset: Dataset,
    repo_name: str,
    token: Optional[str] = None,
    append: bool = False,
) -> None:
    """Upload dataset to Hugging Face Hub.

    Args:
        dataset: Dataset to upload
        repo_name: Repository name on HuggingFace (format: username/repo-name)
        token: HuggingFace API token
        append: If True, append to existing dataset instead of overwriting
    """
    print("Preparing to upload dataset to Hugging Face Hub...")

    # Try to get token from env if not provided
    token = token or os.getenv("HF_TOKEN")
    if not token:
        raise ValueError(
            "Hugging Face token not found. Please provide it via --token argument or set HF_TOKEN environment variable"
        )

    print("Logging in to Hugging Face...")
    login(token)

    try:
        if append:
            try:
                print(f"Attempting to load existing dataset {repo_name}...")
                existing_dataset: Dataset = load_dataset(repo_name)["train"]  # type: ignore
                print(f"Concatenating new data with existing dataset...")
                dataset = concatenate_datasets([existing_dataset, dataset])
            except Exception as e:
                print(
                    f"Warning: Could not load or append to existing dataset: {str(e)}"
                )
                print("Proceeding with uploading new dataset only")

        print(f"Uploading dataset {repo_name}...")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        commit_message = (
            f"{'Append to' if append else 'Update'} dataset - version {timestamp}"
        )
        dataset.push_to_hub(
            repo_name,
            commit_message=commit_message,
        )
        print(f"Dataset {repo_name} uploaded successfully")
    except Exception as e:
        print(f"Error during upload: {str(e)}")
        raise  # Re-raise other exceptions


def main(
    repo_name: str,
    num_samples: int = typer.Option(100, help="Number of samples to generate"),
    token: Optional[str] = typer.Option(
        None,
        help="HuggingFace API token. If not provided, will read from HF_TOKEN environment variable",
    ),
    append: bool = typer.Option(
        False, help="Whether to append to existing dataset instead of overwriting"
    ),
) -> None:
    """
    Generate a sample dataset and upload it to HuggingFace Hub.

    Example usage:
    python upload_data.py --repo-name="username/my-dataset"
    """
    print("\n=== Starting Dataset Generation and Upload Process ===\n")

    # Generate sample data
    df = generate_sample_data(num_samples)

    print("\nConverting DataFrame to HuggingFace Dataset format...")
    # Convert to HuggingFace Dataset
    dataset = Dataset.from_pandas(df)

    # Upload to HuggingFace Hub
    upload_to_hub(dataset, repo_name, token, append)
    print(f"\n✨ Dataset successfully uploaded to {repo_name}")
    print("\n=== Process Complete ===\n")


if __name__ == "__main__":
    typer.run(main)
