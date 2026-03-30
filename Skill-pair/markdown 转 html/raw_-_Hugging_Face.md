---
license: apache-2.0
datasets:
- agentica-org/DeepScaleR-Preview-Dataset
base_model:
- Qwen/Qwen3-4B
language:
- en
pipeline_tag: text-generation
library_name: transformers
tags:
- moe
- text-generation-inference
- code
- deepscale
- math
---
 
![Add a heading.png](https://cdn-uploads.huggingface.co/production/uploads/65bb837dbfb878f46c77de4c/3BhMy5T93m__r9gKpk6jY.png)

# Segue-Qwen3\_DeepScaleR-Preview

> Segue-Qwen3\_DeepScaleR-Preview is an experimental fine-tuned variant of the Qwen3-4B model architecture. It is trained on the DeepScaleR-Preview dataset—comprising high-quality mathematical reasoning problems—to achieve exceptional performance in symbolic, mathematical, and logical tasks with lightweight computational requirements.

## Key Features

1. Precision Reasoning with DeepScaleR-Preview Dataset
   Fine-tuned on approximately 40,000 curated math problem-answer pairs sourced from:

   * AIME (1984–2023)
   * AMC (pre-2023)
   * Omni-MATH
     This enables superior symbolic manipulation and step-by-step logical deduction.

2. Lightweight Code Understanding
   Capable of interpreting and generating correct code in Python, C++, and other logic-intensive languages with an emphasis on problem-solving and structured thought.

3. Structured Output Formatting
   Outputs are designed to be well-formatted in Markdown, JSON, LaTeX, or tables—ideal for technical documentation, math notebooks, and data workflows.

4. Instruction-Following Accuracy
   Strong multi-step instruction adherence, particularly for STEM domains. Ensures continuity, factual correctness, and process transparency in reasoning chains.

5. Multilingual Capabilities
   Supports over 20 languages for mathematical and logical reasoning, technical instruction translation, and cross-lingual academic support.

6. Efficient 4B Architecture
   Built on the Qwen3-4B base model to balance performance and scalability. Runs efficiently on mid-range GPUs while delivering high-accuracy inference.

## Quickstart with Transformers

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "prithivMLmods/Segue-Qwen3_DeepScaleR-Preview"

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained(model_name)

prompt = "Solve for x: 5(x - 2) = 3x + 4, showing all steps clearly."

messages = [
    {"role": "system", "content": "You are a precise mathematical assistant trained on DeepScaleR-Preview dataset."},
    {"role": "user", "content": prompt}
]

text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True
)

model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

generated_ids = model.generate(
    **model_inputs,
    max_new_tokens=512
)
generated_ids = [
    output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
]

response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
print(response)
```

## Intended Use

* Step-by-step mathematical problem solving
* Symbolic computation and logic derivation
* Code generation and correction in technical environments
* Automated LaTeX/Markdown/JSON generation for education and documentation
* Academic tutoring and educational assistants
* Multilingual reasoning and translation of structured content

## Limitations

* Less suitable for open-domain conversation or creative writing
* Smaller context window compared to large-scale LLMs
* May be sensitive to token formatting in edge-case symbolic prompts
* Could underperform on intentionally adversarial logic inputs

## References

1. Qwen2.5 Technical Report – [https://arxiv.org/pdf/2412.15115](https://arxiv.org/pdf/2412.15115)
2. YaRN: Context Window Extension for LLMs – [https://arxiv.org/pdf/2309.00071](https://arxiv.org/pdf/2309.00071)