import React, { useEffect } from 'react';
import { StyleSheet } from 'react-native';
import Animated, { 
  useSharedValue, 
  useAnimatedStyle, 
  withRepeat, 
  withSequence, 
  withTiming, 
  Easing 
} from 'react-native-reanimated';

interface PulsingRingProps {
  size: number;
  delay?: number;
}

export const PulsingRing: React.FC<PulsingRingProps> = ({ size, delay = 0 }) => {
  const scale = useSharedValue(1);
  const opacity = useSharedValue(0.5);

  useEffect(() => {
    const duration = 1500; // Half of your 3s total duration to loop up and down
    
    const animate = () => {
      scale.value = withRepeat(
        withSequence(
          withTiming(1.18, { duration, easing: Easing.inOut(Easing.ease) }),
          withTiming(1, { duration, easing: Easing.inOut(Easing.ease) })
        ),
        -1, // -1 means infinite loop
        false
      );

      opacity.value = withRepeat(
        withSequence(
          withTiming(0.18, { duration, easing: Easing.inOut(Easing.ease) }),
          withTiming(0.5, { duration, easing: Easing.inOut(Easing.ease) })
        ),
        -1,
        false
      );
    };

    if (delay > 0) {
      setTimeout(animate, delay);
    } else {
      animate();
    }
  }, [delay, scale, opacity]);

  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ scale: scale.value }],
    opacity: opacity.value,
  }));

  return (
    <Animated.View
      style={[
        styles.ring,
        { width: size, height: size, borderRadius: size / 2 },
        animatedStyle,
      ]}
    />
  );
};

const styles = StyleSheet.create({
  ring: {
    position: 'absolute',
    borderWidth: 1,
    borderColor: 'rgba(224,120,64,0.1)', // Amber with 10% opacity
  }
});