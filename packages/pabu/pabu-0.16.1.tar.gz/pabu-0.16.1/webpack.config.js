var LiveReloadPlugin = require('webpack-livereload-plugin');

module.exports = {
    entry: "./pabu/assets/ts/index.tsx",
    output: {
        filename: "bundle.js",
        path: __dirname + "/pabu/static",
        libraryTarget: 'umd',
    },

    // Enable sourcemaps for debugging webpack's output.
    devtool: "source-map",

    resolve: {
        // Add '.ts' and '.tsx' as resolvable extensions.
        extensions: [".ts", ".tsx", ".js"]
    },

    mode: 'development',

    module: {
        rules: [
            {
                test: /\.ts(x?)$/,
                exclude: /node_modules/,
                use: [
                    {
                        loader: "ts-loader"
                    }
                ]
            },
            // All output '.js' files will have any sourcemaps re-processed by 'source-map-loader'.
            {
                enforce: "pre",
                test: /\.js$/,
                loader: "source-map-loader"
            },
        ],
    },
    externals: [
        {
            "react": "React",
            "react-dom": "ReactDOM",
            "@material-ui/core": "MaterialUI",
            "react-beautiful-dnd": "ReactBeautifulDnd",
            "@fortawesome/fontawesome-svg-core": "fontawesome-svg-core",
            "@fortawesome/free-solid-svg-icons": "free-solid-svg-icons",
            "@fortawesome/free-brands-svg-icons": "free-brands-svg-icons",
            "@fortawesome/free-regular-svg-icons": "free-regular-svg-icons",
        },
    ],

    plugins: [
        new LiveReloadPlugin({})
    ]
};
