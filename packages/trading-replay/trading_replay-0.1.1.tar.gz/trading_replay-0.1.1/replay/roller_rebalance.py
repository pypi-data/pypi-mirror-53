import os
import pickle
import random
import uuid

from crayons import blue
from redis import Redis
import rolling


# rhost = os.environ.get("REDISHOST", "localhost")



class RebalanceController(object):
    def __init__(self, redis_host, **kwargs):
        self.redis = Redis(redis_host)
    
    def add_rebalance_coins(self, coin, user_id, prices, episode=None):
        user_coins_key = f"{user_id}:coins"
        placeholder_key = f"{user_id}:{coin}:placeholder_prices"

        if episode is not None:
            placeholder_key = f"{episode}:" + placeholder_key

        self.redis.sadd(user_coins_key, coin)
        self.redis.set(placeholder_key, pickle.dumps(prices))

    

    def get_rebalance_coins(self, user_id, episode=None):
        user_coins = f"{user_id}:coins"
        coins = self.redis.smembers(user_coins)
        coins = [x.decode("utf-8") for x in coins]
        coin_dict = {}
        for coin in coins:
            user_placeholder_key = f"{user_id}:{coin}:placeholder_prices"
            if episode is not None:
                user_placeholder_key = f"{episode}:" + user_placeholder_key
            coin_shit = self.redis.get(user_placeholder_key, None)
            if coin_shit is not None:
                coin_dict[coin] = pickle.loads(coin_shit)
        return coin_dict