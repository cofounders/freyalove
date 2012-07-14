module.exports = function(grunt) {

	grunt.loadTasks("grunt-stylus");

	grunt.initConfig({

		pkg: '<json:package.json>',

		staging: 'intermediate',

		output: 'publish',

		exclude: '.git* build/** node_modules/** grunt-stylus grunt.js package.json *.md'.split(' '),

		clean: {
			staging: ['<config:staging>'],
			output: ['<config:output>']
		},

		mkdirs: {
			staging: '<config:exclude>'
		},

		concat: {
			dist: {
				src: [
//					'js/plugins.js',
//					'js/main.js'
				],
				dest: 'js/merged.js'
			}
		},

		stylus: {
			file: {
				src: 'styles/app.styl',
				dest: 'styles'
			}
		},

		css: {
			'styles/app.css': ['styles/app.css']
		},

		rev: {
//			js: 'js/**/*.js',
			css: 'styles/app.css',
			img: 'img/**',
			fonts: [
				'fonts/**/*.eot',
				'fonts/**/*.svg',
				'fonts/**/*.ttf',
				'fonts/**/*.woff'
			]
		},

		usemin: {
			css: ['**/*.css'],
			html: ['index.html']
		},

		html: {
			files: '<config:usemin.html>',
			type: 'basics'
		},

		img: {
			dist: '<config:rev.img>'
		},

		watch: {
			files: '<config:lint.files>',
			tasks: 'lint qunit'
		},

		meta: {
			version: '0.1.0',
			banner: '/*! <%= meta.name %> - v<%= pkg.version %> - <%= grunt.template.today("m/d/yyyy") %>\n'
				+ '* <%= pkg.homepage %>\n'
				+ '* Copyright (c) <%= grunt.template.today("yyyy") %> <%= pkg.author.name %>;'
				+ ' Licensed <%= _.pluck(pkg.licenses, "type").join(", ") %> */'
		},

		lint: {
			files: ['grunt.js', 'js/**/*.js', 'test/**/*.js']
		},

		qunit: {
			files: ['test/**/*.html']
		},

		min: {
			dist: {
				src: 'js/merged.js',
				dest: 'js/build.js'
			}
		}

	});

	grunt.registerTask('default', 'intro clean qunit mkdirs concat stylus css min rev usemin manifest html img copy');

};
