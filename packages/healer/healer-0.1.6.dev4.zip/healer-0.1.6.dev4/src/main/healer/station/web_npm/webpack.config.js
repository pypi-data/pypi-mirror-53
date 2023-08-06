/**
 * webpack bundle definition
 */

const path = require('path')
const webpack = require('webpack')
const clone_deep = require('lodash/cloneDeep')
const extract_plugin = require('mini-css-extract-plugin');

normal = {

	mode : 'none',

	target : 'web',

	entry : {
		bundle : [ './src/bundle.js', ],
	},

	output : {
		path : path.resolve(__dirname, 'target'),
		filename : '[name].js',
		libraryTarget : 'window',
	},

	devtool : 'source-map',

	resolve : {
		alias : {
			'vue' : 'vue/dist/vue.esm.js',
			'idle-vue' : 'idle-vue/src/index.js',
		},
	},

	module : {

		rules : [ {
			test : /\.css$/,
			use : [ extract_plugin.loader, 'css-loader' ],
		} ]

	},

	plugins : [ new extract_plugin({
		ignoreOrder : false,
		filename : '[name].css',
		chunkFilename : '[id].css',
	}), ],

	optimization : {
		minimize : false
	},

}

const optimal = clone_deep(normal);
optimal.optimization.minimize = true
optimal.output.filename = '[name].min.js';

module.exports = [ normal, ]
// module.exports = [ normal, optimal ]
