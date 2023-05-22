from dotenv import load_dotenv
import os
import pathlib
import openai
import tiktoken

def summarize():


    # Load the .env file
    load_dotenv(pathlib.Path(__file__).parent.parent / '.env')

    # Get all necessary parameters from .env file
    openai.api_key = os.getenv('OPENAI_KEY')
    output_folder = os.getenv('OUTPUT_FOLDER')
    output_filename = os.getenv('OUTPUT_FILENAME')
    transcript_filename = os.getenv('TRANSCRIPT_FILENAME') 
    chunk_filename = os.getenv('CHUNK_FILENAME') 
    user_prompt1 = os.getenv('USER_PROMPT1')
    user_prompt2 = os.getenv('USER_PROMPT2')
    ai_role = os.getenv('AI_ROLE')
    gpt_model = os.getenv('GPT_MODEL')
    gpt_temp = float(os.getenv('GPT_TEMP'))  # Convert to float

    # Set encoding type for tiktoken
    encoding = tiktoken.encoding_for_model(gpt_model)
    response_token_limit = 1000
    # Create output and content directory if it does not exist
    try: 
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
    except Exception as e:
        print(f"Error creating directories: {e}")
        exit(1)

    # Define the maximum token limit based on model selection
    model_token_limit = {
        'gpt-3.5-turbo': 4096,
        'gpt-4': 8192
    }
    # Define function to count tokens for ChatGPT
    def count_tokens(text):        
        return len(encoding.encode(text))

    # Get the maximum token limit for the chosen model or default to 4096
    limit_tokens = model_token_limit.get(gpt_model, 4096)
    max_tokens = limit_tokens - count_tokens(ai_role) - count_tokens(user_prompt1) - count_tokens(user_prompt2) - response_token_limit
    
    # Function to save chunks to files
    def save_chunks(chunks, base_filename):
        for i, chunk in enumerate(chunks):
            with open(f'{base_filename}_{i}.txt', 'w') as f:
                print("Saving file for chunk ["+ str(i) +"]")  # Convert 'i' to string
                f.write(chunk)

    # Define function to chunk text based on token count
    def chunk_text(text, max_tokens):
        words = text.split(' ')
        chunks = []
        current_chunk = ''

        # Iterate over all words
        for word in words:
            # If adding the word would exceed max tokens, add current chunk to chunks
            if count_tokens(current_chunk + ' ' + word) > max_tokens:
                chunks.append(current_chunk)
                current_chunk = word
            else:
                # If not, add the word to current chunk
                current_chunk += ' ' + word

        # Add the final chunk to chunks
        chunks.append(current_chunk)

        return chunks

    # Load the transcript file, chunk it and save the chunks to files
    try:
        with open(os.path.join(output_folder, transcript_filename+'.txt'), "r") as transcript_file:
            transcript = transcript_file.read()
            transcript_chunks = chunk_text(transcript, max_tokens)
            save_chunks(transcript_chunks, os.path.join(output_folder, chunk_filename))
    except FileNotFoundError:
        print("Transcript file does not exist. Please fix this and rerun the script.")
        exit(1)
    
    # Process each text chunk file
    try:
        files = [filename for filename in os.listdir(output_folder) 
             if filename.startswith(chunk_filename) and filename.endswith(".txt")]
        files_sorted = sorted(files, key=lambda x: int(x.split('_')[-1].split('.')[0]))
        for filename in files_sorted:
            if filename.startswith(chunk_filename) and filename.endswith(".txt"):
                filepath = os.path.join(output_folder, filename)
                with open(filepath, "r", encoding='utf-8') as f:
                    chunk_text = f.read()
                    print("Processing: "+ str(filepath))
                    # Call OpenAI API for initial summarization
                    response = openai.ChatCompletion.create(
                        model=gpt_model,
                        temperature=gpt_temp,
                        messages=[
                            {"role": "system", "content": ai_role},
                            {"role": "user", "content": f'{user_prompt1}: '+ chunk_text},                            
                        ]
                    )                    
                    # Append response to output file
                    summary_text = response['choices'][0]['message']['content']
                    with open(f'{output_folder}/{output_filename}.txt', 'a') as f:
                        f.write(summary_text)                    
                        
    except FileNotFoundError:
        print("Input file or folder does not exist. Please fix this and rerun the script.")
        exit(1)
    pass

    # Call OpenAI API for second summarization
    ai_role = "Você é especialista em reunir informações já pre-resumidas para entregar um contexto claro e objetivo."                
    user_prompt2 = "Organize as informações a seguir agrupadas por contexto mantendo os dados e fatos relevantes: "
    user_prompt1 = "Corrija possíveis erros de transcrição caso exista"
    
    response = openai.ChatCompletion.create(
        model=gpt_model,
        temperature=gpt_temp,
        messages=[
            {"role": "system", "content": ai_role},            
            {"role": "user", "content": user_prompt1},
            {"role": "user", "content": f'{user_prompt2}: '+ summary_text},
        ]
    )

    # Append response to output file
    with open(f'{output_folder}/{output_filename}_summarized.txt', 'w') as f:
        f.write(response['choices'][0]['message']['content'])       