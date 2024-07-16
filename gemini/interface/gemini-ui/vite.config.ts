import {vitePlugin as remix} from '@remix-run/dev';
import {defineConfig} from 'vite';
import path from 'path';

export default defineConfig({
  plugins: [remix()],
  resolve: {
    alias: {
      // This alias allows you to import modules from the root of the project
      app: path.resolve(__dirname, './app'),
      api: path.resolve(__dirname, './api'),
    },
  },
});
 