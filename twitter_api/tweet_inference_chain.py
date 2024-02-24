from typing import Union,List,Literal

from numpy import full
from utils.iface import TweetWithoutMediaIFace,ReplyIFace

TweetTypes=Union[Literal['repost'],Literal['quote'],Literal['tweet'],Literal['reply']]

def is_repost(full_text:str)->bool:
    if full_text.startswith("RT @"):
        return True
    else:
        return False
def tweet_inference(array:List[Union[TweetWithoutMediaIFace,ReplyIFace]]):
    