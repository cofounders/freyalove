# FreyaLove

> The match making site for lesbians.

## Deployment Instructions

1. Install [Node.js/NPM](http://nodejs.org/)
1. Set up the dependencies: `npm install -g grunt stylus https://github.com/h5bp/node-build-script/tarball/master`
1. Run `h5bp`
1. For local develpoment, add the following entries to `/etc/hosts` (Mac: `/private/etc/hosts` Win: `%SYSTEMROOT%\system32\drivers\etc\hosts`)

        127.0.0.1     freyalove.localhost
        127.0.0.1     dev.freyalove.localhost

1. **Nginx** Set up Nginx to serve `./publish` and allow client-side route handling.

        server {
          listen 80;
          server_name dev.freyalove.localhost;
          root /var/www/freyalove.com/www;
          index index.html;
          # Proxy API calls to avoid CORS restriction
          location /api {
            rewrite ^/api/(.*) /$1 break;
            proxy_pass http://api.freyalove.cofounders.sg;
          }
          # Let the Backbone.js router handle internal app paths
          location ~ ^/(css|fonts|img|js|templates)/ {}
          location / { try_files $uri $uri/ /index.html; }
        }

        server {
          listen 80;
          server_name freyalove.localhost;
          root /var/www/freyalove.com/www/publish;
          index index.html;
          # Proxy API calls to avoid CORS restriction
          location /api {
            rewrite ^/api/(.*) /$1 break;
            proxy_pass http://api.freyalove.cofounders.sg;
          }
          # Let the Backbone.js router handle internal app paths
          location ~ ^/(css|fonts|img|js|templates)/ {}
          location / { try_files $uri $uri/ /index.html; }
        }

  **Apache** Update your http.conf to enable vhosts and update httpd-vhosts.config file and use this template (but change the paths). *TODO: Needs update to support `/api` redirect.*

        <VirtualHost *:80>
          ServerName freyalove.localhost
          DocumentRoot "/Users/username/Sites/freyalove/www/publish"
          <Directory /Users/username/Sites/freyalove/www/publish>
            AllowOverride All
            Order allow,deny
            Allow from all
          </Directory>
        </VirtualHost>

        <VirtualHost *:80>
          ServerName dev.freyalove.localhost
          DocumentRoot "/Users/username/Sites/freyalove/www"
          <Directory /Users/username/Sites/freyalove/www>
            AllowOverride All
            Order allow,deny
            Allow from all
          </Directory>
        </VirtualHost>

1. Run `h5bp`
1. Open http://freyalove.localhost/ or http://dev.freyalove.localhost/

## Development Guidelines

- After any modificatoions to the `*.styl` files, or after a `git pull`, remember to compile the Stylus files.

        stylus --watch ./styles/app.styl ./styles/app.styl

- Learn these frameworks:
  - [RequireJS](http://requirejs.org/)
  - [Underscore.js](http://underscorejs.org/)
  - [Backbone.js](http://backbonejs.org/) with [Backbone.LayoutManager](https://github.com/tbranyen/backbone.layoutmanager)
