
from flask import Flask, jsonify, render_template, request, json
from flaskext.mysql import MySQL

app = Flask(__name__,template_folder='template')

# MySQL configurations
mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Darshika@28'
app.config['MYSQL_DATABASE_DB'] = 'sampledb'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

conn = mysql.connect()



@app.route('/')
def main():
    return render_template('index.html')

@app.route('/billApp',methods=['POST'])
def billApp():
 
    # read the posted values from the UI
    _prodName = request.form['prodName']
    _quantity = request.form['quantity']
    _price = request.form['price']

    if _prodName and _quantity and _price:
        
        cursor = conn.cursor()
        cursor.callproc('sp_createBill',(_prodName,_quantity,_price))    
        data = cursor.fetchall()

        if len(data) is 0:
            conn.commit()
            return json.dumps({'message':'Bill created successfully !'})
        else:
            return json.dumps({'error':str(data[0])})
            return json.dumps({'html':'<span>All fields good !!</span>'})
    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'})
    
    

if __name__ == "__main__":
    app.run(debug=True)
