import React, { useEffect } from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { RootStackParamList } from '../../navigation/AppNavigator';
import { colors } from '../../theme/colors';
import { PulsingRing } from '../../components/animations/PulsingRing';

type Props = {
  navigation: NativeStackNavigationProp<RootStackParamList, 'Splash'>;
};

export default function SplashScreen({ navigation }: Props) {
  useEffect(() => {
    const timer = setTimeout(() => {
      navigation.replace('Onboarding');
    }, 2500); // Transitions after 2.5s
    return () => clearTimeout(timer);
  }, [navigation]);

  return (
    <View style={styles.container}>
      <PulsingRing size={180} />
      <PulsingRing size={280} delay={800} />
      <PulsingRing size={380} delay={1600} />
      
      <View style={styles.logoContainer}>
        <View style={styles.logoRow}>
          <Text style={styles.logoText}>memora</Text>
          <View style={styles.logoDot} />
        </View>
        <Text style={styles.subtitle}>MEMORY SYSTEM</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
    alignItems: 'center',
    justifyContent: 'center',
  },
  logoContainer: {
    alignItems: 'flex-end',
    gap: 4,
  },
  logoRow: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    gap: 4,
  },
  logoText: {
    fontFamily: 'Georgia', // React Native fallback for Palatino/serif
    fontStyle: 'italic',
    fontSize: 44,
    color: colors.text0,
    lineHeight: 44,
  },
  logoDot: {
    width: 7,
    height: 7,
    backgroundColor: colors.amber,
    borderRadius: 3.5,
    marginTop: 6,
  },
  subtitle: {
    fontSize: 11,
    letterSpacing: 2,
    color: colors.text2,
    marginRight: 11,
  }
});