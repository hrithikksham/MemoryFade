import React from 'react';
import { TouchableOpacity, StyleSheet, TouchableOpacityProps, ViewStyle } from 'react-native';
import { colors } from '../../theme/colors';

interface ButtonCircularProps extends TouchableOpacityProps {
  children: React.ReactNode;
  style?: ViewStyle;
}

export const ButtonCircular: React.FC<ButtonCircularProps> = ({ children, style, ...rest }) => {
  return (
    <TouchableOpacity 
      style={[styles.button, style]} 
      activeOpacity={0.8} 
      {...rest}
    >
      {children}
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  button: {
    width: 52,
    height: 52,
    backgroundColor: colors.amber,
    borderRadius: 26, // half of width/height makes it a perfect circle
    alignItems: 'center',
    justifyContent: 'center',
  }
});