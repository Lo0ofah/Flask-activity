from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from startup_setup import Base, Startup, Founder

app = Flask(__name__)

engine = create_engine('sqlite:///startup.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/startup')
def showStartup():
    startups = session.query(Startup).all()
    return  render_template('startups.html', startups = startups)

@app.route('/startup/new', methods=['GET', 'POST'])
def newStartup():
    if request.method == 'POST':
        newStartup = Startup(name=request.form['name'])
        session.add(newStartup)
        session.commit()
        flash("new startup created!")
        return redirect(url_for('showStartup'))
    else:
        return  render_template('newStartup.html')

@app.route('/startup/<int:startup_id>/edit', methods=['GET', 'POST'])
def editStartup(startup_id):
    editedSartup = session.query(Startup).filter_by(id=startup_id).one()

    if request.method == 'POST':
        if request.form['name']:
            editedSartup.name = request.form['name']
        session.add(editedSartup)
        session.commit()
        return redirect(url_for('showStartup'))
    else:
        return  render_template('editStartup.html', startup = editedSartup)

@app.route('/startup/<int:startup_id>/delete',  methods=['GET', 'POST'])
def deleteStartup(startup_id):
    deletedstartup = session.query(Startup).filter_by(id=startup_id).one()

    if request.method == 'POST':
        session.delete(deletedstartup)
        session.commit()
        return redirect(url_for('showStartup'))
    else:
        return  render_template('deleteStartup.html', startup = deletedstartup)

@app.route('/startup/<int:startup_id>/details')
def detailsStartup(startup_id):
    startup = session.query(Startup).filter_by(id=startup_id).one()
    founders = session.query(Founder).filter_by(startup_id=startup.id)
    return  render_template('detailsStartup.html', startup = startup , founders = founders)

@app.route('/startup/<int:startup_id>/details/newFounder',  methods=['GET', 'POST'])
def newFounder(startup_id):
    startup = session.query(Startup).filter_by(id=startup_id).one()
    if request.method == 'POST':
        newFounder = Founder(name=request.form['name'],bio=request.form['bio'],startup_id = startup.id)
        session.add(newFounder)
        session.commit()
        flash("new founder created!")
        return redirect(url_for('detailsStartup',startup_id = startup_id))

    else:
        return  render_template('newFounder.html', startup = startup)

@app.route('/startup/<int:startup_id>/details/editeFounder/<int:founder_id>',  methods=['GET', 'POST'])
def editFounder(startup_id, founder_id):
    editedFounder = session.query(Founder).filter_by(id=founder_id).one()
    if request.method == 'POST':
            if request.form['name']:
                editedFounder.name = request.form['name']
            if request.form['bio']:
                editedFounder.bio = request.form['bio']
            session.add(editedFounder)
            session.commit()
            return redirect(url_for('detailsStartup',   startup_id = startup_id))
    else:
            return  render_template('editFounder.html', startup_id = startup_id, founder = editedFounder)

@app.route('/startup/<int:startup_id>/details/deleteFounder/<int:founder_id>',  methods=['GET', 'POST'])
def deleteFounder(startup_id, founder_id):
    deletedFounder = session.query(Founder).filter_by(id=founder_id).one()
    if request.method == 'POST':
            session.delete(deletedFounder)
            session.commit()
            return redirect(url_for('detailsStartup',   startup_id = startup_id))
    else:
            return  render_template('deleteFounder.html', startup_id = startup_id, founder = deletedFounder)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
