import React from 'react';
import { Image } from 'react-native';
import { StyleSheet, Text, View, TouchableHighlight } from 'react-native';
import { websocketCallbacks, websocketClientConnect } from './src/utils/websockets'
import { MINIMUM_TIME_BETWEEN_NOTIFICATION } from "./config"


export default class App extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            foundImage: null,
            lastNotification : 0,
        }
    }

    componentDidMount() {
        this.connectToWebsocket();
    }

    connectToWebsocket() {
        websocketClientConnect('faces')
            .then((client) => {
                websocketCallbacks(client, (message) => {
                    if (this.shouldSkipCurrentNotification()) {
                        return;
                    }
                    const response = JSON.parse(message.payloadString);
                    if (!response.hasOwnProperty('data')) {
                        return;
                    }
                    const b64EncodedImage = response['data']['image'];
                    this.setState({'foundImage': b64EncodedImage, 'lastNotification' : Date.now()});
                })
            }, e => {
                console.log('failed', e);
            });
    }

    shouldSkipCurrentNotification() {
        return Date.now() - this.state.lastNotification < MINIMUM_TIME_BETWEEN_NOTIFICATION;
    }


    render() {
        return (
            <View style={styles.container}>
                <Text>Last found image</Text>
                <Image style={{width: 300, height: 300}}
                       source={{uri: `data:image/jpeg;base64,${this.state.foundImage}`}} />
            </View>
        );
    }
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#fff',
        alignItems: 'center',
        justifyContent: 'center',
    },
});