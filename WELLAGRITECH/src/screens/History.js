import React, { useEffect, useState } from 'react';
import { View, Text, FlatList } from 'react-native';
import { getDevices, getHistory } from '../services/api';

export default function History() {
  const [items, setItems] = useState([]);

  useEffect(() => {
    (async () => {
      const { data } = await getDevices();
      if (data.length) {
        const res = await getHistory({ device_id: data[0].device_id, limit: 50 });
        setItems(res.data);
      }
    })();
  }, []);

  return (
    <View style={{ padding: 16 }}>
      <Text style={{ fontSize: 22, marginBottom: 12 }}>Historique</Text>
      <FlatList
        data={items}
        keyExtractor={(_, idx) => String(idx)}
        renderItem={({ item }) => (
          <View style={{ paddingVertical: 8, borderBottomWidth: 1, borderColor: '#eee' }}>
            <Text>{item.timestamp} — H:{item.humidite_sol} — N:{item.niveau_eau} — P:{item.etat_pompe ? 'ON' : 'OFF'}</Text>
          </View>
        )}
      />
    </View>
  );
}