FROM python:3.10.15


# 创建虚拟环境
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV

# 将虚拟环境添加到 PATH
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /app
COPY . /app

# 安装依赖
RUN  pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

#run app
CMD ["python", "main.py"]

