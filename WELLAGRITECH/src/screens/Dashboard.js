import React, { useEffect, useState } from 'react';
import { View, Text, Button } from 'react-native';
import { getDevices, getLatest, sendDeviceCommand } from '../services/api';

export default function Dashboard() {
  const [device, setDevice] = useState(null);
  const [latest, setLatest] = useState(null);

  useEffect(() => {
    (async () => {
      const { data } = await getDevices();
      if (data.length) {
        setDevice(data[0]);
        const latestRes = await getLatest(data[0].device_id);
        setLatest(latestRes.data);
      }
    })();
  }, []);

  const togglePump = async () => {
    if (!device || !latest) return;
    const cmd = latest.etat_pompe ? 'pump_off' : 'pump_on';
    await sendDeviceCommand(device.id, cmd);
  };

  return (
    <View style={{ padding: 16 }}>
      <Text style={{ fontSize: 22, marginBottom: 12 }}>Dashboard</Text>
      {device ? (
        <>
          <Text>Appareil: {device.device_id}</Text>
          <Text>Humidité: {latest?.humidite_sol ?? '-'}</Text>
          <Text>Niveau eau: {latest?.niveau_eau ?? '-'}</Text>
          <Text>Intrusion: {latest?.intrusion ? 'Oui' : 'Non'}</Text>
          <Text>Pompe: {latest?.etat_pompe ? 'ON' : 'OFF'}</Text>
          <Button title={latest?.etat_pompe ? 'Arrêter la pompe' : 'Démarrer la pompe'} onPress={togglePump} />
        </>
      ) : (
        <Text>Aucun appareil</Text>
      )}
    </View>
  );
}