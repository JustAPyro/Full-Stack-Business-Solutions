import {Text, TextInput, View, StyleSheet} from "react-native";
import styles from './styles';
import React from "react";
const LabeledTextInput = (props) => {
    const [text, onChangeText] = React.useState(null);
  return (
      <View>
        <Text style={styles.text}>{props.text}</Text>
         <TextInput
             style={styles.textInput}
             onChangeText={onChangeText}
             value={text}
         />
      </View>
  );
}



export default LabeledTextInput;