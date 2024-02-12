# python_rag
 基于langchain+openai+chromadb构建
 
 需要redis list提供文本数据URL
 
 运行：python mian.py，需要openai_api_key
 
 提供http服务post访问，端口为3678，数据格式为：
{
    "user_content": "LangChain是什么？"
}

返回结果：
{
    "code":1,"msg":"success",
    "data":{
        "content":"LangChain是一个在LLM中实现的工作流程，用于结合CoT推理和与任务相关的工具来完成任务。它通过提供工具名称列表、工具效用描述和预期输入/输出的详细信息，指导LLM在需要时使用提供的工具来回答用户给定的提示。LangChain在ChemCrow案例研究中被使用，用于有机合成、药物发现和材料设计等任务。"
    }
}
