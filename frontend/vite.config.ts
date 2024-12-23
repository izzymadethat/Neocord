import tailwindcss from '@tailwindcss/vite';
import react from '@vitejs/plugin-react-swc';
import { defineConfig } from 'vite';

// https://vite.dev/config/
// biome-ignore lint/style/noDefaultExport: <Required for Vite>
export default defineConfig({
	plugins: [react(), tailwindcss()],
	server: {
		open: true,
		proxy: {
			'/api': 'http://127.0.0.1:8000',
		},
	},
});
