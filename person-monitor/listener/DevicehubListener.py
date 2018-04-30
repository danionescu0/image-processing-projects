from pydispatch import dispatcher

from listener.BaseListener import BaseListener
from event.FaceFound import FaceFound
from lock.ConfiguredTimedLock import ConfiguredTimedLock
from communication.DevicehubSensorNotifier import DevicehubSensorNotifier


class DevicehubListener(BaseListener):
    def __init__(self, devicehub_timed_lock: ConfiguredTimedLock,
                 devicehub_sensor_notifier: DevicehubSensorNotifier, device_uuid: str,
                 user_id_to_sensor_mapping: dict) -> None:
        self.__devicehub_timed_lock = devicehub_timed_lock
        self.__devicehub_sensor_notifier = devicehub_sensor_notifier
        self.__device_uuid = device_uuid
        self.__user_id_to_sensor_mapping = user_id_to_sensor_mapping

    def listen(self, event: FaceFound):
        if self.__devicehub_timed_lock.has_lock():
            return
        if event.user_id not in self.__user_id_to_sensor_mapping:
            return
        self.__devicehub_sensor_notifier.send(self.__device_uuid, self.__user_id_to_sensor_mapping[event.user_id], '1')
        self.__devicehub_timed_lock.set_lock()

    def connect(self):
        dispatcher.connect(self.listen, signal="face_found", sender=dispatcher.Any)