const fs = require('fs');
const childProcess = require('child_process');
const ExtractTextPlugin = require('extract-text-webpack-plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const SpritesmithPlugin = require('webpack-spritesmith');


/**
 * This callback type is called `tuneConfigCallback` and is displayed as a global symbol.
 *
 * @callback tuneConfigCallback
 * @param {Object} config  The webpack configuration
 * @param {Object} options Global options used in this function
 */

/**
 * Create a initial configuration for webpack
 *
 * @function makeConfig
 * @param  {string}             name       The package name
 * @param  {string}             shortName  The package short name
 * @param  {string}             path       The path where the static files are generated
 * @param  {string}             publicPath The prefix that should be added in the beggining of the emmited files
 * @param  {tuneConfigCallback} callback   Callback used to finetune options
 * @return {Object}                        Webpack configuration object
 */
let makeConfig = (name, shortName, path, publicPath, cb=null) => {
  // Get git hash to add in the end of files
  // https://github.com/alleyinteractive/webpack-git-hash/issues/10
  const gitCmd = 'git rev-list -1 HEAD -- `pwd`';

  let options = {};
  options.name = name;
  options.shortName = shortName;
  options.path = path;
  options.publicPath = publicPath;
  options.gitHash = childProcess.execSync(gitCmd).toString().substring(0, 7);

  // Remove old static resources
  childProcess.execSync(`rm -f ${options.path}/${options.shortName}-*`);

  let config = {
    entry: [
      `./app/${options.shortName}.js`,
    ],
    output: {
      filename: `${options.shortName}-${options.gitHash}.js`,
      library: options.shortName,
      libraryExport: 'default',
      libraryTarget: 'var',
      path: options.path,
      publicPath: options.publicPath,
    },
    externals: {
      jquery: 'jQuery',
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
        test: /\.(gif|png|jpe?g)$/i,
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
        test: /\.(eot|svg|ttf|woff2?)$/,  
        use: {    
          loader: 'file-loader',  
          options: {  
            name: '[path][name].[ext]',   
            context: 'app/'   
          }   
        } 
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
        filename: `${options.shortName}-${options.gitHash}.css`,
        allChunks: true
      }),
    ]
  };
  // Add SCSS file if exists
  let scss = `./app/${options.shortName}.scss`;
  if (fs.existsSync(scss)) {
    config.entry.unshift(scss);
  }
  // Create source maps if in debug mode
  if (process.env.NODE_ENV === 'debug') {
    config.devtool = 'source-map';
  }
  // Create index file (used for theme creation)
  if (fs.existsSync('app/index.html')) {
    config.plugins.push(
      new HtmlWebpackPlugin({
        filename: 'index.html',
        template: 'app/index.html',
        publicPath: options.publicPath,
      })
    );
  }
  // Create resources file (used for addon creation)
  if (fs.existsSync('app/resources.pt')) {
    config.plugins.push(
      new HtmlWebpackPlugin({
        inject: false,
        filename: 'resources.pt',
        template: 'app/resources.pt',
        publicPath: options.publicPath,
      })
    );
  }
  // Add spritesmith configuration
  if (fs.existsSync('./app/sprite')) {
    config.plugins.push(
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
    );
  }
  if (typeof(callback) === 'function') {
    callback(config, options);
  }
  return config;
};


module.exports = makeConfig;
