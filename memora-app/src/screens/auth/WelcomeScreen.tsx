import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { RootStackParamList } from '../../navigation/AppNavigator';
import { colors } from '../../theme/colors';
import { ButtonPill } from '../../components/ui/ButtonPill';

type Props = {
  navigation: NativeStackNavigationProp<RootStackParamList, 'Welcome'>;
};

export default function WelcomeScreen({ navigation }: Props) {
  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.content}>
        <View style={styles.logoRow}>
          <Text style={styles.logoText}>memora</Text>
          <View style={styles.logoDot} />
        </View>

        {/* You can pass the actual name from context/params later */}
        <Text style={styles.greeting}>Hello, Hrithik.</Text>
        
        <Text style={styles.description}>
          Your thoughts deserve to live on.{'\n'}
          Meet Memora — record your ideas{'\n'}
          now, recall them intelligently later.
        </Text>

        <ButtonPill 
          title="Continue" 
          onPress={() => navigation.reset({ index: 0, routes: [{ name: 'Home' }] })} 
        />
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
    paddingHorizontal: 28,
    paddingBottom: 36,
  },
  content: {
    flex: 1,
    justifyContent: 'center',
  },
  logoRow: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    gap: 2,
    marginBottom: 36,
  },
  logoText: {
    fontFamily: 'Georgia',
    fontStyle: 'italic',
    fontSize: 22,
    color: colors.text0,
  },
  logoDot: {
    width: 4,
    height: 4,
    backgroundColor: colors.amber,
    borderRadius: 2,
    marginTop: 4,
  },
  greeting: {
    fontSize: 30,
    fontWeight: '300',
    color: colors.text0,
    marginBottom: 20,
  },
  description: {
    fontSize: 14,
    color: colors.text2,
    lineHeight: 24,
    marginBottom: 40,
  }
});