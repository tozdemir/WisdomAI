FROM amazonlinux:2

# Install python3.7
RUN yum install -y python37 && \
    yum install -y python3-pip && \
    yum install -y zip && \
    yum clean all

# Set up PIP and Venv
RUN python3.7 -m pip install --upgrade pip && \
    python3.7 -m pip install virtualenv
RUN python3.7 -m venv base
RUN source base/bin/activate

# Install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt -t ./python

# RUN rm -rf /python/{bin,include,lib64,pyvenv.cfg} /python/{__pycache__,easy_install.py,numpy*,pip*,pkg_resources,setuptools*}

# Zip it up for deployment
RUN zip -r layer.zip ./python/
ENTRYPOINT [ "/bin/bash","-l" ]