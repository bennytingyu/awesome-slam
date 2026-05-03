# image-gen-comparison

Python toolkit + thin UI for comparing text-to-image generation between:

- Gemini image generation ("Nano Banana")
- GPT Image 2

## What is included

- `client.py`: backend Python library for provider API calls.
- `app.py`: Streamlit frontend with prompt chat input and two image canvases.
- `requirements.txt`: Python dependencies.
- `.env.example`: expected API key names.

## Setup

1. Create and activate a Python virtual environment.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set API keys:

   ```bash
   export GEMINI_API_KEY="..."
   export OPENAI_API_KEY="..."
   ```

## Run the UI

```bash
streamlit run app.py
```

Type a prompt in the chat input. The app calls both backends and displays both
images side-by-side for comparison.

## Notes

- This project currently targets:
  - Gemini model name default: `gemini-3-pro-image-generation-preview`
  - GPT model name default: `gpt-image-2`
- You can adjust model names in `ImageGenerationClient` as provider naming
  evolves.
