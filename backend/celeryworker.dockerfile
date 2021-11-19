FROM python:3.9

WORKDIR /app/

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./app/pyproject.toml ./app/poetry.lock* /app/

# /start Project-specific dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
		# Sqwyre
		make \
		build-essential \
		curl \
		autoconf \
		automake \
		libtool \
		pkg-config \
		# Qwyre
		pandoc \
		default-jre \
 && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*	

# Install pyenv and set Python 3.9 as poetry env
# set the variables as per $(pyenv init -)
ENV LANG="C.UTF-8" \
    LC_ALL="C.UTF-8" \
    PATH="/opt/pyenv/shims:/opt/pyenv/bin:$PATH" \
    PYENV_ROOT="/opt/pyenv" \
    PYENV_SHELL="bash"
	
RUN git clone --depth 1 https://github.com/pyenv/pyenv.git $PYENV_ROOT \
    && pyenv install 3.9.4 \
	&& pyenv local 3.9.4

WORKDIR /tmp/

RUN git clone --depth 1 https://github.com/openvenues/libpostal && \
	cd libpostal && \
	#make distclean && \
	./bootstrap.sh && \
	./configure --datadir=/tmp && \
	make -j4 && \
	make install && \
	ldconfig && \
	apt-get purge --auto-remove -qy \
	make \
	build-essential \
	curl \
	autoconf \
	automake \
	libtool \
	pkg-config

WORKDIR /app/
# /end Project-specific dependencies


# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"

# For development, Jupyter remote kernel, Hydrogen
# Using inside the container:
# jupyter lab --ip=0.0.0.0 --allow-root --NotebookApp.custom_display_url=http://127.0.0.1:8888
ARG INSTALL_JUPYTER=false
RUN bash -c "if [ $INSTALL_JUPYTER == 'true' ] ; then pip install jupyterlab ; fi"

ENV C_FORCE_ROOT=1

COPY ./app /app
WORKDIR /app

ENV PYTHONPATH=/app

COPY ./app/worker-start.sh /worker-start.sh

RUN chmod +x /worker-start.sh

CMD ["bash", "/worker-start.sh"]
