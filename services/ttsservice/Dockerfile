# Use a lightweight base image
FROM ubuntu:22.04
# 设置非交互模式，防止构建过程中交互式提示
ENV DEBIAN_FRONTEND=noninteractive
# Install dependencies
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    gcc \
    libssl-dev \
    python3.9 \
    python3.10-venv \
    python3-pip && \
    rm -rf /var/lib/apt/lists/*

# 设置 CARGO_HOME 并安装 Rust
ENV CARGO_HOME=/root/.cargo
# Install Rust using rustup
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

# 显式添加 Rust 到 PATH
ENV PATH="$CARGO_HOME/bin:$PATH"

# 验证 Rust 是否成功安装
RUN rustc --version

WORKDIR /app
COPY . /app

# 创建虚拟环境
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
# 将虚拟环境添加到 PATH
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install --upgrade pip setuptools wheel && pip install --upgrade cython && pip install spacy --no-build-isolation

# 安装依赖
RUN  pip install --upgrade pip && pip install  -r requirements.txt

#run app
CMD ["python", "server.py"]
