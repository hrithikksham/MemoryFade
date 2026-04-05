import React, { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { ChevronLeft, ArrowRight } from 'lucide-react-native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { RootStackParamList } from '../../navigation/AppNavigator';
import { colors } from '../../theme/colors';
import { InputField } from '../../components/ui/InputField';
import { ButtonCircular } from '../../components/ui/ButtonCircular';

type Props = { navigation: NativeStackNavigationProp<RootStackParamList, 'Name'>; };

export default function NameScreen({ navigation }: Props) {
  const [name, setName] = useState('');

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => navigation.goBack()} hitSlop={{top: 10, bottom: 10, left: 10, right: 10}}>
          <ChevronLeft color={colors.text1} size={24} strokeWidth={1.8} />
        </TouchableOpacity>
        <Text style={styles.step}>1 of 3</Text>
      </View>

      <View style={styles.content}>
        <Text style={styles.title}>What's your name?</Text>
        <InputField 
          placeholder="Your full name" 
          value={name}
          onChangeText={setName}
          autoFocus
        />
      </View>

      <View style={styles.footer}>
        <ButtonCircular onPress={() => navigation.navigate('Email')} disabled={!name}>
          <ArrowRight color="#FFFFFF" size={20} strokeWidth={2} />
        </ButtonCircular>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background, paddingHorizontal: 28, paddingBottom: 36 },
  header: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', paddingVertical: 20, marginBottom: 20 },
  step: { fontSize: 12, color: colors.text2 },
  content: { flex: 1, justifyContent: 'center', marginBottom: 40 },
  title: { fontSize: 24, fontWeight: '300', color: colors.text0, marginBottom: 32 },
  footer: { alignItems: 'flex-end' }
});