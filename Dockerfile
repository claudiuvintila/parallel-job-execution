FROM continuumio/anaconda3
RUN apt update

RUN mkdir /workspace

COPY ./requirements.txt /workspace/requirements.txt

RUN conda config --add channels conda-forge
#RUN conda update conda
RUN conda config --show channels
RUN conda create -n py39 python=3.9 pip --file /workspace/requirements.txt
#RUN /opt/conda/envs/py39/bin/pip install jupyter
RUN echo "source activate py39" > ~/.bashrc
ENV PATH /opt/conda/envs/env/bin:$PATH

COPY ./rabbitmq /workspace/rabbitmq

WORKDIR "/workspace"
CMD ["bash", "-c", "/opt/conda/envs/py39/bin/python connsumer.py"]