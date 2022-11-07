import {StatusBar} from 'expo-status-bar';
import {Alert, Button, StyleSheet, View} from 'react-native';
import {LabeledTextInput} from './components/LabeledTextInput'
import {useState} from "react";

const App = () => {
    const [input_email, setEmail] = useState()
    const [input_pass, setPass] = useState()

    const loginBtnHandler = () => {
        console.log("Button is being hit!")
        console.log(input_email)
        api_auth({email: input_email, pass:input_pass})
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
          console.log(json)
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