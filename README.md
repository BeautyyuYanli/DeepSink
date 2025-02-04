# DeepSink

```bash
pdm sync
```

## Data Generation

Using OpenRouter to generate data.

Env to set:
- `HF_TOKEN`
- `OPENAI_API_KEY`
- `OPENAI_BASE_URL`

```bash
python -m deepsink.scripts.data_pipe --help
python -m deepsink.scripts.data_pipe build --batch-num 1 --save-local ./output --no-append beautyyuyanli/deep-sink-data
```

