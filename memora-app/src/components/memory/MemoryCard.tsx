import React from 'react';
import { TouchableOpacity, Text, StyleSheet } from 'react-native';
import { ChevronRight } from 'lucide-react-native';
import { colors } from '../../theme/colors';
import { Badge, MemoryState } from '../ui/Badge';

interface MemoryCardProps {
  title: string;
  status: MemoryState;
  onPress?: () => void;
}

export const MemoryCard: React.FC<MemoryCardProps> = ({ title, status, onPress }) => {
  const isArchived = status === 'ARCHIVED';

  return (
    <TouchableOpacity 
      style={[styles.card, isArchived && styles.archivedCard]} 
      activeOpacity={0.7}
      onPress={onPress}
    >
      <Badge status={status} />
      <Text style={[styles.title, isArchived && styles.archivedText]} numberOfLines={1}>
        {title}
      </Text>
      <ChevronRight color={colors.text3} size={16} strokeWidth={1.5} />
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  card: {
    backgroundColor: colors.surface1,
    borderWidth: 0.5,
    borderColor: colors.border0,
    borderRadius: 14,
    paddingVertical: 13,
    paddingHorizontal: 15,
    flexDirection: 'row',
    alignItems: 'center',
    gap: 10,
    marginBottom: 7,
  },
  archivedCard: {
    opacity: 0.38,
  },
  title: {
    fontSize: 13,
    color: colors.text0,
    flex: 1,
  },
  archivedText: {
    color: colors.text2,
  }
});