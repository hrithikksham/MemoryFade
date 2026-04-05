import React, { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { ChevronLeft } from 'lucide-react-native';
import { saveToken } from '../../services/auth';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { RootStackParamList } from '../../navigation/AppNavigator';
import { colors } from '../../theme/colors';
import { InputField } from '../../components/ui/InputField';
import { ButtonPill } from '../../components/ui/ButtonPill';
import axios from 'axios';

type Props = { navigation: NativeStackNavigationProp<RootStackParamList, 'Login'>; };

export default function LoginScreen({ navigation }: Props) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async () => {
  try {
    // 1. Authenticate directly with Supabase via their REST API using Axios
    // (Replace with your actual Supabase URL and Anon Key from your Python settings)
    const response = await axios.post(
      'https://zizfygdqcfcxhonawffk.supabase.co/auth/v1/token?grant_type=password',
      {
        email: email,
        password: password,
      },
      {
        headers: {
          'apikey': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InppemZ5Z2RxY2ZjeGhvbmF3ZmZrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzM2NTAyNDEsImV4cCI6MjA4OTIyNjI0MX0.j0NNE6Z6aBjnyVtfyn8kLrxDIPID1hkEgSx8CMbhKXM',
          'Content-Type': 'application/json',
        }
      }
    );

    const { access_token } = response.data;

    // 2. Save the JWT to the device's SecureStore
    await saveToken(access_token);

    // 3. Navigate to the Home screen
    navigation.reset({ index: 0, routes: [{ name: 'Home' }] });

  } catch (error) {
    console.error("Login failed:", error);
    // You could add an Alert here to tell the user the password was wrong
  }
};

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => navigation.goBack()} hitSlop={{top: 10, bottom: 10, left: 10, right: 10}}>
          <ChevronLeft color={colors.text1} size={24} strokeWidth={1.8} />
        </TouchableOpacity>
      </View>

      <View style={styles.content}>
        <Text style={styles.title}>Welcome back.</Text>
        
        <View style={styles.inputGroup}>
          <InputField 
            placeholder="Email address" 
            value={email}
            onChangeText={setEmail}
            keyboardType="email-address"
            autoCapitalize="none"
          />
          <InputField 
            placeholder="Password" 
            value={password}
            onChangeText={setPassword}
            secureTextEntry
          />
        </View>
      </View>

      <View style={styles.footer}>
        <ButtonPill 
          title="Log in" 
          onPress={handleLogin}
          disabled={!email || !password}
        />
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background, paddingHorizontal: 28, paddingBottom: 36 },
  header: { paddingVertical: 20, marginBottom: 20 },
  content: { flex: 1, justifyContent: 'center', marginBottom: 40 },
  title: { fontSize: 28, fontWeight: '300', color: colors.text0, marginBottom: 40 },
  inputGroup: { gap: 24 },
  footer: { paddingBottom: 10 }
});