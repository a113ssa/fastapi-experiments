import torch
from transformers import Pipeline, pipeline
import os
from dotenv import load_dotenv

load_dotenv()

prompt = "How to create Text Quest game?"
system_prompt = """
Your name is Text Quest bot and you are a helpful chatbot
 responsible for teaching Text Quest game creation to your users.
 Always respond in markdown.
"""


def load_text_model():
    pipe = pipeline(
        "text-generation",
        model=os.getenv("TEXT_MODEL", "TinyLlama/TinyLlama-1.1B-Chat-v1.0"),
        torch_dtype=torch.bfloat16,
        device=0 if torch.cuda.is_available() else -1,
    )
    return pipe


def generate_text(pipe: Pipeline, prompt: str, temperature: float = 0.7) -> str:
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt},
    ]

    prompt = pipe.tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )

    predictions = pipe(
        prompt,
        temperature=temperature,
        max_new_tokens=256,
        do_sample=True,
        top_k=50,
        top_p=0.95,
    )

    output = predictions[0]["generated_text"].split("</s>\n<|assistant|>\n")[1]
    return output
