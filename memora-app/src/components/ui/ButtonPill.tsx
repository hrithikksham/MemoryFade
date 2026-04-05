import React from 'react';
import { TouchableOpacity, Text, StyleSheet, TouchableOpacityProps, ViewStyle, TextStyle } from 'react-native';
import { colors } from '../../theme/colors';

interface ButtonPillProps extends TouchableOpacityProps {
  title: string;
  variant?: 'solid' | 'ghost';
  style?: ViewStyle;
  textStyle?: TextStyle;
}

export const ButtonPill: React.FC<ButtonPillProps> = ({ 
  title, 
  variant = 'solid', 
  style, 
  textStyle, 
  ...rest 
}) => {
  const isGhost = variant === 'ghost';

  return (
    <TouchableOpacity
      style={[styles.base, isGhost ? styles.ghost : styles.solid, style]}
      activeOpacity={0.8}
      {...rest}
    >
      <Text style={[styles.textBase, isGhost ? styles.textGhost : styles.textSolid, textStyle]}>
        {title}
      </Text>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  base: {
    borderRadius: 50,
    paddingVertical: 16,
    paddingHorizontal: 32,
    width: '100%',
    alignItems: 'center',
    justifyContent: 'center',
  },
  solid: {
    backgroundColor: colors.amber,
  },
  ghost: {
    backgroundColor: colors.surface2,
    borderWidth: 0.5,
    borderColor: colors.border2,
  },
  textBase: {
    fontSize: 14,
    fontWeight: '600',
    letterSpacing: 0.35, // roughly 0.025em of 14px
  },
  textSolid: {
    color: '#FFFFFF',
  },
  textGhost: {
    color: colors.text1,
  }
});