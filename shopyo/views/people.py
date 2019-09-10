from flask import (
    Blueprint, render_template, request, redirect
)
from datetime import date
from addon import db
from models import People

from settings import get_value
import datetime

people_blueprint = Blueprint('people', __name__, url_prefix='/people')


@people_blueprint.route("/")
def people_main():
    return render_template('people/index.html', peoples=People.query.all(),
                           OUR_APP_NAME=get_value('OUR_APP_NAME'), SECTION_NAME=get_value('SECTION_NAME'))


@people_blueprint.route('/add', methods=['GET', 'POST'])
def people_add():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        mobile = request.form['mobile']
        email = request.form['email']
        linkedin = request.form['linkedin']
        facebook = request.form['facebook']
        twitter = request.form['twitter']
        birthday = request.form['birthday']
        notes = request.form['notes']
        # calculate age
        today_date = date.today()
        date_format = "%Y-%m-%d"
        b_day = datetime.datetime.strptime(birthday, date_format)
        age = today_date.year - b_day.year - ((today_date.month, today_date.day) < (b_day.month, b_day.day))

        # insert data into DB
        person = People(name=name, phone=phone, mobile=mobile, email=email,
                    linkedin=linkedin, facebook=facebook, twitter=twitter,
                    age=age, birthday=birthday, notes=notes)
        db.session.add(person)
        db.session.commit()
        return redirect('/people/add')
    return render_template('people/add.html', OUR_APP_NAME=get_value('OUR_APP_NAME'), message='')


@people_blueprint.route('/delete/<id>', methods=['GET', 'POST'])
def people_delete(id):
    People.query.filter(People.id == id).delete()
    db.session.commit()
    return redirect('/people')


@people_blueprint.route('/edit/<id>', methods=['GET', 'POST'])
def people_edit(id):
    a = People.query.get(id)
    return render_template('people/edit.html',
                            id=a.id,
                            name=a.name, phone=a.phone,
                            mobile=a.mobile, email=a.email,
                            linkedin=a.linkedin, facebook=a.facebook,
                            twitter=a.twitter, age=a.age,
                            birthday=a.birthday, notes=a.notes,
                            OUR_APP_NAME=get_value('OUR_APP_NAME'),
                            SECTION_ITEMS=get_value('SECTION_ITEMS'))


@people_blueprint.route('/update', methods=['GET', 'POST'])
def people_update():
    if request.method =='POST':
            people_id = request.form['id']
            people_name = request.form['name']
            people_phone = request.form['phone']
            people_mobile = request.form['mobile']
            people_email = request.form['email']
            people_linkedin = request.form['linkedin']
            people_facebook = request.form['facebook']
            people_twitter = request.form['twitter']
            people_birthday = request.form['birthday']
            people_notes = request.form['notes']

            # calculate age
            today_date = datetime.datetime.now()
            time_format = "%Y-%m-%d"
            b_day = datetime.datetime.strptime(people_birthday, time_format)
            people_age = str(today_date - b_day)
            # retrive record from db with id
            s = People.query.get(people_id)
            s.name = people_name
            s.phone = people_phone
            s.mobile = people_mobile
            s.email = people_email
            s.linkedin = people_linkedin
            s.twitter = people_twitter
            s.birthday = people_birthday
            s.notes= people_notes
            s.age = people_age

            db.session.commit()

            return redirect('/people')
