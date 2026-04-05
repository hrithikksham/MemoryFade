import React, { useState } from 'react';
import { TextInput, StyleSheet, TextInputProps, ViewStyle } from 'react-native';
import { colors } from '../../theme/colors';

interface InputFieldProps extends TextInputProps {
  containerStyle?: ViewStyle;
}

export const InputField: React.FC<InputFieldProps> = ({ 
  containerStyle, 
  onFocus, 
  onBlur, 
  ...rest 
}) => {
  const [isFocused, setIsFocused] = useState(false);

  return (
    <TextInput
      style={[
        styles.input,
        { borderBottomColor: isFocused ? colors.amber : colors.border2 },
        containerStyle
      ]}
      placeholderTextColor={colors.text2}
      onFocus={(e) => {
        setIsFocused(true);
        onFocus && onFocus(e);
      }}
      onBlur={(e) => {
        setIsFocused(false);
        onBlur && onBlur(e);
      }}
      {...rest}
    />
  );
};

const styles = StyleSheet.create({
  input: {
    color: colors.text0,
    fontSize: 16,
    paddingVertical: 13,
    width: '100%',
    borderBottomWidth: 1,
  }
});