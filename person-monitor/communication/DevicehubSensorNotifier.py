import requests


class DevicehubSensorNotifier:
    __URL = 'https://api.devicehub.net/v2/project/{0}/device/{1}/sensor/{2}/data'

    def __init__(self, api_key: str, project_id: str) -> None:
        self.__api_key = api_key
        self.__project_id = project_id

    def send(self, device_uuid: str, sensor: str, status: str):
        url = self.__URL.format(self.__project_id, device_uuid, sensor)
        post_data = '{\"value\":' + status + '}'
        requests.post(
            url,
            headers=self.__get_headers(),
            data=post_data
        )

    def __get_headers(self):
        return {
            'X-ApiKey': self.__api_key,
            'Content-Type': 'application/json'
        }