import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

import SplashScreen from '../screens/onboarding/SplashScreen';
import OnboardingScreen from '../screens/onboarding/OnboardingScreen';
import NameScreen from '../screens/auth/NameScreen';
import EmailScreen from '../screens/auth/EmailScreen';
import PasswordScreen from '../screens/auth/PasswordScreen';
import WelcomeScreen from '../screens/auth/WelcomeScreen';
import LoginScreen from '../screens/auth/LoginScreen';
import HomeScreen from '../screens/main/HomeScreen';
import ListeningScreen from '../screens/main/ListeningScreen';
import ResponseScreen from '../screens/main/ResponseScreen';

// Type definition for safe routing
export type RootStackParamList = {
  Splash: undefined;
  Onboarding: undefined;
  Name: undefined;
  Email: undefined;
  Password: undefined;
  Welcome: undefined;
  Login: undefined;
  Home: undefined;
  Listening: undefined;
  Response: {query: string}; 
};

const Stack = createNativeStackNavigator<RootStackParamList>();

export const AppNavigator = () => {
  return (
    <NavigationContainer>
      <Stack.Navigator 
        initialRouteName="Splash"
        screenOptions={{
          headerShown: false,
          animation: 'fade', // Mimics your CSS transition: opacity 0.32s ease
          contentStyle: { backgroundColor: '#080808' } // Global background
        }}
      >
        {/* Onboarding Flow */}
        <Stack.Screen name="Splash" component={SplashScreen} />
        <Stack.Screen name="Onboarding" component={OnboardingScreen} />
        
        {/* Auth Flow */}
        
        <Stack.Screen name="Name" component={NameScreen} />
        <Stack.Screen name="Email" component={EmailScreen} />
        <Stack.Screen name="Password" component={PasswordScreen} />
        <Stack.Screen name="Welcome" component={WelcomeScreen} />
        

        
        {/* Main App Flow */}
        <Stack.Screen name="Login" component={LoginScreen} />
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen name="Listening" component={ListeningScreen} />
        <Stack.Screen name="Response" component={ResponseScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
};