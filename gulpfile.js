var gulp    = require('gulp'),
    connect = require('connect'),
    fs      = require('fs'),
    static  = require('connect-gzip-static'),
    logger  = require('morgan'),
    concat  = require('gulp-concat'),
    uglify  = require('gulp-uglify'),
    gzip    = require('gulp-gzip'),
    argv    = require('yargs').argv,
    gulpif  = require('gulp-if');

var APP_PATH = "./app/static/";
var LIB_SCRIPTS_DESTINATION = APP_PATH + "dist/js/lib/";
var APP_SCRIPTS_DESTINATION = APP_PATH + "dist/js/app/";
var AMD_SCRIPTS_DESTINATION = APP_PATH + "dist/js/amd/";

gulp.task('serve', function() {
  var server = connect();
  server.use(logger('combined'));
  server.use(static(APP_PATH)).listen(3000);
});

var LIB_ROOT = "./bower_components/";
var APP_ROOT = APP_PATH;

var lib_paths = {
  "ang":        "angular/angular.min.js",
  "require":    "requirejs/require.js",
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
  "app":            "app.js",
  "api":            "service/api.js",
  "model":          "service/model.js",
  "root":           "partial/root/root.js",
  "home":           "partial/home/home.js",
  "dash":           "partial/dash/dash.js",
  "sidebar":        "partial/sidebar/sidebar.js",
  "user":           "user/user.js",
  "settings":       "user/partial/settings/settings.js",
  "user-panel":     "user/partial/user-panel/user-panel.js",
  "userService":    "user/service/userService.js",
  "dataset":        "dataset/dataset.js",
  "dataService":    "dataset/service/dataService.js",
  "dataset-base":   "dataset/partial/base/base.js",
  "dataset-list":   "dataset/partial/list/list.js",
  "dataset-detail": "dataset/partial/detail/detail.js",
  "form-user-new":  "user/partial/form/user-new.js"
};

// app_root = barebones stuff
var app_skel = [
  "ang",
  "ang-route",
  "ang-res"
];

var app_ang = [
  "app",
  "api",
  "model",
  "root",
  "home",
  "dash",
  "user",
  "dataset",
  "settings",
  "user-panel",
  "sidebar",
  "userService",
  "dataService",
  "dataset-base",
  "dataset-list",
  "dataset-detail",
  "form-user-new"
];

var app_lib = [
  "$",
  "bs",
  "d3",
  "ang-cook",
  "ang-util",
  "ang-bs",
  "moment"
];

/*var app_amd = [
  "d3"
];*/

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

var prod = argv.prod !== undefined;

gulp.task('concat_skel', function() {
  gulp.src(lib_arr_to_paths_arr(app_skel, lib_paths, LIB_ROOT))
    .pipe(concat( 'skel.js' ))
    .pipe( gulpif( prod, uglify() ))
    .pipe(gulp.dest(LIB_SCRIPTS_DESTINATION))
    .pipe( gulpif( prod, gzip() ))
    .pipe( gulpif( prod, gulp.dest(LIB_SCRIPTS_DESTINATION) ));
});

gulp.task('concat_app', function() {
  gulp.src(lib_arr_to_paths_arr(app_ang, app_paths, APP_ROOT))
    .pipe(concat( 'app.js' ))
    .pipe( gulpif( prod, uglify() ))
    .pipe( gulp.dest(APP_SCRIPTS_DESTINATION) )
    .pipe( gulpif( prod, gzip() ))
    .pipe( gulpif( prod, gulp.dest(APP_SCRIPTS_DESTINATION) ));
});

gulp.task('concat_lib', function() {
  gulp.src(lib_arr_to_paths_arr(app_lib, lib_paths, LIB_ROOT))
    .pipe( concat( 'lib.js' ) )
    .pipe( gulpif( prod, uglify() ) )
    .pipe( gulp.dest(LIB_SCRIPTS_DESTINATION) )
    .pipe( gulpif( prod, gzip() ))
    .pipe( gulpif( prod, gulp.dest(LIB_SCRIPTS_DESTINATION) ));
});

/*gulp.task('set_amd', function() {
  gulp.src(lib_arr_to_paths_arr(app_amd, lib_paths, LIB_ROOT))
    .pipe( gulpif( prod, uglify() ))
    .pipe( gulp.dest(AMD_SCRIPTS_DESTINATION) )
    .pipe( gulpif( prod, gzip() ))
    .pipe( gulpif( prod, gulp.dest(AMD_SCRIPTS_DESTINATION) ));
});*/

gulp.task('watch', ['all'], function() {
  gulp.watch("./app/static/**/*.js", ["all"]);
});

gulp.task('all', ['concat_skel', 'concat_app', 'concat_lib'], function() {
  gulp.start('concat_skel', 'concat_app', 'concat_lib');
});