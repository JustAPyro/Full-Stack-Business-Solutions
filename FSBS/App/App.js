import { StatusBar } from 'expo-status-bar';
import {Alert, Button, StyleSheet, Text, TouchableOpacity, View} from 'react-native';
import { LabeledTextInput } from './components/LabeledTextInput'
import { TextInputGroup } from "./components/TextInputGroup";
import { useState } from "react";
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import * as SecureStore from 'expo-secure-store';



function NewTransactionPage({ navigation }) {
    const [transactionLocation, setLocation] = useState()
    const [transactionAmount, setAmount] = useState()
    const [transactionTax, setTax] = useState()

    const submitBtnHandler = () => {

        const cost = transactionAmount * 100;
        const tax = transactionTax * 100;

        if (!transactionLocation.trim().length) {
            alert("Please fill in transaction location.");
            return;
        }
        if (cost - Math.floor(cost) !== 0) {
            alert("Transaction cost must not have more than two decimal places.")
            return;
        }
        if (tax - Math.floor(tax) !== 0) {
            alert("Tax must not have more than two decimal places")
            return;
        }

        api_post_transaction({
            location: transactionLocation,
            cost: transactionAmount,
            tax: transactionTax})
            .then((status) => {
            if (status===200) {
                alert("Transaction posted successfully!")

            } else
                alert("Error posting transaction!")
        })};

    return (
    <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center', paddingBottom: 325 }}>
        <LabeledTextInput textHeader="Location" callback={setLocation} />
        <LabeledTextInput textHeader="$ Amount" keyboardType={'numeric'} callback={setAmount} />
        <LabeledTextInput textHeader="Tax" keyboardType={'numeric'} callback={setTax} />
        <TouchableOpacity style = {styles.confirmBtn} onPress={submitBtnHandler}>
            <Text >
               Submit
           </Text>
        </TouchableOpacity >
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
                    alert("Failed to log in. Error: " + response.ERROR)
                }
                if (response.hasOwnProperty('auth_token')) {
                    void SecureStore.setItemAsync('Authorization', response.auth_token)
                    void navigation.navigate('NewTransaction')
                }
            })
            .catch((error) => console.error(error))
    }

  return (
    <View style={styles.container}>
      <LabeledTextInput textHeader="E-mail:" callback={setEmail} type="username"/>
      <LabeledTextInput textHeader="Password:" callback={setPass} type="password" secure />
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
        <Stack.Navigator initialRouteName="NewTransaction">
            <Stack.Screen name="Login" component={LoginPage} />
            <Stack.Screen name="NewTransaction" component={NewTransactionPage} />
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

const api_post_transaction = (props) => {
    return SecureStore.getItemAsync('Authorization').then((auth) => {
        return fetch('https://fullstackbusinesssolutions.herokuapp.com/transaction', {
            method: 'POST',
            headers: {
                Accept: '*/*',
                'Content-Type': 'application/json',
                'Authorization': auth
            },
            body: JSON.stringify({
                location: props.location,
                cost: props.cost,
                tax: props.tax
            })
        })
            .then((response) => {
                return response.status
            })
            .catch((error) => {
                console.error(error);
            });
    }).catch((error) => {console.error(error)})
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#fff',
        alignItems: 'center',
        justifyContent: 'center',
        paddingBottom: 200
    },
    confirmBtn: {
        marginTop: 20,
        paddingHorizontal: 50,
        paddingVertical: 10,
        borderWidth: 3,
        backgroundColor: '#fff',
        borderRadius: 12,
    }
});

export default App;