# Nebius Assignment

# Description
Implementation of the Nebius assignment task, which serves as a preliminary qualification test
for Nebius Agenitc AI course.

# Repository Content
Root Folder

    app.py                  # FastAPI application

    requirements.txt

    src

        auxiliary

              config.py           # parameters initialized either by enviromental parameters or hard-coded

              utils.py            # Definition of some classes and functions

        llm

              base.py             # LLM inteface definition

              openai_provider.py  # Implementation of OpenAI LLM

        prompts

              consider_src.txt    # A prompt to the LLM, which consider source files

              ignore_src.txt      # A prompt that ignores source files

        services

              github_service.py   # Fetch the repository and extract its main information components

              summarizer.py       # Use the LLM for generating a summary descrition of the repo, based on the prompt and the repo's components


# LLM Choice
I chose to use **OpenAI**, as I'm most familiar with it for similar task, and it is also known to be
rather competative regarding code generation and analysis tasks.
The specific model I chose is *gpt-4o-mini*, which is known to be a good choice, from cost-performance perspective.

# Handle Repository Content
First I used the packages *httpx* and *urllib* for fetching the repository and extract its main information components.
Four components were extracted from the reposirory:

  README     - description file

  Metadata   - automatically generated details about the repository, beyond its source code

  Languages  - the software languages used in the repository

  files      - all the files which can be found in the repository, regardless of their types and roles


At first I used all these 4 components, and tried them on a few reposiries known to me.
The results seemd reasonable and adequate, but the number of files may present a problem for larger repositories.
As extensive research of this subject is, of course, beyond the scope of this task, I decided to try few
simple ways for reducing and limiting the amount of information sent to the LLM:

      (1) Exclude the *files* components, which is by far the *heavier* repo component

      (2) Define a list of source code extensions (e.g. *.py, *.cc, *.js, etc.), and exclude all files with different extensions

      (3) Induce a hard limit on the files number (e.g. no more than 500)


As the first attempt - excluding the *files* component - induced good performance (very similar to the performance with *files*),
and due to resources and time constraints I have, I decided to content with this configuration.

# Step-By-Step Setup Instructions
* Download **nebius_task.zip** and unzip it in your convenient location
* Create conda environment (e.g. conda create --name *my_env* python=3.11). Virtual environment is fine too.
* Activate the conda environment (e.g. conda activate *my_env*). Or the virtual environment, alternatively.
* pip install -r requirements.txt
* export OPENAI_API_KEY=**API CODE for OpenAI**
* uvicorn app:app --reload  # run the application
