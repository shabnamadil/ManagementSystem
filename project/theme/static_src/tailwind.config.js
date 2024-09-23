/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
    content: [
        // Templates within theme app (e.g. base.html)
        '../templates/**/*.html',
        // Templates in other apps
        '../../templates/**/*.html',
        // Ignore files in node_modules
        '!../../**/node_modules',
        // Include JavaScript files that might contain Tailwind CSS classes
        '../../**/*.js',
        // Include Python files that might contain Tailwind CSS classes
        '../../**/*.py'
    ],
    theme: {
        extend: {
            fontFamily: {
                sans: ['Work Sans', 'sans-serif'], // Burada Work Sans fontunu tanımlıyoruz
              },
            colors: {
              primary: '#31FFAA', 
              'primary-hover': '#28D79E', 
              secondary: '#FEE86E', 
              'secondary-hover': '#28D79E', 
            },
            maxWidth: {
                'custom': '1595px', // Özel genişlik
            },
            animation: {
                marquee: 'marquee 15s linear infinite',
                marquee2: 'marquee2 15s linear infinite',
                'spin-slow': 'spin 3s linear infinite', // 3 saniyede bir döner
                'spin-fast': 'spin 0.5s linear infinite', // 0.5 saniyede bir döner
              },
            keyframes: {
              marquee: {
                '0%': { transform: 'translateX(0%)' },
                '100%': { transform: 'translateX(-100%)' },
              },
              marquee2: {
                '0%': { transform: 'translateX(100%)' },
                '100%': { transform: 'translateX(0%)' },
              },
              
            },
            boxShadow: {
              custom: '8.11px 14.61px 32.46px 4.87px rgba(19, 21, 23, 0.1)',
            },
        },
    },
    plugins: [
        /**
         * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
         * for forms. If you don't like it or have own styling for forms,
         * comment the line below to disable '@tailwindcss/forms'.
         */
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
    ],
}
