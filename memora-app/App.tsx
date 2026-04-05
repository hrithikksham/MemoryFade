import React from 'react';
import { StatusBar } from 'react-native';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { AppNavigator } from './src/navigation/AppNavigator';

export default function App() {
  return (
    <SafeAreaProvider>
      {/* Memora uses a dark UI, so we force light text on the OS status bar */}
      <StatusBar 
        barStyle="light-content" 
        backgroundColor="#080808" 
        translucent={true} 
      />
      <AppNavigator />
    </SafeAreaProvider>
  );
}