# Summarizer Script

This script is used to generate a summary from a given text using OpenAI's GPT models.

## Setup

Before running this script, please ensure you have configured the following environment variables in your `.env` file:

- `OPENAI_KEY`: Your OpenAI API key.
- `OUTPUT_FOLDER`: The directory where the transcript file is located and the summary will be saved.
- `OUTPUT_FILENAME`: The name of the output summary file (without extension).
- `TRANSCRIPT_FILENAME`: The name of the transcript file (without extension).
- `CHUNK_FILENAME`: The base name for chunk files.
- `USER_PROMPT1` and `USER_PROMIPMT2`: Prompts used to guide the summarization.
- `AI_ROLE`: The role of the AI during the conversation.
- `GPT_MODEL`: The name of the GPT model to use for summarization.
- `GPT_TEMP`: The temperature parameter used in the GPT model.

## Usage

You can run the summarizer script with the following command:

```bash
python summarizer.py
