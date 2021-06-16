from flask import Flask, render_template,flash,url_for,request,redirect
from wtforms import Form,StringField,validators

app = Flask(__name__)
app.secret_key = "super secret key"
import pymysql   # Open database connection
#
db = pymysql.connect("localhost", "root", "parola", "biblioteca")# prepare a cursor object using cursor() method
cursor = db.cursor()

@app.route("/")
def home():
    return render_template('dashboard.html')

@app.route("/carti")
def carti():
     sql = "select * from biblioteca;"
     r = cursor.execute(sql)
     results = cursor.fetchall()
     print(results)
     if r > 0:
         return render_template('persons.html',results = results)
     else:
         msg = "NO found"
         return render_template('persons.html',msg=msg)
     cursor.close()

@app.route("/person/<string:id>")
def person(id):
    cursor.execute("select * from biblioteca where id = %s",[id])
    result = cursor.fetchone()
    return render_template('person.html',result = result)


@app.route("/dashboard")
def dashboard():
     sql = "select * from biblioteca;"
     r = cursor.execute(sql)
     results = cursor.fetchall()
     if r > 0:
         return render_template('dashboard.html',results = results)
     else:
         msg = "NO found"
         return render_template('dashboard.html',msg=msg)
     cursor.close()


class CheForm(Form):
    autor = StringField('Autor',[validators.Length(min =1,max=200)])
    titlu = StringField('Titlu',[validators.Length(min =1,max=200)])
    gen = StringField('Gen',[validators.Length(min =1,max=200)])
    an = StringField('An', [validators.Length(min=1, max=200)])
    nume_editor = StringField('Nume editor', [validators.Length(min=1, max=200)])
    rezumat = StringField('Rezumat', [validators.Length(min=1, max=1000)])


@app.route("/add", methods = ['GET','POST'])
def add():
    form = CheForm(request.form)
    if request.method == 'POST' and form.validate():
        autor = form.autor.data
        titlu = form.titlu.data
        gen   = form.gen.data
        an    = form.an.data
        nume_editor = form.nume_editor.data
        rezumat = form.rezumat.data
        cursor = db.cursor()
        cursor.execute('insert into biblioteca (autor,titlu,gen,an,nume_editor,rezumat) values(%s,%s,%s,%s,%s,%s)',(autor,titlu,gen,an,nume_editor,rezumat))
        db.commit()
        cursor.close()
        return redirect(url_for('dashboard'))
    return render_template('add.html', form=form)


@app.route("/edit/<string:id>", methods = ['GET','POST'])
def edit(id):
    cursor = db.cursor()
    cursor.execute("select * from biblioteca where id = %s",[id])
    result = cursor.fetchone()
    form = CheForm(request.form)
    form.autor.data = result[1]
    form.titlu.data = result[2]
    form.gen.data = result[3]
    form.an.data = result[4]
    form.nume_editor.data = result[5]
    form.rezumat.data = result[6]

    if request.method == 'POST' and form.validate():
        autor = request.form['autor']
        titlu = request.form['titlu']
        gen = request.form['gen']
        an = request.form['an']
        nume_editor = request.form['nume_editor']
        rezumat = request.form['rezumat']

        cursor.execute('update biblioteca set autor=%s, titlu=%s,gen=%s,an=%s, nume_editor=%s,rezumat=%s where id=%s',(autor,titlu,gen,an,nume_editor,rezumat,id))
        db.commit()
        flash("Submited",'success')
        cursor.close()
        return redirect(url_for('dashboard'))
    return render_template('edit.html', form = form)


@app.route('/delete/<string:id>', methods = ['POST'])
def delete(id):
    cursor = db.cursor()
    cursor.execute("delete from biblioteca where id = %s",[id])
    db.commit()
    cursor.close()
    return redirect(url_for('dashboard'))


if  __name__ == '__main__':
    app.run(debug=True)