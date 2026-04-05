import React, { useEffect } from 'react';
import { View, StyleSheet } from 'react-native';
import Animated, { 
  useSharedValue, 
  useAnimatedStyle, 
  withRepeat, 
  withSequence, 
  withTiming, 
  Easing 
} from 'react-native-reanimated';
import { colors } from '../../theme/colors';

const HEIGHTS = [8, 14, 24, 38, 52, 38, 52, 40, 28, 18, 10, 6];

const WaveBar = ({ height, delay }: { height: number; delay: number }) => {
  const scaleY = useSharedValue(0.3);

  useEffect(() => {
    const duration = 650 + Math.random() * 400; // Mimicking your JS duration logic
    
    setTimeout(() => {
      scaleY.value = withRepeat(
        withSequence(
          withTiming(1, { duration: duration / 2, easing: Easing.inOut(Easing.ease) }),
          withTiming(0.3, { duration: duration / 2, easing: Easing.inOut(Easing.ease) })
        ),
        -1,
        false
      );
    }, delay);
  }, [delay, scaleY]);

  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ scaleY: scaleY.value }]
  }));

  return <Animated.View style={[styles.bar, { height }, animatedStyle]} />;
};

export const WaveVisualizer = () => {
  return (
    <View style={styles.container}>
      {HEIGHTS.map((h, i) => (
        <WaveBar key={i} height={h} delay={i * 70} /> // Mimics (i * 0.07)s delay
      ))}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
    height: 60,
    marginBottom: 24,
  },
  bar: {
    width: 3,
    backgroundColor: colors.amber,
    borderRadius: 2,
    // transformOrigin isn't fully supported in React Native StyleSheet the same way, 
    // but scaleY works natively from the center which looks perfectly fine for voice waves.
  }
});