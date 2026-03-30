from pathlib import Path
from jinja2 import Template
import json
from src.auxiliary import config, utils


def load_prompt():
    prompt = (
        config.CONSIDER_SRC_PROMPT
        if config.CONSIDER_SRC_FILES
        else config.IGNORE_SRC_PROMPT
    )
    return Path(config.PROMPTS_FOLDER + prompt).read_text()


def render_prompt(bundle: dict, template: Template) -> str:
    utils.logger.info(f"CONSIDER Source Files Flag = {config.CONSIDER_SRC_FILES}")
    if config.CONSIDER_SRC_FILES:
        utils.logger.info("PROMPT: Consider Source Files")
        return template.render(
            metadata=json.dumps(bundle["metadata"], indent=2),
            readme=bundle["readme"],
            languages=json.dumps(bundle["languages"], indent=2),
            files=json.dumps(bundle["files"], indent=2),
        )
    else:
        utils.logger.info("PROMPT: Ignore Source Files")
        return template.render(
            metadata=json.dumps(bundle["metadata"], indent=2),
            readme=bundle["readme"],
            languages=json.dumps(bundle["languages"], indent=2),
        )


async def summarize_repository(bundle, llm):
    prompt = render_prompt(bundle=bundle, template=Template(load_prompt()))
    return await llm.generate(prompt)
