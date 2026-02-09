FROM nvidia/cuda:12.6.3-cudnn-devel-ubuntu22.04
ENV TZ=Asia/Shanghai
ENV DEBIAN_FRONTEND=noninteractive

RUN sed -i 's|http://archive.ubuntu.com/ubuntu/|https://mirrors.tuna.tsinghua.edu.cn/ubuntu/|g' /etc/apt/sources.list && \
    sed -i 's|http://security.ubuntu.com/ubuntu/|https://mirrors.tuna.tsinghua.edu.cn/ubuntu/|g' /etc/apt/sources.list

RUN mkdir -p /tmp/apt-key-gpghome && chmod 1777 /tmp

RUN apt update && apt install -y python3.10 python3.10-dev python3-pip vim curl wget git git-lfs
RUN python3.10 -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple rawpy pillow requests
RUN python3.10 -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -U vllm --pre --extra-index-url https://wheels.vllm.ai/nightly