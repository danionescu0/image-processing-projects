import React from 'react';
import { Image } from 'react-native';
import { StyleSheet, Text, View } from 'react-native';
import {websocketCallbacks, websocketClientConnect} from './src/utils/websockets'


export default class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            foundImage: null
        }
    }

    componentDidMount() {
        this.connectToWebsocket();
    }

    connectToWebsocket() {
        websocketClientConnect('faces')
            .then((client) => {
                console.log(client);
                websocketCallbacks(client, (message) => {
                    response = JSON.parse(message.payloadString);
                    if (!response.hasOwnProperty('data')) {
                        return;
                    }
                    b64EncodedImage = response['data']['image'];
                    this.setState({'foundImage': b64EncodedImage});
                })
            }, e => {
                console.log('failed', e);
            });
    }

    render() {
        return (
            <View style={styles.container}>
                <Text>Last found image</Text>
                <Image style={{width: 300, height: 300}} source={{uri: `data:image/jpeg;base64,${this.state.foundImage}`}} />
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