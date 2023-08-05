
from os.path import join

from cbsettings import DjangoDefaults


class BaseStaticFilesSettings(object):

    BOWER_INSTALLED_APPS = ()
    STYLESHEETS = ()
    JAVASCRIPT = ()

    IS_LESS_ENABLED = False

    STATICFILES_STORAGE = 'pipeline.storage.PipelineStorage'

    STATICFILES_FINDERS = DjangoDefaults.STATICFILES_FINDERS + [
        'pipeline.finders.PipelineFinder',
        'djangobower.finders.BowerFinder'
    ]

    STATIC_URL = '/static/'

    @property
    def PIPELINE(self):
        return {
            'JS_COMPRESSOR': 'pipeline.compressors.jsmin.JSMinCompressor',
            'CSS_COMPRESSOR': 'pipeline.compressors.cssmin.CSSMinCompressor',
            'COMPILERS': self.COMPILERS,
            'STYLESHEETS': {
                'generic': {
                    'source_filenames': self.STYLESHEETS,
                    'output_filename': 'cache/generic.css',
                }
            },
            'JAVASCRIPT': {
                'generic': {
                    'source_filenames': self.JAVASCRIPT,
                    'output_filename': 'cache/generic.js'
                }
            }
        }

    @property
    def STATIC_ROOT(self):
        return join(self.BASE_DIR, 'static-collect')

    @property
    def BOWER_COMPONENTS_ROOT(self):
        return join(self.BASE_DIR, 'static')

    @property
    def STATICFILES_DIRS(self):
        return [
            join(self.BASE_DIR, 'static'),
            join(self.BASE_DIR, 'static', 'bower_components')
        ]

    @property
    def COMPILERS(self):
        if self.IS_LESS_ENABLED:
            return ['pipeline.compilers.less.LessCompiler']
        return []

    @property
    def INSTALLED_APPS(self):
        return super().INSTALLED_APPS + [
            'django.contrib.staticfiles',
            'pipeline',
            'djangobower'
        ]

    @property
    def MIDDLEWARE(self):
        return super().MIDDLEWARE + [
            'pipeline.middleware.MinifyHTMLMiddleware'
        ]
