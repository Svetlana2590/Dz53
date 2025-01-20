   from flask import Blueprint, render_template

   db_blueprint = Blueprint('db_blueprint', __name__, template_folder='templates')

   @db_blueprint.route('/db-route')
   def db_function():
       return render_template('db_template.html')
