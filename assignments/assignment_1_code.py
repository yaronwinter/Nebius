import pandas as pd
import os
import json
from openai import OpenAI
import unicodedata

SYSTEM_PROMPT = """
You are an AI agent.
Your task is to describe products based on their given attributes.
The product to be described will be presented by a s JSON-formatted string, in
which the keys are the attributes names and the values are their description.

***For Example:***
"{
'Name':'Apple iPhone 15 Pro',
'material':'titanium...',
'warranty':'1‑year limited warranty',
'features':'A17 Pro chip...',
'battery':'long‐lasting',
}"

Notice that the first 4 attributes - Name, material, warranty, and features - appear,
for each product, while the other attributes appear alternately across the products.

Please generate for such product a description, which will satisfies the next criterions:

***Description Criterion:***
* Sounds natural and fluent, clear and easy to read.
* Should be grammatically correct, with puctuations and uppercase where needed.
* The 'tone' of the text should be friendly, sounds like a credible sales voice, nice and poilte.
* The length of the generated text, i words number, should be in the range 50-90 words.
* It is VERY IMPORTANT that the generated description can be inferred from the product attributes only, with no hallucinations!

***Output Format:***
Please retrive just the generated description.
"""

USER_PROMPT = """
Please describe the given product based on its attributes.
The attributes are provided below as JSON-Formatted string between triple backticks:

```json
"""

client = OpenAI(
    base_url="https://api.tokenfactory.nebius.com/v1/",
    api_key=os.environ.get("NEBIUS_API_KEY"),
)


def describe_product(attributes: dict):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": [
                {"type": "text", "text": f"{USER_PROMPT} {json.dumps(attributes)}"}
            ],
        },
    ]

    response = client.chat.completions.create(
        model="google/gemma-2-9b-it-fast", messages=messages
    )

    print(f"messages: {messages}")
    return response.to_dict()


def break_attributes(attributes: str) -> dict:
    try:
        items = attributes.split(";")
        items = [item.split(":") for item in items]
        items = [item if len(item) > 1 else ("other", item[0]) for item in items]
        return {item[0].strip(): item[1].strip() for item in items}
    except Exception as e:
        raise Exception(f"Failed to process item {attributes}, e={e}")


def normalize_text(s):
    if isinstance(s, str):
        s = unicodedata.normalize("NFKC", s)
        return s.replace("\u202f", " ").replace("\u2010", " ").replace("\xa0", " ")
    return s


def preprocess_table(df: pd.DataFrame) -> pd.DataFrame:
    df["Name"] = df.index
    df.index = [i for i in range(len(df))]
    df = df.rename(columns={"Product_attribute_list": "attributes"})
    df = df[["Name", "attributes", "material", "warranty"]].copy()
    for field in ["Name", "attributes", "material", "warranty"]:
        df[field] = df[field].apply(lambda x: normalize_text(x))
    return df


def get_attributes_dict(r: pd.Series) -> dict:
    d = dict(r)
    d = {**d, **break_attributes(d["attributes"])}
    d.pop("attributes")
    return d
