from flask import Blueprint, request, render_template
import sympy as sp

derivadas_parciales_bp = Blueprint('derivadas_parciales', __name__)

@derivadas_parciales_bp.route('/')
def derivadas_parciales():
    return render_template('derivadas_parciales.html')

@derivadas_parciales_bp.route('/calculate', methods=['POST'])
def calculate():
    try:
        # Recibir los valores del formulario
        func_str = request.form['func']
        variable_str = request.form['variable']

        # Definir las variables simbólicas
        variables = sp.symbols(variable_str)

        # Convertir la función de cadena a expresión simbólica
        func = sp.sympify(func_str)

        # Calcular la derivada parcial
        derivative = sp.diff(func, variables)

        # Generar el procedimiento
        steps = [rf"**Paso 1: Derivar respecto a {variable_str}**: \(\frac{{\partial}}{{\partial {variable_str}}} {sp.latex(func)} = {sp.latex(derivative)}\)"]

        return render_template('derivadas_parciales.html', result=f'Resultado de la derivada: {derivative}', steps=steps)
    except ValueError as e:
        return render_template('derivadas_parciales.html', result=f"Error en la entrada: {e}")
    except Exception as e:
        return render_template('derivadas_parciales.html', result=f"Error al calcular la derivada: {e}")