import {Text, TextInput, View, StyleSheet} from "react-native";
import React from "react";
import styles from './styles';

const TextInputGroup = ({ inputs }) => {
  return (
      <TextInputRow inputs={['1', '2', '3']}/>
  );
}

const TextInputRow = ({ inputs }) => {
  return (
      <View style={styles.rowViewStyle}>
          {inputs.map(() => (
              <TextInput style={styles.textInput}></TextInput>
          ))}
      </View>
  )
};


export default TextInputGroup;