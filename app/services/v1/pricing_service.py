OPENAI_PRICING = {
    "gpt-4.1-mini": {
        "input": 0.40,
        "output": 1.60,
    },
}

GEMINI_PRICING = {
    "gemini-2.5-flash": {
        "input": 0.30,
        "output": 2.50,
    },
}

DEEPSEEK_PRICING = {
    "deepseek-chat": {
        "input": 0.27,
        "output": 1.10,
    },
}

def calculate_cost(
    provider,
    model,
    prompt_tokens,
    completion_tokens,
):

    if provider == "openai":
        price = OPENAI_PRICING[model]

    elif provider == "gemini":
        price = GEMINI_PRICING[model]

    elif provider == "deepseek":
        price = DEEPSEEK_PRICING[model]

    else:
        return 0

    input_cost = prompt_tokens / 1_000_000 * price["input"]

    output_cost = completion_tokens / 1_000_000 * price["output"]

    return input_cost + output_cost