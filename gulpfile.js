var gulp    = require('gulp'),
    connect = require('connect'),
    fs      = require('fs'),
    static  = require('connect-gzip-static'),
    logger  = require('morgan'),
    concat  = require('gulp-concat'),
    gzip    = require('gulp-gzip');

var APP_PATH = "./app/static/";
var LIB_SCRIPTS_DESTINATION = APP_PATH + "dist/js/lib/";
var APP_SCRIPTS_DESTINATION = APP_PATH + "dist/js/app/";

gulp.task('serve', function() {
  var server = connect();
  server.use(logger('combined'));
  server.use(static(APP_PATH)).listen(3000);
});

var LIB_ROOT = "./bower_components/";
var APP_ROOT = APP_PATH;

var lib_paths = {
  "ang":        "angular/angular.min.js",
  "ang-bs":     "angular-bootstrap/ui-bootstrap.min.js",
  "ang-cook":   "angular-cookies/angular-cookies.min.js",
  "ang-res":    "angular-resource/angular-resource.min.js",
  "ang-route":  "angular-ui-router/release/angular-ui-router.min.js",
  "ang-util":   "angular-ui-utils/ui-utils.min.js",
  "bs":         "bootstrap/dist/js/bootstrap.min.js",
  "d3":         "d3/d3.min.js",
  "$":          "jquery/dist/jquery.min.js",
  "less":       "less.js/dist/less.min.js",
  "moment":     "moment/min/moment.min.js"
};

var app_paths = {
  "app":        "app.js",
  "root":       "partial/root/root.js"
};

// app_root = barebones stuff
var app_skel = [
  "ang",
  "ang-route",
  "ang-res",
];

var ang_app = [
  "app",
  "root"
];

var app_lib = [
  "$",
  "bs",
  "ang-cook",
  "ang-util",
  "ang-bs",
  "moment",
  "d3"
];

var lib_arr_to_paths_arr = function(scrpts, script_paths, root_path) {
  var paths, i, path;
  paths = [];
  for (i = 0; i < scrpts.length; i++) {
    path = script_paths[scrpts[i]];
    if (path === undefined) {
      throw new Error('Script ' + scrpts[i] + ' does not exist in script paths');
    } else {
      path = root_path + path;
      if ( !fs.existsSync(path) ) {
        throw new Error('Path ' + path + ' does not exist');
      } else {
        paths.push( path );
      }
    }
  }
  return paths;
};

gulp.task('concat_skel', function() {
  gulp.src(lib_arr_to_paths_arr(app_skel, lib_paths, LIB_ROOT))
    .pipe(concat( 'skel.js' ))
    .pipe(gulp.dest(LIB_SCRIPTS_DESTINATION))
    .pipe(gzip())
    .pipe(gulp.dest(LIB_SCRIPTS_DESTINATION));
});

gulp.task('concat_app', function() {
  gulp.src(lib_arr_to_paths_arr(ang_app, app_paths, APP_ROOT))
    .pipe(concat( 'app.js' ))
    .pipe(gulp.dest(APP_SCRIPTS_DESTINATION))
    .pipe(gzip())
    .pipe(gulp.dest(APP_SCRIPTS_DESTINATION));
});

gulp.task('concat_lib', function() {
  gulp.src(lib_arr_to_paths_arr(app_lib, lib_paths, LIB_ROOT))
    .pipe(concat( 'lib.js' ))
    .pipe(gulp.dest(LIB_SCRIPTS_DESTINATION))
    .pipe(gzip())
    .pipe(gulp.dest(LIB_SCRIPTS_DESTINATION));
});

gulp.task('concat_all', ['concat_skel', 'concat_app', 'concat_lib'], function() {
  gulp.start('concat_skel', 'concat_app', 'concat_lib');
});