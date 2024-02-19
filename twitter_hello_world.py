from autogen import AssistantAgent, UserProxyAgent, ConversableAgent, GroupChat, GroupChatManager, config_list_from_json
from autogen.agentchat.contrib.gpt_assistant_agent import GPTAssistantAgent
from twitter_api.constants import openai_api_key
from twitter_api.clients_setup import clients
from typing import List
from time import sleep
import schedule
import random

config_list = config_list_from_json("OAI_CONFIG_LIST", filter_dict={
    "model": "gpt-3.5-turbo-0125"
})


def is_termination_msg(x):
    # print(x)  # 打印 x 的值
    if (x.get("content", "").rstrip().endswith("TERMINATE")):
        print("yes")
        return True
    print(x)
    print("no")
    return True


assistant = GPTAssistantAgent(name="Assistant",    llm_config={
    "seed": 42,  # seed for caching and reproducibility
    "config_list": config_list,  # a list of OpenAI API configurations
    "assistant_id": "asst_vBwL4gYtTx830aYsFeuVvtwk",
    "temperature": 0,  # temperature for sampling
    # "request_timeout": 120,  # timeout

}, is_termination_msg=lambda x: True
    # GPT的is_termination_msg是invalid的不知道为什么

)


def generate_random_times(duration, num):
    random_times = []
    for _ in range(num):
        random_time = duration * random.uniform(0.1, 0.9)
        random_times.append(random_time)
    return random_times


def multi_accounts_tweet(tweets: List[str]):
    counter = 0
    times_sleep = generate_random_times(60, 9)
    for (client, tweet, time) in zip(clients, tweets, times_sleep):
        client['account'].tweet(tweet)
        counter += 1

        if counter == 9:
            break
        sleep(time)
    # sleep(10000)
    return True


assistant.register_function(
    function_map={"multi_accounts_tweet": multi_accounts_tweet})
user_proxy = UserProxyAgent(name="proxy_agent", default_auto_reply="TERMINATE",
                            human_input_mode="NEVER",
                            is_termination_msg=is_termination_msg,
                            code_execution_config=False)

while (True):
    user_proxy.initiate_chat(
        assistant, message="""please generate tweets,and press them by multi_accounts_tweet in one time""")
