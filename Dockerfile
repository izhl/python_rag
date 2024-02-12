#   编译阶段
FROM ghcr.io/izhl/python_gcc_base:1.0
COPY . .

RUN pip install --upgrade pip
# docker不支持onnxruntime
# RUN pip3 install onnxruntime
RUN pip install --upgrade --quiet --use-deprecated=legacy-resolver redis langchain langchain-community langchainhub langchain-openai chromadb bs4
# RUN pip install redis langchain langchain-community langchainhub langchain-openai chromadb bs4
CMD ["python", "./main.py"]