process.env.NODE_ENV = 'normal';

var gulp = require('gulp'),
    way2enjoy = require('./index'),
    cwd = __dirname,
    sigs = process.env.WAY2ENJOY_SIGS ? true : false;

gulp.task('way2enjoy', function() {
    gulp.src(cwd + '/test/assets/image.png')
        .pipe(way2enjoy({
            key: process.env.WAY2ENJOY_KEY || 'rlDAQuwa4AOtQPaekNpu-HgLOedHXOlh',
            log: true,
            sigFile: (sigs ? '.sigs' : false)
        }).on('error', function(err) {
            console.error(err.message);
        }))
        .pipe(gulp.dest(cwd + '/test/assets/tmp'));
});

process.env.NODE_ENV = 'test';
