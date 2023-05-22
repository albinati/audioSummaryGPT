# main.py

import sys
sys.path.append('./transcriber')
sys.path.append('./summarizer')

from transcriber import transcribe
from summarizer import summarize

def main():
    print("Starting transcription...")
    transcribe()

    print("\nStarting summarization...")
    summarize()

    print("\nSummarization completed.")

if __name__ == "__main__":
    main()
