JUDGE_SYSTEM_PROMPT = """
You are an AI agent who provides a judging service.
Your task is to rate a given text, which was generated
by another AI agent.
The generated text is a description of an e-commerce product, which
is based on a set of attributes characterizing the product.
The product to be described will be presented by a s JSON-formatted string,
consisting on two keys: attribute and generated_description.
Here is an example of the product input:

*** Example:***
"{
'attributes':
    {
        'Name':'Apple iPhone 15 Pro',
        'material':'titanium...',
        'warranty':'1-year limited warranty',
        'features':'A17 Pro chip...',
        'battery':'long-lasting',
    }
'generated_description': 'The Apple iPhone 15 Pro is a sleek and powerful device featuring...'
}"

Notice that the first 4 attributes - Name, material, warranty, and features - appear,
for each product, while the other attributes appear alternately across the products.

Your task, therefore, is to rate the generated_description based on the product's attributes.
You should assign to the generated description four scores, according to the next
scoring rubric and accoring to the provided response_format structure.

***Generated Description Scoring rubric:***
* Fluency:
    * Good: if the generated description is coherent, sounds natural, clear, and easy to read.
    * OK: if the generated description is still as above, but slighly less fluent and clear.
    * Bad: if there are gliches of uncoherent text, or awkward language.
* Grammar:
    * Good: if the generated description is grammatically correct, with punctuations, and uppercase where needed.
    * OK: if the generated description is still basically correct, but with minor glich or two (e.g. none perfect punctuation).
    * Bad: if there are more than two grammaticall gliches in the generated description.
* Tone:
    * Good: if the generated description matches friendly, credible sales voice, persuasive, and include poilte words and subtle enthusiasm.
    * OK: if the generated description is still nice and decent, but lacking some of the aspects mentioned in 'Good' above.
    * Bad: if the generated description lacks too many positive aspects, described above, or contains some less friendly expressions.
* Grounding:
    * Good: if there are no hallucinations, and the generated description can be directly inferred from the product name or features.
    * OK: if the above conditions are satisfied, but with possible minor 'creativity' (e.g. use synonyms, 'metal' instead of 'aluminum').
    * Bad: if the generated description contains hallucinations, or it can be hardly inferred from the content.

***Output Format:***
Please retrive a response according to the provided response_format structure.
Please provide for each criterion an explanation, which explains your verdict choice.
"""

JUDGE_USER_PROMPT = """
Please score the given product's generated description based on its attributes,
as explained above, and output your decision according to the provided structure.
The attributes are provided below as JSON-Formatted string between triple backticks:

```json
"""

{
    "name": "generated_description_judgement",
    "schema": {
        "type": "object",
        "properties": {
            "fluency": {
                "type": "object",
                "description": "rate the fluency level of the generated text",
                "properties": {
                    "justification": {
                        "type": "string",
                        "description": "explain why you chose this fluency rate for the text",
                        "minLength": 75,
                    },
                    "verdict": {
                        "type": "string",
                        "description": "the fluency rate of the text: Good / OK / Bad",
                    },
                },
                "required": ["justification", "verdict"],
                "additionalProperties": False,
            },
            "grammar": {
                "type": "object",
                "description": "rate the level of the grammar accuracy of the generated text",
                "properties": {
                    "justification": {
                        "type": "string",
                        "description": "explain why you chose this grammar accuracy rate for the text",
                        "minLength": 75,
                    },
                    "verdict": {
                        "type": "string",
                        "description": "the grammar accuracy rate of the text: Good / OK / Bad",
                    },
                },
                "required": ["justification", "verdict"],
                "additionalProperties": False,
            },
            "tone": {
                "type": "object",
                "description": "rate the tone quality of the generated text",
                "properties": {
                    "justification": {
                        "type": "string",
                        "description": "explain why you chose this rate for the tone quality of the text",
                        "minLength": 75,
                    },
                    "verdict": {
                        "type": "string",
                        "description": "the rate of the tone quality of the text: Good / OK / Bad",
                    },
                },
                "required": ["justification", "verdict"],
                "additionalProperties": False,
            },
            "grounding": {
                "type": "object",
                "description": "rate the faithfulness of the generated text",
                "properties": {
                    "justification": {
                        "type": "string",
                        "description": "explain why you chose this rate for the faithfulness of the text",
                        "minLength": 75,
                    },
                    "verdict": {
                        "type": "string",
                        "description": "the rate of the faithfulness of the text: Good / OK / Bad",
                    },
                },
                "required": ["justification", "verdict"],
                "additionalProperties": False,
            },
        },
        "required": ["fluency", "grammar", "tone", "grounding"],
        "additionalProperties": False,
    },
    "strict": True,
}
