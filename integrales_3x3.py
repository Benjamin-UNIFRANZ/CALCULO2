from flask import Blueprint, request, render_template
import sympy as sp

integrales_3x3_bp = Blueprint('integrales_3x3', __name__)

@integrales_3x3_bp.route('/')
def index():
    return render_template('index.html')

@integrales_3x3_bp.route('/calculate', methods=['POST'])
def calculate():
    try:
        # Recibir los valores del formulario
        func_str = request.form['func']
        x_lower = request.form['x_lower']
        x_upper = request.form['x_upper']
        y_lower = request.form['y_lower']
        y_upper = request.form['y_upper']
        z_lower = request.form['z_lower']
        z_upper = request.form['z_upper']

        # Definir las variables simbólicas
        x, y, z = sp.symbols('x y z')

        # Convertir la función de cadena a expresión simbólica
        func = sp.sympify(func_str, locals={'x': x, 'y': y, 'z': z})

        # Convertir los límites de integración a expresiones simbólicas
        x_lower = sp.sympify(x_lower, locals={'x': x, 'y': y, 'z': z})
        x_upper = sp.sympify(x_upper, locals={'x': x, 'y': y, 'z': z})
        y_lower = sp.sympify(y_lower, locals={'x': x, 'y': y, 'z': z})
        y_upper = sp.sympify(y_upper, locals={'x': x, 'y': y, 'z': z})
        z_lower = sp.sympify(z_lower, locals={'x': x, 'y': y, 'z': z})
        z_upper = sp.sympify(z_upper, locals={'x': x, 'y': y, 'z': z})

        # Realizar la integración triple paso a paso
        steps = []
        integral_z = sp.integrate(func, (z, z_lower, z_upper))
        steps.append(rf"**Paso 1: Integrar respecto a z**: \(\int_{{{z_lower}}}^{{{z_upper}}} {sp.latex(func)} \, dz = {sp.latex(integral_z)}\)")
        integral_y = sp.integrate(integral_z, (y, y_lower, y_upper))
        steps.append(rf"**Paso 2: Integrar respecto a y**: \(\int_{{{y_lower}}}^{{{y_upper}}} {sp.latex(integral_z)} \, dy = {sp.latex(integral_y)}\)")
        integral_x = sp.integrate(integral_y, (x, x_lower, x_upper))
        steps.append(rf"**Paso 3: Integrar respecto a x**: \(\int_{{{x_lower}}}^{{{x_upper}}} {sp.latex(integral_y)} \, dx = {sp.latex(integral_x)}\)")

        return render_template('index.html', result=f'Resultado de la integral: {integral_x}', steps=steps)
    except ValueError as e:
        return render_template('index.html', result=f"Error en la entrada: {e}")
    except Exception as e:
        return render_template('index.html', result=f"Error al calcular la integral: {e}")