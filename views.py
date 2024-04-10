from flask import Flask, request, render_template
from dao.employee import get_one, get_all
import config

app = Flask(__name__)


@app.route('/')
def get_main():
    return render_template("main.html")


@app.route('/search')
def get_name_employee():
    try:
        search_id = get_one(config.db, request.args['id'])[0]
        return render_template("employee.html", id=search_id)
    except Exception as e:
        return render_template("error.html")


@app.route('/employees')
def get_all_employees():
    all_employees = get_all(config.db)
    return render_template("all_employee.html", all_employees=all_employees)


@app.route('/append_employee')
def post_employees():
    return render_template("append_employee.html")


@app.route('/directory')
def get_directory():
    return render_template("directory.html")


if __name__ == '__main__':
    app.run(debug=True, port=8080)

