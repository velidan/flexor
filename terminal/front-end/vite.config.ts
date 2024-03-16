import { defineConfig, loadEnv  } from 'vite'
import  path from 'path'
import react from '@vitejs/plugin-react-swc'
import sass from 'sass'

// https://vitejs.dev/config/
export default (({ command, mode, isSsrBuild, isPreview }) => {

  // Load env file based on `mode` in the current working directory.
  // Set the third parameter to '' to load all env regardless of the `VITE_` prefix.
  const env = loadEnv(mode, process.cwd(), '')

  const sharedConf = {
    root: path.resolve(__dirname),
    build: {
      // outDir: path.resolve(__dirname, '../static'), 
      rollupOptions: {
        input: {
          app: path.resolve(__dirname, './src/main.tsx'),
          // styles: path.resolve(__dirname, './styles/style.scss')
        },
        output: {
          entryFileNames: '[name].js',
          assetFileNames: '[name].[ext]', // currently does not work for images
          dir: path.resolve(__dirname, '../static/terminal'), 
          manualChunks: false,
          // inlineDynamicImports: true,

        }
      },
      sourcemap: true,
      cssCodeSplit: false,
    },
    define: {
      __APP_ENV__: JSON.stringify(env.APP_ENV),
    },
    resolve: {
      extensions: ['.js', '.jsx', '.ts', '.tsx', '.css', '.scss'],
      alias: {
        '@appSrc': path.resolve(__dirname, 'src/'),
        '@appComponents': path.resolve(__dirname, 'src/components/'),
        '@appCore': path.resolve(__dirname, 'src/core/'),
        '@appHocs': path.resolve(__dirname, 'src/hocs/'),
        '@appUtils': path.resolve(__dirname, 'src/utils/'),
        '@appHooks': path.resolve(__dirname, 'src/hooks/'),
      }
    },
    css: {
      preprocessorOptions: {
        scss: {
          implementation: sass,
        },
      },
    },
    plugins: [react()],
  }

  if (command === 'serve') {
    return {
      ...sharedConf,
    }
  } else {
    // command === 'build'
    return {
      ...sharedConf,
    }
  }
})
// // https://vitejs.dev/config/
// export default defineConfig({
//   plugins: [react()],
// })
