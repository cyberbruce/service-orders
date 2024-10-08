const path = require('path');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");


module.exports = {
  mode: 'development',
  entry: './app/src/js/entry.js',
  output: {
    path: path.resolve(__dirname, "app", 'dist'),
    filename: 'index.js',
  },
  plugins: [
    new MiniCssExtractPlugin()
  ],
  module: {
    
    rules: [
      {
        test: /\.css$/,
        exclude: /node_modules/,
        use: [
          {
            loader: MiniCssExtractPlugin.loader,
          },
          {
            loader: 'css-loader',
            options: {
              importLoaders: 1,
            }
          },
          {
            loader: 'postcss-loader'
          }
        ]
      }
    ]
  }
};