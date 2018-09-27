const fs = require('fs');
const childProcess = require('child_process');
const ExtractTextPlugin = require('extract-text-webpack-plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const SpritesmithPlugin = require('webpack-spritesmith');


/**
 * Create a initial configuration for webpack
 *
 * @function makeConfig
 * @param  {string} name           The package name
 * @param  {string} shortName      The package short name
 * @param  {string} path           The path where the static files are generated
 * @param  {string} publicPath     The prefix that should be added in the beggining of the emmited files
 * @param  {string[]} extraEntries List of extra items to be inserted before default entries
 * @param  {Plugin[]} extraPlugins List of extra plugins to be inserted after default plugins
 * @return {Object}                Webpack configuration object
 */
let makeConfig = (name, shortName, path, publicPath='', extraEntries=[], extraPlugins=[]) => {
  // Get git hash to add in the end of files
  // https://github.com/alleyinteractive/webpack-git-hash/issues/10
  const gitCmd = 'git rev-list -1 HEAD -- `pwd`'
  const gitHash = childProcess.execSync(gitCmd).toString().substring(0, 7);

  // Remove old static resources
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
        // Handle JS files
        test: /\.js$/,
        exclude: /(\/node_modules\/|test\.js$|\.spec\.js$)/,
        use: 'babel-loader',
      }, {
        // Handle SCSS files
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
        // Handle image optimization
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
        // Handle SVG files inline in CSS
        test: /\.svg/,
        exclude: /node_modules/,
        use: 'svg-url-loader',
      }]
    },
    plugins: [
      // Default CSS generation configuration
      new ExtractTextPlugin({
        filename: `${shortName}-${gitHash}.css`,
        allChunks: true
      }),
      // Default Spritesmith configuration
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
  // Add extra entries
  for (let entry of extraEntries) {
    options.entry.unshift(entry);
  }
  // Create source maps if in debug mode
  if (process.env.NODE_ENV === 'debug') {
    options.devtool = 'source-map';
  }
  // Create index file (used for theme creation)
  if (fs.existsSync('app/index.html')) {
    options.plugins.push(
      new HtmlWebpackPlugin({
        filename: 'index.html',
        template: 'app/index.html',
      })
    );
  }
  // Create resources file (used for addon creation)
  if (fs.existsSync('app/resources.pt')) {
    options.plugins.push(
      new HtmlWebpackPlugin({
        inject: false,
        filename: 'resources.pt',
        template: 'app/resources.pt',
      })
    );
  }
  // Add extra plugins
  for (let plugin of extraPlugins) {
    options.plugins.push(plugin);
  }
  return options;
}

module.exports = makeConfig;
