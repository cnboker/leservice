FROM python:3.10.15

WORKDIR /app
COPY server.py /app
COPY segmentParser.py /app
COPY requirements.txt /app

# 创建并激活虚拟环境

RUN python -m venv venv

# 安装依赖
RUN . venv/bin/activate && RUN pip install --upgrade pip setuptools && pip install --no-cache-dir -r requirements.txt

#run app
CMD ["venv/bin/python", "main.py"]

