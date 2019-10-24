from flask import render_template, Blueprint
from application.skills import bp
from wsgi import app

"""
Contains the functions necessary to 
route requests to skill articles
"""

@bp.route('/cloud')
def cloud():
    return render_template('cloud.html', title='Cloud Skills')


@bp.route('/containers')
def containers():
    return render_template('containers.html', title='Container Skills')


@bp.route('/python')
def python():
    return render_template('python.html', title='Python Skills')


@bp.route('/procedural-game')
def procedural_game():
    return render_template('procedural-game.html', title='Procedural Game')