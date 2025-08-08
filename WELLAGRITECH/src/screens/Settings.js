import React, { useEffect, useState } from 'react';
import { View, Text, Switch, TextInput, Button } from 'react-native';
import { getSettings, updateSettings } from '../services/api';

export default function Settings() {
  const [threshold, setThreshold] = useState('');
  const [notif, setNotif] = useState(true);

  useEffect(() => {
    (async () => {
      const { data } = await getSettings();
      setThreshold(String(data.humidite_seuil));
      setNotif(!!data.notifications_enabled);
    })();
  }, []);

  const save = async () => {
    await updateSettings({ humidite_seuil: parseFloat(threshold), notifications_enabled: notif });
  };

  return (
    <View style={{ padding: 16 }}>
      <Text style={{ fontSize: 22, marginBottom: 12 }}>Paramètres</Text>
      <Text>Seuil d'humidité</Text>
      <TextInput value={threshold} onChangeText={setThreshold} keyboardType="numeric" style={{ borderWidth: 1, marginBottom: 12, padding: 8 }} />
      <View style={{ flexDirection: 'row', alignItems: 'center', marginBottom: 12 }}>
        <Text>Notifications</Text>
        <Switch value={notif} onValueChange={setNotif} style={{ marginLeft: 12 }} />
      </View>
      <Button title="Enregistrer" onPress={save} />
    </View>
  );
}