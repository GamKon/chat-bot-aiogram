#https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.2

from transformers import AutoModelForCausalLM, AutoTokenizer, TextStreamer

async def Mistral_7B_Instruct_pipe(prompt_to_llm: str, max_new_tokens: int):

    if max_new_tokens <= 20 and max_new_tokens >= 2048: max_new_tokens = 256
    print("1----------------------------------------------prompt TO AWQ Mistral 7b-----------------------------------------")
    print(prompt_to_llm)
    print("2---------------------------------------------------------------------------------------------------------------")


    model_name_or_path = "mistralai/Mistral-7B-Instruct-v0.2"

    tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_name_or_path,
        low_cpu_mem_usage=True,
        device_map="cuda:0",
        trust_remote_code=True
    )

    # # Using the text streamer to stream output one token at a time
    # streamer = TextStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)

    # prompt = "Tell me about AI"
    # prompt_template=f'''<s>[INST] {prompt} [/INST]
    # '''

    prompt_template = prompt_to_llm

    # Convert prompt to tokens
    tokens = tokenizer(
        prompt_template,
        return_tensors='pt'
    ).input_ids.cuda()

    generation_params = {
        "do_sample": True,
        "temperature": 0.7,
        "top_p": 0.95,
        "top_k": 40,
        "max_new_tokens": max_new_tokens,
        "repetition_penalty": 1.1
    }

    # # Generate streamed output, visible one token at a time
    # generation_output = model.generate(
    #     tokens,
    #     streamer=streamer,
    #     **generation_params
    # )

    # # Generation without a streamer, which will include the prompt in the output
    # generation_output = model.generate(
    #     tokens,
    #     **generation_params
    # )

    # # Get the tokens from the output, decode them, print them
    # token_output = generation_output[0]
    # text_output = tokenizer.decode(token_output)
    # print("model.generate output: ", text_output)

    # Inference is also possible via Transformers' pipeline
    from transformers import pipeline

    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        **generation_params
    )

    pipe_output = pipe(prompt_template)[0]['generated_text']
    #print("pipeline output: ", pipe_output)

    llm_reply = str(pipe_output.split('[/INST] ')[-1]).split('</s>')[0]
    print("3----------------------------------------------RAW output FROM AWQ Mistral 7B-----------------------------------")
    print(pipe_output)
    print("4---------------------------------------------SPLIT output FROM AWQ Mistral 7B----------------------------------")
    print(llm_reply)
    print("5---------------------------------------------------------------------------------------------------------------")
    return str(llm_reply)