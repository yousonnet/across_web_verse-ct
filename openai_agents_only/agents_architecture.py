
from utils.utils import load_json, is_termination_msg
from autogen.agentchat.contrib.gpt_assistant_agent import GPTAssistantAgent
from autogen import config_list_from_json
import pandas as pd

remakeable_config = {"seed": 42,
                     "temperature": 0, }

config_list_3dot5_turbo = config_list_from_json(env_or_file="OAI_CONFIG_LIST", filter_dict={
    "model": ["gpt-3.5-turbo-0125"]
})

twitter_api_researcher_settings = load_json(
    "openai_agents_only/twitter_api_researcher.json")
print(twitter_api_researcher_settings["tools"])
print(twitter_api_researcher_settings["file_ids"])
twitter_api_researcher = GPTAssistantAgent(name="twitter_api_researcher", instructions=twitter_api_researcher_settings['instruction'], llm_config={
                                           "config_list": config_list_3dot5_turbo, "tools": twitter_api_researcher_settings["tools"], "file_ids": twitter_api_researcher_settings["file_ids"], **remakeable_config}, overwrite_instructions=True, overwrite_tools=True, is_termination_msg=lambda x: is_termination_msg(x))
