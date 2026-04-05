import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity, ActivityIndicator } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { ChevronLeft, Search } from 'lucide-react-native';
import { NativeStackScreenProps } from '@react-navigation/native-stack';
import { RootStackParamList } from '../../navigation/AppNavigator';
import { colors } from '../../theme/colors';
import { queryMemory, QueryResponse } from '../../services/api';

type Props = NativeStackScreenProps<RootStackParamList, 'Response'>;

export default function ResponseScreen({ route, navigation }: Props) {
  const { query } = route.params; // The text passed from HomeScreen
  
  const [isLoading, setIsLoading] = useState(true);
  const [result, setResult] = useState<QueryResponse | null>(null);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchAnswer = async () => {
      try {
        setIsLoading(true);
        // Calls your FastAPI backend!
        const data = await queryMemory(query);
        setResult(data);
      } catch (err) {
        setError('Failed to retrieve memory. Please try again.');
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchAnswer();
  }, [query]);

  return (
    <SafeAreaView style={styles.container} edges={['top', 'bottom']}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => navigation.goBack()} style={styles.backButton}>
          <ChevronLeft color={colors.text1} size={18} strokeWidth={2} />
          <Text style={styles.backText}>Back</Text>
        </TouchableOpacity>
      </View>

      <ScrollView style={styles.chatArea} contentContainerStyle={styles.chatContent}>
        {/* User Query */}
        <View style={styles.userBubbleContainer}>
          <View style={styles.userBubble}>
            <Text style={styles.userBubbleText}>{query}</Text>
          </View>
        </View>

        {/* Loading State */}
        {isLoading && (
          <ActivityIndicator size="small" color={colors.amber} style={{ marginTop: 20 }} />
        )}

        {/* Error State */}
        {error ? (
          <Text style={{ color: colors.text2, textAlign: 'center' }}>{error}</Text>
        ) : null}

        {/* AI Response & Citations */}
        {!isLoading && result && (
          <View style={styles.responseCard}>
            <View style={styles.responseHeader}>
              <View style={styles.amberDot} />
              <Text style={styles.responseTitle}>Memora answer</Text>
            </View>
            
            <Text style={styles.responseText}>{result.answer}</Text>

            {/* Render dynamic citations based on returned memory texts */}
            {result.top_memories.map((memoryText, index) => (
              <View key={index} style={styles.citation}>
                <View style={styles.citationNumContainer}>
                  <Text style={styles.citationNumText}>{index + 1}</Text>
                </View>
                <Text style={styles.citationText} numberOfLines={2}>
                  {memoryText}
                </Text>
              </View>
            ))}
          </View>
        )}
      </ScrollView>
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
    paddingHorizontal: 14,
    paddingVertical: 10,
  },
  backButton: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
  },
  backText: {
    color: colors.text1,
    fontSize: 14,
  },
  chatArea: {
    flex: 1,
    paddingHorizontal: 14,
  },
  chatContent: {
    paddingTop: 10,
    paddingBottom: 20,
  },
  userBubbleContainer: {
    alignItems: 'flex-end',
    marginBottom: 20,
  },
  userBubble: {
    backgroundColor: colors.surface2,
    borderWidth: 0.5,
    borderColor: colors.border1,
    borderRadius: 18,
    borderTopRightRadius: 4, // creates the chat bubble tail effect
    paddingVertical: 10,
    paddingHorizontal: 14,
    maxWidth: '80%',
  },
  userBubbleText: {
    color: colors.text1,
    fontSize: 13,
    lineHeight: 20,
  },
  responseCard: {
    backgroundColor: colors.surface1,
    borderWidth: 0.5,
    borderColor: colors.border1,
    borderRadius: 14,
    padding: 15,
  },
  responseHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 7,
    marginBottom: 12,
  },
  amberDot: {
    width: 6,
    height: 6,
    borderRadius: 3,
    backgroundColor: colors.amber,
  },
  responseTitle: {
    fontSize: 12,
    fontWeight: '600',
    color: colors.amber,
    letterSpacing: 0.36, // ~0.03em of 12px
  },
  responseText: {
    fontSize: 13,
    color: colors.text1,
    lineHeight: 22,
    marginBottom: 16,
  },
  citation: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    gap: 8,
    paddingTop: 10,
    marginTop: 4,
    borderTopWidth: 0.5,
    borderTopColor: colors.border0,
  },
  citationNumContainer: {
    backgroundColor: colors.surface2,
    borderWidth: 0.5,
    borderColor: colors.border2,
    paddingVertical: 2,
    paddingHorizontal: 6,
    borderRadius: 20,
    marginTop: 2, // align with text visually
  },
  citationNumText: {
    fontSize: 9,
    color: colors.amber,
    fontWeight: '600',
  },
  citationText: {
    flex: 1,
    fontSize: 11,
    color: colors.text2,
    lineHeight: 16,
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
  }
});