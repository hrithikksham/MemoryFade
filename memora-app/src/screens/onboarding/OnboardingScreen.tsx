import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { SafeAreaView } from 'react-native-safe-area-context';
import { RootStackParamList } from '../../navigation/AppNavigator';
import { colors } from '../../theme/colors';
import { ButtonPill } from '../../components/ui/ButtonPill';

type Props = {
  navigation: NativeStackNavigationProp<RootStackParamList, 'Onboarding'>;
};

export default function OnboardingScreen({ navigation }: Props) {
  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.spacer} />
      
      <Text style={styles.headline}>
        Your ideas{'\n'}shouldn't{'\n'}disappear.
      </Text>
      
      <Text style={styles.description}>
        Memora captures your thoughts and surfaces them — precisely when you need them.
      </Text>
      
      <ButtonPill 
        title="Start remembering" 
        onPress={() => navigation.navigate('Name')} 
      />
      
      {/* New Login Link for existing users */}
      <TouchableOpacity 
        style={styles.loginContainer} 
        onPress={() => navigation.navigate('Login')}
      >
        <Text style={styles.loginText}>
          Already have an account? <Text style={styles.loginTextBold}>Log in</Text>
        </Text>
      </TouchableOpacity>
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
  spacer: {
    flex: 1,
  },
  headline: {
    fontFamily: 'Georgia',
    fontSize: 38,
    color: colors.text0,
    lineHeight: 42,
    marginBottom: 18,
  },
  description: {
    fontSize: 14,
    color: colors.text1,
    lineHeight: 24,
    marginBottom: 40,
  },
  loginContainer: {
    marginTop: 20,
    alignItems: 'center',
    paddingVertical: 10,
  },
  loginText: {
    color: colors.text2,
    fontSize: 13,
  },
  loginTextBold: {
    color: colors.text0,
    fontWeight: '600',
  }
});