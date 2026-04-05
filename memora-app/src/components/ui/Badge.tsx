import React from 'react';
import { View, Text, StyleSheet, ViewStyle } from 'react-native';
import { colors } from '../../theme/colors';

export type MemoryState = 'FRESH' | 'ACTIVE' | 'FADING' | 'ARCHIVED';

interface BadgeProps {
  status: MemoryState;
  style?: ViewStyle;
}

export const Badge: React.FC<BadgeProps> = ({ status, style }) => {
  const getStyles = () => {
    switch (status) {
      case 'FRESH':
        return { bg: 'rgba(0,196,174,0.12)', text: colors.fresh };
      case 'ACTIVE':
        return { bg: 'rgba(78,196,110,0.12)', text: colors.active };
      case 'FADING':
        return { bg: 'rgba(224,120,64,0.12)', text: colors.amber };
      case 'ARCHIVED':
        return { bg: 'rgba(255,255,255,0.05)', text: colors.text2 };
      default:
        return { bg: 'transparent', text: colors.text0 };
    }
  };

  const statusColors = getStyles();

  return (
    <View style={[styles.container, { backgroundColor: statusColors.bg }, style]}>
      <Text style={[styles.text, { color: statusColors.text }]}>
        {status}
      </Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    paddingVertical: 3,
    paddingHorizontal: 7,
    borderRadius: 20,
    alignSelf: 'flex-start', // prevents the badge from stretching full width
  },
  text: {
    fontSize: 9,
    fontWeight: '600',
    letterSpacing: 0.54, // roughly 0.06em of 9px
    textTransform: 'uppercase',
  }
});