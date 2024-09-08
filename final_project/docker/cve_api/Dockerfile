FROM python:3.12.2-bullseye

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH "${PYTHONPATH}:/"
ENV HOME=/cve_api

ARG USERNAME=default
ARG GROUPNAME=$USERNAME
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd -g ${USER_GID} ${GROUPNAME} \
    && useradd -m -d ${HOME} -s /bin/bash -g ${GROUPNAME} -u ${USER_UID} ${USERNAME} \
    && mkdir -p /etc/sudoers.d \
    && echo "${USERNAME} ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/${USERNAME} \
    && chmod 0440 /etc/sudoers.d/${USERNAME}

RUN apt-get update \
    && pip install --upgrade pip

WORKDIR ${HOME}
COPY ./requirements.txt ${HOME}/requirements.txt
RUN pip install -r requirements.txt
COPY ./cve_api ${HOME}

USER ${USERNAME}
