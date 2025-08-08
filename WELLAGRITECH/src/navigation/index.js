import React, { useContext } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { AuthContext } from '../context/AuthContext';
import Login from '../screens/Login';
import Dashboard from '../screens/Dashboard';
import History from '../screens/History';
import Settings from '../screens/Settings';

const Stack = createNativeStackNavigator();

export default function RootNavigation() {
  const { user } = useContext(AuthContext);
  return (
    <NavigationContainer>
      <Stack.Navigator>
        {user ? (
          <>
            <Stack.Screen name="Dashboard" component={Dashboard} />
            <Stack.Screen name="History" component={History} />
            <Stack.Screen name="Settings" component={Settings} />
          </>
        ) : (
          <Stack.Screen name="Login" component={Login} />
        )}
      </Stack.Navigator>
    </NavigationContainer>
  );
}