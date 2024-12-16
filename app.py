from flask import Flask, render_template
from integrales_3x3 import integrales_3x3_bp
from integrales_2x2 import integrales_2x2_bp
from derivadas_parciales import derivadas_parciales_bp

app = Flask(__name__)

app.register_blueprint(integrales_3x3_bp, url_prefix='/')
app.register_blueprint(integrales_2x2_bp, url_prefix='/integrales_2x2')
app.register_blueprint(derivadas_parciales_bp, url_prefix='/derivadas_parciales')

@app.route('/documentacion')
def documentacion():
    return render_template('documentacion.html')

@app.route('/formulario')
def formulario():
    return render_template('formulario.html')

if __name__ == '__main__':
    app.run(debug=True)