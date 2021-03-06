import os
from flask import Flask

# application factory
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        CSVFILE=os.path.join(app.instance_path, 'report.csv'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    # call get_df from the factory
    from . import df
    with app.app_context():
        df.get_df()
        df.get_cameras_operation(df.get_df())
    
    '''
    # Import and register the blueprint auth from the factory
    from . import auth
    app.register_blueprint(auth.bp)
    '''

    # Import and register the blueprint counts from the factory
    from . import counts
    app.register_blueprint(counts.bp)
    app.add_url_rule('/', endpoint='index')
    
    return app
