import os

def setup(app):
    app.add_html_theme(
        'ustackdocs',
        os.path.abspath(os.path.dirname(__file__)),
    )
    return {
        'parallel_read_safe': True,
    }
