import React, {useCallback, useEffect, useMemo, useRef, useState} from 'react';
import {
	SafeAreaView,
	StyleSheet,
	Text,
	View,
	Button,
	PermissionsAndroid,
	Platform,
	ScrollView
} from 'react-native';
import Slider from '@react-native-community/slider';
// @ts-ignore types may be partial depending on library version
import RNBluetoothClassic, {
	BluetoothDevice
} from 'react-native-bluetooth-classic';

const PREFERRED_NAMES = ['HC-05', 'HC-06', 'BT-CAR'];

export default function App() {
	const [isConnecting, setIsConnecting] = useState(false);
	const [isConnected, setIsConnected] = useState(false);
	const [status, setStatus] = useState('Disconnected');
	const [speed, setSpeed] = useState(150);
	const deviceRef = useRef<BluetoothDevice | null>(null);

	const requestPermissions = useCallback(async () => {
		if (Platform.OS !== 'android') return true;
		const toRequest: string[] = [];
		// Android 12+
		if (Platform.Version >= 31) {
			const perms = [
				PermissionsAndroid.PERMISSIONS.BLUETOOTH_SCAN,
				PermissionsAndroid.PERMISSIONS.BLUETOOTH_CONNECT,
			];
			for (const p of perms) {
				const has = await PermissionsAndroid.check(p);
				if (!has) toRequest.push(p);
			}
		} else {
			const perms = [
				PermissionsAndroid.PERMISSIONS.ACCESS_FINE_LOCATION,
				PermissionsAndroid.PERMISSIONS.ACCESS_COARSE_LOCATION,
			];
			for (const p of perms) {
				const has = await PermissionsAndroid.check(p);
				if (!has) toRequest.push(p);
			}
		}
		if (toRequest.length === 0) return true;
		const res = await PermissionsAndroid.requestMultiple(toRequest);
		return Object.values(res).every(v => v === PermissionsAndroid.RESULTS.GRANTED);
	}, []);

	const findBondedTarget = useCallback(async () => {
		const bonded: BluetoothDevice[] = await RNBluetoothClassic.getBondedDevices();
		return bonded.find(d => d.name && PREFERRED_NAMES.includes(d.name));
	}, []);

	const connect = useCallback(async () => {
		try {
			const ok = await requestPermissions();
			if (!ok) {
				setStatus('Missing permissions');
				return;
			}
			setIsConnecting(true);
			setStatus('Connecting...');
			const target = await findBondedTarget();
			if (!target) {
				setStatus('Pair HC-05/HC-06 in system settings first');
				setIsConnecting(false);
				return;
			}
			// Close any existing
			try { await deviceRef.current?.disconnect(); } catch {}
			const connected = await RNBluetoothClassic.connectToDevice(target.address, {
				// SPP UUID default handled by the module
				// insecure: false
			});
			deviceRef.current = connected;
			setIsConnected(true);
			setIsConnecting(false);
			setStatus(`Connected to ${connected.name ?? connected.address}`);
			// Push base speed
			sendCommand(`V${speed}\n`);
		} catch (e: any) {
			setIsConnecting(false);
			setIsConnected(false);
			setStatus(`Connect failed: ${e?.message ?? String(e)}`);
			try { await deviceRef.current?.disconnect(); } catch {}
			deviceRef.current = null;
		}
	}, [findBondedTarget, requestPermissions, speed]);

	const disconnect = useCallback(async () => {
		try {
			await deviceRef.current?.disconnect();
		} catch {}
		deviceRef.current = null;
		setIsConnected(false);
		setStatus('Disconnected');
	}, []);

	const connectOrDisconnect = useCallback(() => {
		if (isConnected) disconnect();
		else connect();
	}, [isConnected, connect, disconnect]);

	const sendCommand = useCallback(async (cmd: string) => {
		const dev = deviceRef.current;
		if (!dev) return;
		try {
			await dev.write(cmd);
		} catch (e: any) {
			setStatus(`Send failed: ${e?.message ?? String(e)}`);
		}
	}, []);

	const sendMove = useCallback((prefix: string, s: number) => {
		const v = Math.max(0, Math.min(255, Math.round(s)));
		sendCommand(`${prefix}${v}\n`);
	}, [sendCommand]);

	useEffect(() => {
		return () => {
			// cleanup
			deviceRef.current?.disconnect().catch(() => {});
		};
	}, []);

	return (
		<SafeAreaView style={styles.container}>
			<ScrollView contentContainerStyle={styles.inner}>
				<Text style={styles.title}>Robot Car (Bluetooth Classic)</Text>
				<Text style={styles.status}>{status}</Text>
				<View style={styles.row}>
					<Button
						title={isConnected ? 'Disconnect' : (isConnecting ? 'Connecting...' : 'Connect')}
						onPress={connectOrDisconnect}
						disabled={isConnecting}
					/>
				</View>

				<View style={styles.section}>
					<Text style={styles.label}>Speed: {speed}</Text>
					<Slider
						value={speed}
						minimumValue={0}
						maximumValue={255}
						step={1}
						onValueChange={(v) => setSpeed(v)}
						onSlidingComplete={(v) => sendCommand(`V${Math.round(v)}\n`)}
					/>
				</View>

				<View style={styles.controls}>
					<View style={styles.row}>
						<Button title="Forward" onPress={() => sendMove('F', speed)} />
					</View>
					<View style={styles.row}>
						<Button title="Left" onPress={() => sendMove('L', speed)} />
						<View style={{width: 24}} />
						<Button title="Stop" onPress={() => sendCommand('S\n')} />
						<View style={{width: 24}} />
						<Button title="Right" onPress={() => sendMove('R', speed)} />
					</View>
					<View style={styles.row}>
						<Button title="Backward" onPress={() => sendMove('B', speed)} />
					</View>
				</View>
			</ScrollView>
		</SafeAreaView>
	);
}

const styles = StyleSheet.create({
	container: { flex: 1, backgroundColor: '#0f172a' },
	inner: { padding: 16 },
	title: { color: 'white', fontSize: 20, fontWeight: '600', marginBottom: 8 },
	status: { color: '#a3e635', marginBottom: 12 },
	row: { flexDirection: 'row', alignItems: 'center', justifyContent: 'center', marginVertical: 8 },
	section: { backgroundColor: '#111827', padding: 12, borderRadius: 8, marginVertical: 8 },
	label: { color: '#e5e7eb', marginBottom: 8 },
	controls: { backgroundColor: '#111827', padding: 12, borderRadius: 8, marginTop: 8 }
});


