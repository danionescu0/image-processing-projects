import {Client} from "react-native-paho-mqtt";
import {MQTT_ENDPOINT, MQTT_PASSWORD, MQTT_USER} from "../../config"


export const websocketClientConnect = (topic) => {
    const myStorage = {
        setItem: (key, item) => {
            myStorage[key] = item;
        },
        getItem: (key) => myStorage[key],
        removeItem: (key) => {
            delete myStorage[key];
        },
    };
    const client = new Client({ uri: MQTT_ENDPOINT, clientId: '', storage: myStorage });

    return new Promise((resolve, reject) => {
        return client.connect({userName: MQTT_USER, password: MQTT_PASSWORD})
            .then(() => {
                client.subscribe(topic);
                return resolve(client);
            })
            .catch(e => reject(e));
    });

};

export const websocketCallbacks = (client, messageReceivedCallback) => {
    client.on('connectionLost', (responseObject) => {
        if (responseObject.errorCode !== 0) {
            console.log(responseObject.errorMessage);
        }
    });
    client.on('messageReceived', (message) => {
        messageReceivedCallback(message);
    });
};