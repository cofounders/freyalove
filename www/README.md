# FreyaLove

> The match making site for lesbians.

## Deployment Instructions

1. Install [Node.js/NPM](http://nodejs.org/)
1. Set up the dependencies: `npm install -g grunt stylus https://github.com/h5bp/node-build-script/tarball/master`
1. Run `h5bp`
1. Set up Nginx to serve `./publish` and allow client-side route handling.

        server {
          listen 80;
          server_name www.freyalove.com;
          root /var/www/freyalove.com/www/publish;
          index index.html;
          # Let the Backbone.js router handle internal app paths
          location ~ ^/(css|fonts|img|js|templates)/ {}
          location / { try_files $uri $uri/ /index.html; }
        }

## Development Guidelines

- Don't forget to compile `./css/app.styl` with Stylus. Tip: Use Sublime Text 2 with the Stylus build plugin.
- Learn these frameworks:
  - [RequireJS](http://requirejs.org/)
  - [Underscore.js](http://underscorejs.org/)
  - [Backbone.js](http://backbonejs.org/) with [Backbone.LayoutManager](https://github.com/tbranyen/backbone.layoutmanager)
