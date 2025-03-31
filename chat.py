from ctransformers import AutoModelForCausalLM

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
# response = model.generate("Привет! Как ты?")
# print(response)