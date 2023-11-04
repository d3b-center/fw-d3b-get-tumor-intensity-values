FROM python:3.9.7-slim-buster

ENV FLYWHEEL="/flywheel/v0"
WORKDIR ${FLYWHEEL}

RUN apt-get update \
&& apt-get install gcc -y \
&& apt-get clean

COPY run.py manifest.json README.md requirements.txt $FLYWHEEL/
COPY fw_gear_functions ${FLYWHEEL}/fw_gear_functions 

# Install main deps
RUN pip3 install -r requirements.txt
# RUN pip install poetry
# COPY pyproject.toml poetry.lock $FLYWHEEL/
# RUN poetry install --no-dev --no-root

# Installing the current project (most likely to change, above install is cached)
# RUN poetry install --no-dev

# Configure entrypoint
RUN chmod a+x $FLYWHEEL/run.py
ENTRYPOINT ["python","/flywheel/v0/run.py"]
