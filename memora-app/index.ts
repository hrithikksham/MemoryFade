import { registerRootComponent } from 'expo';
import App from './App';

// registerRootComponent calls AppRegistry.registerComponent('main', () => App);
// It ensures that whether you load the app in Expo Go or in a compiled native build,
// the environment is set up and bound accurately.
registerRootComponent(App);