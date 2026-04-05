import React from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Settings, Search, Mic } from 'lucide-react-native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { RootStackParamList } from '../../navigation/AppNavigator';
import { colors } from '../../theme/colors';
import { MemoryCard } from '../../components/memory/MemoryCard';
import { MemoryState } from '../../components/ui/Badge';

type Props = {
  navigation: NativeStackNavigationProp<RootStackParamList, 'Home'>;
};

// Dummy data matching your HTML prototype
const RECENT_MEMORIES = [
  { id: '1', title: 'RAG pipeline architecture insights', status: 'FRESH' as MemoryState },
  { id: '2', title: 'UI idea for memory capture flow', status: 'ACTIVE' as MemoryState },
  { id: '3', title: 'Qdrant vector search optimization', status: 'FADING' as MemoryState },
  { id: '4', title: 'Old project brainstorm notes', status: 'ARCHIVED' as MemoryState },
  { id: '5', title: 'API design session notes', status: 'ARCHIVED' as MemoryState },
];

export default function HomeScreen({ navigation }: Props) {
  return (
    <SafeAreaView style={styles.container} edges={['top', 'bottom']}>
      {/* Header */}
      <View style={styles.header}>
        <View style={styles.logoRow}>
          <Text style={styles.logoText}>memora</Text>
          <View style={styles.logoDot} />
        </View>
        <TouchableOpacity hitSlop={{top: 10, bottom: 10, left: 10, right: 10}}>
          <Settings color={colors.text1} size={20} strokeWidth={1.4} />
        </TouchableOpacity>
      </View>

      {/* Memory List */}
      <View style={styles.listContainer}>
        <Text style={styles.sectionTitle}>Recent memories</Text>
        <ScrollView showsVerticalScrollIndicator={false} contentContainerStyle={styles.scrollContent}>
          {RECENT_MEMORIES.map((mem) => (
            <MemoryCard 
              key={mem.id}
              title={mem.title}
              status={mem.status}
              onPress={() => console.log(`Open memory ${mem.id}`)}
            />
          ))}
        </ScrollView>
      </View>

      {/* Bottom Action Area */}
      <View style={styles.actionArea}>
        <TouchableOpacity 
          style={styles.queryBar} 
          activeOpacity={0.8}
          onPress={() => navigation.navigate('Response')} // Mocking text search routing directly to response
        >
          <Search color={colors.text2} size={16} strokeWidth={1.5} />
          <Text style={styles.queryText}>how can I help you?</Text>
          <View style={styles.querySend}>
            <Search color="#FFFFFF" size={12} strokeWidth={2.5} />
          </View>
        </TouchableOpacity>

        <View style={styles.micContainer}>
          <TouchableOpacity 
            style={styles.micButton}
            activeOpacity={0.7}
            onPress={() => navigation.navigate('Listening')}
          >
            <Mic color={colors.text1} size={20} strokeWidth={1.6} />
          </TouchableOpacity>
        </View>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 20,
    paddingBottom: 14,
    paddingTop: 10,
  },
  logoRow: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    gap: 2,
  },
  logoText: {
    fontFamily: 'Georgia',
    fontStyle: 'italic',
    fontSize: 24,
    color: colors.text0,
    lineHeight: 28,
  },
  logoDot: {
    width: 4,
    height: 4,
    backgroundColor: colors.amber,
    borderRadius: 2,
    marginTop: 5,
  },
  listContainer: {
    flex: 1,
    paddingHorizontal: 14,
  },
  sectionTitle: {
    fontSize: 11,
    color: colors.text2,
    letterSpacing: 0.77, // ~0.07em of 11px
    textTransform: 'uppercase',
    marginBottom: 10,
    paddingHorizontal: 2,
  },
  scrollContent: {
    paddingBottom: 20,
  },
  actionArea: {
    paddingHorizontal: 14,
    paddingBottom: 16,
    paddingTop: 10,
  },
  queryBar: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 10,
    backgroundColor: colors.surface1,
    borderWidth: 0.5,
    borderColor: colors.border1,
    borderRadius: 50,
    paddingVertical: 9,
    paddingLeft: 15,
    paddingRight: 9,
    marginBottom: 12,
  },
  queryText: {
    flex: 1,
    fontSize: 13,
    color: colors.text2,
  },
  querySend: {
    width: 34,
    height: 34,
    backgroundColor: colors.amber,
    borderRadius: 17,
    alignItems: 'center',
    justifyContent: 'center',
  },
  micContainer: {
    alignItems: 'center',
  },
  micButton: {
    width: 46,
    height: 46,
    backgroundColor: colors.surface2,
    borderWidth: 0.5,
    borderColor: colors.border1,
    borderRadius: 23,
    alignItems: 'center',
    justifyContent: 'center',
  }
});