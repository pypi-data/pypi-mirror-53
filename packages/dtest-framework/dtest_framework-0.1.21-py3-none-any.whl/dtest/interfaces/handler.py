from abc import ABCMeta, abstractmethod


class MqHandler:

    @classmethod
    def version(self): return "1.0"

    @abstractmethod
    def connect(self): raise NotImplementedError

    @abstractmethod
    def publish_results(self): raise NotImplementedError

    @abstractmethod
    def close_connection(self): raise NotImplementedError


class KvHandler:

    @classmethod
    def version(self): return "1.0"

    @abstractmethod
    def retrieve(self): raise NotImplementedError

    @abstractmethod
    def publish(self): raise NotImplementedError
