import { StatusBar } from 'expo-status-bar';
import { Alert, Button, StyleSheet, Text, View } from 'react-native';
import { LabeledTextInput } from './components/LabeledTextInput'
import { useState } from "react";
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import * as SecureStore from 'expo-secure-store';



function NewPage({ navigation }) {
    return (
    <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
      <Text>Details Screen</Text>
        <Button
            title="Log In"
            onPress={() => {
            SecureStore.getItemAsync('auth_token')
                .then((x) => {alert(x)})
        }}/>
    </View>
  );
}

function LoginPage({ navigation }) {
    const [input_email, setEmail] = useState()
    const [input_pass, setPass] = useState()

    const loginBtnHandler = () => {
        api_auth({email: input_email, pass: input_pass})
            .then((response) => {
                if (response.hasOwnProperty('ERROR')) {
                    alert("Failed to log in")
                }
                if (response.hasOwnProperty('auth_token')) {
                    SecureStore.setItemAsync('auth_token', response.auth_token)
                    navigation.navigate('Details').catch((error) => console.error(error))
                }
            })
            .catch((error) => console.error(error))
    }

  return (
    <View style={styles.container}>
      <LabeledTextInput textHeader="E-mail:" callback={setEmail}/>
      <LabeledTextInput textHeader="Password:" callback={setPass}/>
      <Button
          title={"Log In"}
          onPress={loginBtnHandler}
      />
      <StatusBar style="auto" />
    </View>
  );
}

const Stack = createNativeStackNavigator();
function App() {
    return <NavigationContainer>
        <Stack.Navigator initialRouteName="Login">
            <Stack.Screen name="Login" component={LoginPage} />
            <Stack.Screen name="Details" component={NewPage} />
        </Stack.Navigator>
    </NavigationContainer>
}



const api_signup = (props) => {
    console.log(JSON.stringify({
        'email': props.email,
        'password': props.password,
        'first_name': props.first_name,
        'last_name': props.last_name,
        'phone': props.phone
    }))
    return fetch('https://fullstackbusinesssolutions.herokuapp.com/register', {
        method: 'POST',
        headers: {
            Accept: '*/*',
            'Content-Type': 'application/json'},
        body: JSON.stringify({
            'email': props.email,
            'password': props.password,
            'first_name': props.first_name,
            'last_name': props.last_name,
            'phone': props.phone
        })})
        .then((response) => response.text())
        .then((json) => {
            console.log(json)
        })
        .catch((error) => {
            console.error(error)
        });
};



const api_auth = (props) => {
  return fetch('https://fullstackbusinesssolutions.herokuapp.com/authorize', {
      method: 'POST',
      headers: {
          Accept: '*/*',
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({
          email: props.email,
          password: props.pass
      })})
      .then((response) => response.text())
      .then((json) => {
          return JSON.parse(json)
      })
      .catch((error) => {
          console.error(error);
      });
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
    paddingBottom: 200
  },
});

export default App;