"""
    A price object that allows you to move between micro-services without having a 3rd micro-service to act as a intermmediary.
"""

import uuid
import rolling
import random
from scipy.stats import linregress
from redis import Redis


class PriceSeer(object):
    """ 
        Allows us to explain what the last seen price for a given crypto was. 
        Makes it easy and fast for doing later calculations inside of other parts of the application.
    """
    def __init__(self, redis_host="localhost", episode=None):
        self.redis = Redis(redis_host)
        if episode is not None:
            self.base_key = f"{episode}"
        else:
            self.base_key = ""

    def set_episode(self, episode):
        self.base_key = f"{episode}"
    
    def put_latest_price(self, coin, price):
        self.dist_key = f"{self.base_key}:{coin}:coin_price"
        self.redis.rpush(self.dist_key, price)
        

    def get_latest_price(self, coin, limit=1, rand_null=False):
        self.dist_key = f"{self.base_key}:{coin}:coin_price"
        prices = self.redis.lrange(self.dist_key, (limit * -1), -1)
        price_len = len(prices)
        
        if price_len == 0 and rand_null == True:
            return random.uniform(0, 1) * random.randint(1, 100)
        if price_len > 0:
            prices = [float(x) for x in prices]

        if price_len == 1:
            return prices[0]
        return prices
    

class RebalanceHistory(object):
    """ 
        Handles the cap rebalance history for the portfolio. It also generates rolling information to supply 
    """
    def __init__(self, redis_host="localhost", episode=None):
        self.redis = Redis(redis_host)
        if episode is not None:
            self.base_key = f"{episode}"
        else:
            self.base_key = ""

    def set_episode(self, episode):
        self.base_key = f"{episode}"
    
    def put_rebalance(self, coin, percentage):
        self.dist_key = f"{self.base_key}:{coin}:rebalance"
        self.redis.rpush(self.dist_key, percentage)
        

    def get_rebalance_history(self, coin, limit=11, rand_null=False):
        self.dist_key = f"{self.base_key}:{coin}:rebalance"
        prices = self.redis.lrange(self.dist_key, (limit * -1), -1)
        price_len = len(prices)
        history = {}
        if price_len == 0 and rand_null == True:
            history["latest"] = random.uniform(0, 1) * random.randint(1, 10000)
            history["volatility"]   = 0
            history["entropy"]      = 0
            history["var"]          = 0
            history["skew"]         = 0
            history["lin_r"]        = 0
            history["lin_p"]        = 0
            return history
        
        if price_len == 0 and rand_null == False:
            history["latest"]       = 0
            history["volatility"]   = 0
            history["entropy"]      = 0
            history["var"]          = 0
            history["skew"]         = 0
            history["lin_r"]        = 0
            history["lin_p"]        = 0
            return history

        if price_len > 0:
            prices = [float(x) for x in prices]
        
    
        if price_len > 10:
            
            volatility = list(rolling.Std(prices, 4))
            entropy = list(rolling.Entropy(prices, 4))
            var = list(rolling.Var(prices, 4))
            skews=list(rolling.Skew(prices, 4))
            general_roll = list(rolling.Apply(prices, 4, operation=list, window_type='variable'))
            slope, intercept, r_value, p_value, std_err = linregress(list(range(4)), general_roll[-4])

            # TODO: Get the regression of the latest time period
            history["latest"] = prices[-1]
            history["volatility"] = volatility[-1]
            history["entropy"] = entropy[-1]
            history["var"] = var[-1]
            history["skew"] = skews[-1]
            history["lin_r"] = r_value
            history["lin_p"] = p_value
            return history


        history["latest"] = prices[-1]
        history["volatility"]   = 0
        history["entropy"]      = 0
        history["var"]          = 0
        history["skew"]         = 0
        history["lin_r"]        = 0
        history["lin_p"]        = 0
        return history

if __name__ == "__main__":
    roll_size = 500
    y = [random.uniform(0, 1) * 10 for x in range(7000)]
    rebalance = [random.uniform(0, 1) * 10 for x in range(7000)]
    rolls = list(rolling.Apply(y, roll_size, operation=list, window_type='variable'))
    rebalance_history_roll = list(rolling.Apply(y, roll_size, operation=list, window_type='variable'))
    red_price = PriceSeer(episode=uuid.uuid4().hex)
    rebal_history = RebalanceHistory(episode=uuid.uuid4().hex)
    last_number = 0
    for roll in rolls:
        if len(roll) != roll_size:
            continue
        last_number = roll[-1]
        red_price.put_latest_price("BTC", last_number)
        redis_price = red_price.get_latest_price("BTC")
        print(redis_price)
        
    
    for rebal in rebalance_history_roll:
        if len(rebal) != roll_size:
            continue
        rebal_history.put_rebalance("ETH", rebal[-1])
        print(rebal_history.get_rebalance_history("ETH"))
