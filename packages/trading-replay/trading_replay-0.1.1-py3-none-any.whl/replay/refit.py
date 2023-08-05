import pickle
from sklearn.preprocessing import StandardScaler
from redis import Redis


class DynamicScalar(object):
    """ Code here is used to dynamically refit"""
    def __init__(self, redis_host="localhost", entity="BTC", scl_type="stanard", episode=None, scaler=StandardScaler):
        self.redis = Redis(redis_host)
        self.scaler = scaler()

        if episode is not None:
            self.scaler_key = f"{entity}:{episode}:{scl_type}:scaler"
        else:
            self.scaler_key = f"{entity}:{scl_type}:scaler"
    
    def pfit_transform(self, X):
        """ Fit transform """
        self.get_scaler()
        self.scaler.partial_fit(X)
        self.save_scaler()
        return self.scaler.transform(X)

    def get_scaler(self):
        _scaler = self.redis.get(self.scaler_key)
        if _scaler is not None:
            self.scaler = pickle.loads(_scaler)
    
    def save_scaler(self):
        self.redis.set(self.scaler_key, pickle.dumps(self.scaler))