
from json import load

from click import group
from utils.utils import load_json, is_termination_msg
from autogen.agentchat.contrib.gpt_assistant_agent import GPTAssistantAgent
from autogen.agentchat.contrib.web_surfer import WebSurferAgent
from autogen import UserProxyAgent, GroupChat, GroupChatManager
from autogen import config_list_from_json
import pandas as pd

remakeable_config = {"seed": 42,
                     "temperature": 0, }

config_list_3dot5_turbo = config_list_from_json(env_or_file="OAI_CONFIG_LIST", filter_dict={
    "model": ["gpt-4-turbo-preview"]
})


# twitter_api_researcher_settings = load_json(
#     "openai_agents_only/twitter_api_researcher.json")
# print(twitter_api_researcher_settings["tools"])
# print(twitter_api_researcher_settings["file_ids"])
# twitter_api_researcher = GPTAssistantAgent(name="twitter_api_researcher", instructions=twitter_api_researcher_settings['instruction'], llm_config={
#                                            "config_list": config_list_3dot5_turbo, "tools": twitter_api_researcher_settings["tools"], "file_ids": twitter_api_researcher_settings["file_ids"], **remakeable_config}, overwrite_instructions=True, overwrite_tools=True, is_termination_msg=lambda x: is_termination_msg(x))

# crypto_trends_researcher_settings = load_json("openai_agents_only")

web_surfer_researcher = WebSurferAgent(name="web_surfer_researcher", llm_config={
    "config_list": config_list_3dot5_turbo, **remakeable_config
},  is_termination_msg=lambda x: is_termination_msg(x))

# test_proxy = UserProxyAgent(name="test_proxy")

crypto_projects_researcher_settings = load_json(
    "openai_agents_only/crypto_projects_researcher.json")
crypto_projects_researcher = GPTAssistantAgent(name="crypto_projects_researcher", instructions=crypto_projects_researcher_settings["instruction"], llm_config={
    "config_list": config_list_3dot5_turbo, **remakeable_config}, overwrite_instructions=True, is_termination_msg=lambda x: is_termination_msg(x))


user_proxy = UserProxyAgent(name="proxy_agent",
                            is_termination_msg=lambda x: is_termination_msg(x),
                            code_execution_config=False)

web_searcher_group = GroupChat(agents=[
    web_surfer_researcher, crypto_projects_researcher], messages=[], max_round=20)
manager = GroupChatManager(groupchat=web_searcher_group, name="manager", system_message="you are a tough group manager,you only accept perfect research report ,when you receive that reply only TERMINATE to end chat,and you give the best advices to searchers", llm_config={
                           "config_list": config_list_3dot5_turbo, **remakeable_config})
user_proxy.initiate_chat(
    manager, message="collect the concept and design mechanism of this project,link:https://www.berachain.com/,if there are any new related links,please also collect the information from them,thanks!")
