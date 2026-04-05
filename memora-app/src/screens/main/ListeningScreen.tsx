import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Mic } from 'lucide-react-native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { RootStackParamList } from '../../navigation/AppNavigator';
import { colors } from '../../theme/colors';
import { PulsingRing } from '../../components/animations/PulsingRing';
import { WaveVisualizer } from '../../components/animations/WaveVisualizer';
import { ButtonPill } from '../../components/ui/ButtonPill';

type Props = {
  navigation: NativeStackNavigationProp<RootStackParamList, 'Listening'>;
};

export default function ListeningScreen({ navigation }: Props) {
  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.content}>
        {/* Background Animations */}
        <PulsingRing size={160} />
        <PulsingRing size={220} delay={550} />
        
        {/* Central Mic Icon */}
        <View style={styles.micCircle}>
          <Mic color="#FFFFFF" size={28} strokeWidth={1.8} />
        </View>

        {/* Audio Wave Visualizer */}
        <WaveVisualizer />

        <Text style={styles.statusText}>Listening...</Text>
        <Text style={styles.subText}>
          Speak your thought — Memora will capture and index it.
        </Text>
      </View>

      <View style={styles.footer}>
        <ButtonPill 
          title="Done" 
          variant="ghost" 
          onPress={() => navigation.replace('Response')} 
        />
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  content: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
  micCircle: {
    width: 72,
    height: 72,
    borderRadius: 36,
    backgroundColor: colors.amber,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 36,
    zIndex: 1,
  },
  statusText: {
    fontSize: 17,
    color: colors.text0,
    fontWeight: '300',
    marginBottom: 8,
  },
  subText: {
    fontSize: 13,
    color: colors.text2,
    textAlign: 'center',
    maxWidth: 220,
    lineHeight: 20,
  },
  footer: {
    paddingHorizontal: 80, // Constrains button width
    paddingBottom: 40,
  }
});