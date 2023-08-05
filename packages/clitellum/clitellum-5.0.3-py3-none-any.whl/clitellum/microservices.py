from clitellum.channels.configuration import ChannelConfiguration
from clitellum.handlers import HandlerManager
from clitellum.services import ServiceFactory


def microservice(bc, micro_type, micro_id, package, bc_publisher=None):
    def decorator(f):
        MicroServiceBuilder.get_instance().set_bc(bc)
        MicroServiceBuilder.get_instance().set_micro_type(micro_type)
        MicroServiceBuilder.get_instance().set_micro_id(micro_id)
        MicroServiceBuilder.get_instance().set_package(package)
        MicroServiceBuilder.get_instance().set_bc_publisher(bc_publisher)
        return f
    return decorator


class MicroServiceBuilder:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = MicroServiceBuilder()
        return cls._instance

    def __init__(self):
        self.__bc = None
        self.__micro_type = None
        self.__micro_id = None
        self.__package = None
        self.__bc_publisher = None
        self.__amqp_uri = "amqp://guest:guest@localhost:5672/"
        self.__max_threads = 4

    def set_bc(self, bc):
        self.__bc = bc

    def set_micro_type(self, micro_type):
        self.__micro_type = micro_type

    def set_micro_id(self, micro_id):
        self.__micro_id = micro_id

    def set_package(self, package):
        self.__package = package

    def set_bc_publisher(self, bc_publisher):
        self.__bc_publisher = bc_publisher

    def set_amqp_uri(self, amqp_uri):
        self.__amqp_uri = amqp_uri

    def set_max_thread(self, max_threads):
        self.__max_threads = max_threads

    def build(self):
        # Load handlers packages
        __import__(self.__package)

        config_receiver = ChannelConfiguration()
        config_receiver.uri = self.__amqp_uri
        config_receiver.exchange.name = self.__bc
        config_receiver.queue.name = '%s.%s.%s' % (self.__bc, self.__micro_type, self.__micro_id)

        for routing_key in HandlerManager.get_instance().get_routing_keys():
            config_receiver.queue.add_routing_key(routing_key)

        config_receiver.max_threads = 4

        config_sender = ChannelConfiguration()
        config_sender.uri = self.__amqp_uri
        config_sender.exchange.name = self.__bc_publisher if self.__bc_publisher is not None else self.__bc

        service = ServiceFactory.create_service(service_id=self.__micro_id,
                                                service_type=self.__micro_type,
                                                config_sender=config_sender,
                                                config_receiver=config_receiver,
                                                handler_manager=HandlerManager.get_instance())

        return service

