import cherrypy


def serve(app, port=5000, config={}) -> None:
    """
    Serve Flask app with production settings
    :param app: Flask application object
    :param port: on which port to run
    :param config: additional config dictionary
    :return:
    """
    cherrypy.tree.graft(app, '/')

    # Set the configuration of the web server to production mode
    cherrypy.config.update({**{
        'environment': 'production',
        'engine.autoreload_on': False,
        'log.screen': True,
        'server.socket_port': port,
        'server.socket_host': '0.0.0.0'
    }, **config})

    # Start the CherryPy WSGI web server
    cherrypy.engine.start()
    cherrypy.engine.block()
