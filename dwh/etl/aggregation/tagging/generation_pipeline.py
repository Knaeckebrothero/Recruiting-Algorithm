"""
This script is 
"""
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch


def formate_messages(experience_dict: dict) -> list:
    """
    This function takes a experience dict and formats it as a list of messages that can be used for generation.

    :param experience: The experience dict to format.
    :return: A list of messages ready for generation.
    """
    return [
        {"role": "system", "content": ""},
        {"role": "user", "content": ""}
    ]


def generate_tags(prompt_messages: list) -> str:
    """
    This function generates a response for the given messages.

    :param messages: A list of messages to generate a response for.
    """

    # Apply the chat template and send tokens to the gpu
    input_ids = tokenizer.apply_chat_template(
        prompt_messages,
        add_generation_prompt=True,
        return_tensors="pt"
    ).to(model.device)

    # Generate a response
    outputs = model.generate(
        input_ids,
        max_new_tokens=256,
        eos_token_id=terminators,
        do_sample=True,
        temperature=0.6,
        top_p=0.9
    )

    response = outputs[0][input_ids.shape[-1]:]
    print(tokenizer.decode(response, skip_special_tokens=True))

    # Return the response
    return tokenizer.decode(response, skip_special_tokens=True)


# Define the model ID
model_id = "meta-llama/Meta-Llama-3-8B-Instruct"

# Load model andd tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    device_map="auto",
)

# Define the terminators
terminators = [
    tokenizer.eos_token_id,
    tokenizer.convert_tokens_to_ids("<|eot_id|>")
]

