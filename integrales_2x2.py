from flask import Blueprint, request, render_template
import sympy as sp

integrales_2x2_bp = Blueprint('integrales_2x2', __name__)

@integrales_2x2_bp.route('/')
def integrales_2x2():
    return render_template('integrales_2x2.html')

@integrales_2x2_bp.route('/calculate', methods=['POST'])
def calculate():
    try:
        # Recibir los valores del formulario
        func_str = request.form['func']
        x_lower = request.form['x_lower']
        x_upper = request.form['x_upper']
        y_lower = request.form['y_lower']
        y_upper = request.form['y_upper']

        # Definir las variables simbólicas
        x, y = sp.symbols('x y')

        # Convertir la función de cadena a expresión simbólica
        func = sp.sympify(func_str, locals={'x': x, 'y': y})

        # Convertir los límites de integración a expresiones simbólicas
        x_lower = sp.sympify(x_lower, locals={'x': x, 'y': y})
        x_upper = sp.sympify(x_upper, locals={'x': x, 'y': y})
        y_lower = sp.sympify(y_lower, locals={'x': x, 'y': y})
        y_upper = sp.sympify(y_upper, locals={'x': x, 'y': y})

        # Realizar la integración doble paso a paso
        steps = []
        integral_y = sp.integrate(func, (y, y_lower, y_upper))
        steps.append(rf"**Paso 1: Integrar respecto a y**: \(\int_{{{y_lower}}}^{{{y_upper}}} {sp.latex(func)} \, dy = {sp.latex(integral_y)}\)")
        integral_x = sp.integrate(integral_y, (x, x_lower, x_upper))
        steps.append(rf"**Paso 2: Integrar respecto a x**: \(\int_{{{x_lower}}}^{{{x_upper}}} {sp.latex(integral_y)} \, dx = {sp.latex(integral_x)}\)")

        return render_template('integrales_2x2.html', result=f'Resultado de la integral: {integral_x}', steps=steps)
    except ValueError as e:
        return render_template('integrales_2x2.html', result=f"Error en la entrada: {e}")
    except Exception as e:
        return render_template('integrales_2x2.html', result=f"Error al calcular la integral: {e}")