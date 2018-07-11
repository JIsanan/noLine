var gulp = require('gulp');
var sass = require('gulp-sass');
var plumber = require('gulp-plumber');

gulp.task('buildsass', function(){
	return gulp.src('sass/styles.scss')
    	.pipe(sass()) // Converts Sass to CSS with gulp-sass
    	.pipe(plumber())
    	.pipe(gulp.dest('./css/'))
});

//Watch task
gulp.task('default',function() {
    gulp.watch('sass/**/*.scss',['buildsass']);
});