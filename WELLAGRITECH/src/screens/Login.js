import React, { useContext, useState } from 'react';
import { View, Text, TextInput, Button } from 'react-native';
import { AuthContext } from '../context/AuthContext';

export default function LoginScreen() {
  const { login } = useContext(AuthContext);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const onSubmit = async () => {
    try {
      setError('');
      await login(email, password);
    } catch (e) {
      setError('Identifiants invalides');
    }
  };

  return (
    <View style={{ padding: 16 }}>
      <Text style={{ fontSize: 24, marginBottom: 16 }}>Connexion</Text>
      {!!error && <Text style={{ color: 'red' }}>{error}</Text>}
      <TextInput value={email} onChangeText={setEmail} placeholder="Email" autoCapitalize="none" style={{ borderWidth: 1, marginBottom: 12, padding: 8 }} />
      <TextInput value={password} onChangeText={setPassword} placeholder="Mot de passe" secureTextEntry style={{ borderWidth: 1, marginBottom: 12, padding: 8 }} />
      <Button title="Se connecter" onPress={onSubmit} />
    </View>
  );
}