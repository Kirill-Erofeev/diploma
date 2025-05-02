import re
import os
import torch
import transformers
import datetime
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig, TextStreamer
from auto_gptq import AutoGPTQForCausalLM

from app.core.config import settings

def answer_the_question_1():
    start = datetime.datetime.now()
    model_name = "TheBloke/Mistral-7B-Instruct-v0.1-GPTQ"
    # model_name = "TheBloke/Mistral-7B-Instruct-v0.2-GPTQ"
    # model_name = "deepseek-ai/DeepSeek-V3-0324"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    model = AutoGPTQForCausalLM.from_quantized(
        model_name, 
        # device="cuda:0", 
        use_triton=False, 
        quantize_config=None
    )
    model.to(device)
    def generate_response(prompt):
        inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
        outputs = model.generate(**inputs, max_new_tokens=200)
        return tokenizer.decode(outputs[0], skip_special_tokens=True)
    response = generate_response("Какого цвета жабы?")
    finish = datetime.datetime.now()
    print(f"Модель: {model_name}")
    print(f"Время:{str(finish - start)}")
    print(f"Текст: {response}")
    

def answer_the_question_2():
    start = datetime.datetime.now()
    model_name = "TheBloke/Mistral-7B-Instruct-v0.1-GPTQ"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        # device_map="auto",         # Автоматически использует GPU
        torch_dtype=torch.float16, # Использует float16 для ускорения
        trust_remote_code=True
    )
    model.to(device)
    question = "Как установить питон?"
    inputs = tokenizer(question, return_tensors="pt").to("cuda")
    outputs = model.generate(**inputs, max_new_tokens=100)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    finish = datetime.datetime.now()
    print(f"Модель: {model_name}")
    print(f"Время:{str(finish - start)}")
    print(f"Текст: {response}")


def answer_the_question_3():
    start = datetime.datetime.now()
    model_name = "sambanovasystems/SambaLingo-Russian-Chat"
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)
    model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", torch_dtype="auto")
    pipe = transformers.pipeline("text-generation", model=model_name, device_map="auto", use_fast=False)
    messages = [
        {
            "role": "user",
            "content": "Кто такие жабы?"
            # "content": "Как установить питон?</s>"""
        },
    ]
    prompt = pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    outputs = pipe(prompt, max_new_tokens=20, do_sample=False)[0]
    response = outputs["generated_text"]
    finish = datetime.datetime.now()
    print(f"Модель: {model_name}")
    print(f"Время:{str(finish - start)}")
    print(f"Текст: {response}")
    
    
def answer_the_question(prompt: str) -> str:
    # model_name = "SmallDoge/Doge-320M-Instruct"
    # prompt += " in 2-3 sentences"
    model_name = "SmallDoge"
    model_path = os.path.join(settings.lm_folder, model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(model_path, trust_remote_code=True)
    generation_config = GenerationConfig(
        max_new_tokens=300,
        use_cache=True,
        do_sample=False,
        temperature=0.8,
        top_p=0.9,
        repetition_penalty=1.0
    )
    steamer = TextStreamer(
        tokenizer=tokenizer, 
        skip_prompt=True
    )
    conversation = [
        {"role": "user", "content": prompt}
    ]
    inputs = tokenizer.apply_chat_template(
        conversation=conversation,
        tokenize=True,
        return_tensors="pt",
    )
    outputs = model.generate(
        inputs, 
        tokenizer=tokenizer,
        generation_config=generation_config, 
        streamer=steamer
    )
    full_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    match = re.search(r"assistant\s*(.*?)$", full_text, re.DOTALL | re.IGNORECASE)
    if match:
        answer_only = match.group(1).strip()
    else:
        answer_only = full_text.strip()
    return answer_only
    
    
def answer_the_question_5():
    start = datetime.datetime.now()
    generator = transformers.pipeline('text-generation', model='gpt2')
    transformers.set_seed(42)
    print(generator("What is Metallica?", max_length=30, num_return_sequences=5)[0]["generated_text"])


def answer_the_question_6():
    start = datetime.datetime.now()
    model_name = "gai-labs/strela"
    tokenizer = AutoTokenizer.from_pretrained("gai-labs/strela")
    model = AutoModelForCausalLM.from_pretrained("gai-labs/strela")

    prompt = "ИИ - "

    model_inputs = tokenizer([prompt], return_tensors="pt")
    generated_ids = model.generate(**model_inputs, max_new_tokens=64) # Настройте максимальное количество токенов для генерации
    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    finish = datetime.datetime.now()
    print(f"Модель: {model_name}")
    print(f"Время:{str(finish - start)}")
    print(f"Текст: {response}")


def answer_the_question_7():
    start = datetime.datetime.now()
    model_name = "q"
    from llama_cpp import Llama

    llm = Llama.from_pretrained(
        repo_id="RefalMachine/RuadaptQwen2.5-14B-R1-distill-preview-v1-GGUF",
        # filename="IQ4_XS.gguf",
        filename="Q2_K.gguf",
    )

    print(llm.create_chat_completion(
        messages = [
                {
                    "role": "user",
                    "content": "Какая столица Франции??"
                }
            ]
        )
    )
    finish = datetime.datetime.now()
    print(f"Модель: {model_name}")
    # print(f"Текст: {response}")
    print(f"Время:{str(finish - start)}")


def answer_the_question_8():
    # model = AutoModelForCausalLM.from_pretrained(
    #     "TheBloke/Mistral-7B-Instruct-v0.2-GGUF",
    #     model_file="mistral-7b-instruct-v0.1.Q4_0.gguf"
    # )
    model = AutoModelForCausalLM.from_pretrained(
        "TheBloke/Mistral-7B-Instruct-v0.2-GGUF",
        model_file="mistral-7b-instruct-v0.2.Q4_0.gguf"
    )
    response = model("Расскажи про жаб", stream=True)
    print("".join(response))


if __name__ == "__main__":
    # answer_the_question_1()
    answer_the_question_3()
    # answer_the_question_4("What is Metallica?")
    # ru_prompt = "Расскажи про Ленина."
    # en_prompt = translate_text(target_language="en", text=ru_prompt)
    # generated_en_text = answer_the_question(prompt=en_prompt)
    # generated_ru_text = translate_text(target_language="ru", text=generated_en_text)
    # print(generated_en_text)
    # print(generated_ru_text)
    # from transformers import AutoTokenizer

    # # Название модели
    # model_name = "SmallDoge/Doge-320M-Instruct"

    # # Загружаем токенизатор
    # tokenizer = AutoTokenizer.from_pretrained(model_name)

    # # Текст на английском
    # text = "Toads are amphibians belonging to the order Anura, which also includes frogs and newts. They are characterized by having moist, scaly skin, short legs, and a long tail. Toads are found in various parts of the world, including North America, Europe, Asia, and Australia. They are herbivores and feed on a variety of plants, including leaves, stems, and flowers. Toads are also carnivores and feed on small animals, such as insects and worms. They are social animals and live in groups called colonies. Toads are known for their unique mating behaviors, including the use of pheromones to attract mates. They are also known for their ability to regenerate lost limbs and regenerate their tails. Toads are important animals in their ecosystems, as they help to control pest populations and provide food for other animals."

    # # Токенизация
    # tokens = tokenizer.tokenize(text, add_special_tokens=False)

    # # Печать количества токенов
    # print("Количество токенов:", len(tokens))

