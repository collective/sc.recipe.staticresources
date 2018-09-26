const fs = require('fs');
const childProcess = require('child_process');
const ExtractTextPlugin = require('extract-text-webpack-plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const SpritesmithPlugin = require('webpack-spritesmith');


let makeConfig = (name, shortName, path, publicPath='', extraEntries=[], extraPlugins=[]) => {
  // https://github.com/alleyinteractive/webpack-git-hash/issues/10
  const gitCmd = 'git rev-list -1 HEAD -- `pwd`'
  const gitHash = childProcess.execSync(gitCmd).toString().substring(0, 7);
  childProcess.execSync(`rm -f ${path}/${shortName}-*`);

  let options = {
    entry: [
      `./app/${shortName}.scss`,
      `./app/${shortName}.js`,
    ],
    output: {
      filename: `${shortName}-${gitHash}.js`,
      library: shortName,
      libraryExport: 'default',
      libraryTarget: 'umd',
      path: path,
      pathinfo: true,
      publicPath: publicPath,
    },
    module: {
      rules: [{
        test: /\.js$/,
        exclude: /(\/node_modules\/|test\.js$|\.spec\.js$)/,
        use: 'babel-loader',
      }, {
        test: /\.scss$/,
        use: ExtractTextPlugin.extract({
          fallback: 'style-loader',
          use: [
            'css-loader',
            'postcss-loader',
            'sass-loader'
          ]
        }),
      }, {
        test: /.*\.(gif|png|jpe?g)$/i,
        use: [
          {
            loader: 'file-loader',
            options: {
              name: '[path][name].[ext]',
              context: 'app/',
            }
          },
          {
            loader: 'image-webpack-loader',
            query: {
              mozjpeg: {
                progressive: true,
              },
              pngquant: {
                quality: '65-90',
                speed: 4,
              },
              gifsicle: {
                interlaced: false,
              },
              optipng: {
                optimizationLevel: 7,
              }
            }
          }
        ]
      }, {
        test: /\.svg/,
        exclude: /node_modules/,
        use: 'svg-url-loader',
      }]
    },
    plugins: [
      new ExtractTextPlugin({
        filename: `${shortName}-${gitHash}.css`,
        allChunks: true
      }),
      new SpritesmithPlugin({
        src: {
          cwd: 'app/sprite',
          glob: '*.png',
        },
        target: {
          image: 'app/img/sprite.png',
          css: 'app/scss/_sprite.scss',
        },
        apiOptions: {
          cssImageRef: './img/sprite.png',
        }
      }),
    ]
  };
  for (let entry of extraEntries) {
    options.entry.unshift(entry);
  }
  if (process.env.NODE_ENV === 'debug') {
    options.devtool = 'source-map';
  }
  if (fs.existsSync('app/index.html')) {
    options.plugins.push(
      new HtmlWebpackPlugin({
        filename: 'index.html',
        template: 'app/index.html',
      })
    );
  }
  if (fs.existsSync('app/resources.pt')) {
    options.plugins.push(
      new HtmlWebpackPlugin({
        inject: false,
        filename: 'resources.pt',
        template: 'app/resources.pt',
      })
    );
  }
  for (let plugin of extraPlugins) {
    options.plugins.push(plugin);
  }
  return options;
}

module.exports = makeConfig;
