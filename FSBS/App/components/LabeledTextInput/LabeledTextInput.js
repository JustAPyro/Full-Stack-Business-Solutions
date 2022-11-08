import {Text, TextInput, View, StyleSheet} from "react-native";
import styles from './styles';
import React from "react";
const LabeledTextInput = (props) => {
  return (
      <View>
        <Text style={styles.text}>{props.textHeader}</Text>
         <TextInput
             style={styles.textInput}
             onChangeText={(textVal) => props.callback(textVal)}
             textContentType={props.type}
             secureTextEntry={props.secure}
         />
      </View>
  );
}



export default LabeledTextInput;