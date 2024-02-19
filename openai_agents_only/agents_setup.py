from autogen import AssistantAgent, UserProxyAgent, ConversableAgent, GroupChat, GroupChatManager, config_list_from_json, config_list_openai_aoai


config_list_3dot5_turbo = config_list_from_json(env_or_file="OAI_CONFIG_LIST", filter_dict={
    "model": ["gpt-3.5-turbo-0125"]
})

assistant = AssistantAgent(name="Assistant",     llm_config={
    # "seed": 42,  # seed for caching and reproducibility
    "config_list": config_list_3dot5_turbo,  # a list of OpenAI API configurations
    # "temperature": 0,  # temperature for sampling
    # "request_timeout": 120,  # timeout
},
    system_message="you are a crypto project analysist,you will analyze the project based on the project's tweets and bio,and rate them from 1 to 10,then return me the rate and reason,etc summary of the project by json format",

)

user_proxy_agent = UserProxyAgent(name="proxy_agent", llm_config={
    # "seed": 42,  # seed for caching and reproducibility
    "config_list": config_list_3dot5_turbo,  # a list of OpenAI API configurations
    # "temperature": 0,  # temperature for sampling
    # "request_timeout": 120,  # timeout

}, code_execution_config=False)


groupchat = GroupChat(agents=[assistant, user_proxy_agent], messages=[])
manager = GroupChatManager(groupchat=groupchat, name="manager", llm_config={
    # "seed": 42,  # seed for caching and reproducibility
    "config_list": config_list_3dot5_turbo,  # a list of OpenAI API configurations
    # "temperature": 0,  # temperature for sampling
    # "request_timeout": 120,  # timeout
    # "model": "gpt-3.5-turbo"  # model to use
})
user_proxy_agent.initiate_chat(manager, message="analyze uniswap",)
# manager.initiate_chat(user_proxy_agent, message="analyze uniswap",)
