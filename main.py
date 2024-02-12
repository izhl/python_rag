#!/usr/bin/python
# -*- coding: utf-8 -*-
import asyncio
from rdb import get_redis_list_rpop,get_redis_list_llen
from dotenv import load_dotenv
import getpass
import os
import bs4
from langchain import hub
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from wsgiref.simple_server import make_server
# from httpd import RunServer
import json
import urllib

rag_chain = None

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# 1、获取redis中的数据
# 2、加载文件
# 3、拆分文件数据
# 4、转换数据为embedding，并存储到
def do_rag():
    # 使用dotenv，参考https://blog.csdn.net/wohu1104/article/details/128281466
    load_dotenv()
    print('OPENAI_API_KEY',os.environ["OPENAI_API_KEY"])
    if os.environ["OPENAI_API_KEY"] == '':
        os.environ["OPENAI_API_KEY"] = getpass.getpass()
    bs4_strainer = bs4.SoupStrainer(class_=("post-title", "post-header", "post-content"))

    len = get_redis_list_llen('rag:urls')
    if len == 0:
        print('no data')
        return None
    else:
        urls = []
        for l in range(len):
            url = get_redis_list_rpop('rag:urls')
            # set_redis_list_lpush('rag:urls',url) # 将取出的数据放回去，开发使用
            urls.append(url)
        print('urls:',urls)
        loader = WebBaseLoader(
            web_paths=urls,
            bs_kwargs={"parse_only": bs4_strainer},
        )
        docs = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200, add_start_index=True
        )
        all_splits = text_splitter.split_documents(docs)
        # print('all_splits_len',len(all_splits))
        vectorstore = Chroma.from_documents(documents=all_splits, embedding=OpenAIEmbeddings())

        retriever = vectorstore.as_retriever()
        prompt = hub.pull("rlm/rag-prompt")
        llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

        rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )
        return rag_chain

#输出回复时，通过string.encode()指定输出的文字编码方式，string.encode('gb2312')、string.encode('utf-8')、string.encode('gbk')
errStr ='''
{ 
	"code" : -1, 
	"msg" : "not support"
}
'''

def RunServer(environ, start_response):

    #添加回复内容的HTTP头部信息，支持多个
    headers = {'Content-Type': 'application/json', 'Custom-head1': 'Custom-info1'}

    # environ 包含当前环境信息与请求信息，为字符串类型的键值对
    current_url = environ['PATH_INFO']
    print(current_url)
    # current_content_type = environ['CONTENT_TYPE']
    # current_content_length = environ['CONTENT_LENGTH']
    # current_request_method = environ['REQUEST_METHOD']
    # current_remote_address = environ['REMOTE_ADDR']
    # current_encode_type = environ['PYTHONIOENCODING']        #获取当前文字编码格式，默认为UTF-8

    #获取 body JSON内容转换为python对象
    current_req_body = environ['wsgi.input'].read(int(environ['CONTENT_LENGTH']))
    current_req_json = json.loads(current_req_body)

    #打印请求信息
    #print("environ:", environ)
    # print("REQUEST remote ip:", current_remote_address)
    # print("REQUEST method:", current_request_method)
    # print("REQUEST URL:", current_url)
    # print("REQUEST Content-Type:", current_content_type)
    # print("REQUEST body:", current_req_json)

    user_content = current_req_json['user_content']
    user_content = urllib.parse.unquote(user_content)

    #根据不同URL回复不同内容
    # if current_url == "/rag":
    # 处理content
    result = rag_chain.invoke(user_content)
    # print(content)
    # content = urllib.parse.quote(content_re)
    # 拼装回复报文
    successStr = '''
        {
            "code":1,"msg":"success",
            "data":{
                "content":"%s"
            }
        }
        ''' % (result)
    start_response("200 OK", list(headers.items()))
    return [successStr.encode("utf-8"), ]

if __name__ == '__main__':
    rag_chain = do_rag()
    # if rag_chain:
    #     print(rag_chain.invoke("What is Task Decomposition?"))

    #10000为HTTP服务监听端口，自行修改
    httpd = make_server('', 3678, RunServer)
    host, port = httpd.socket.getsockname()
    print('Serving running', host, 'port', port)
    httpd.serve_forever()