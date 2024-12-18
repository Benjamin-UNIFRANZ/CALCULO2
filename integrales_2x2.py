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
        diffs = request.form['differentials']  # Obtener el orden de los diferenciales

        # Definir las variables simbólicas
        x, y = sp.symbols('x y')

        # Convertir la función de cadena a expresión simbólica
        func = sp.sympify(func_str, locals={'x': x, 'y': y})

        # Crear un diccionario para los límites de integración
        limits_dict = {
            'x': (sp.sympify(x_lower, locals={'x': x, 'y': y}), sp.sympify(x_upper, locals={'x': x, 'y': y})),
            'y': (sp.sympify(y_lower, locals={'x': x, 'y': y}), sp.sympify(y_upper, locals={'x': x, 'y': y}))
        }

        # Obtener el orden de integración de derecha a izquierda
        orden_integracion = ['y', 'x']

        # Obtener el orden de eliminación de variables según los diferenciales ingresados
        orden_eliminacion = [var for var in diffs.replace('d', '')]

        # Lista para almacenar los pasos
        steps = []

        # Integración paso a paso
        integral = func
        for idx, var in enumerate(orden_integracion):
            # Obtener la variable a eliminar según el orden de eliminación
            var_eliminar = orden_eliminacion[idx]
            # Obtener los límites correctos según el orden de integración
            lim_inf, lim_sup = limits_dict[var]

            # Guardar la expresión antes de integrar para mostrar en los pasos
            expr_before = integral

            # Realizar la integración
            integral = sp.integrate(integral, (sp.symbols(var_eliminar), lim_inf, lim_sup))

            # Expandir y simplificar después de cada integración
            integral = sp.expand(integral)
            integral = sp.simplify(integral)

            # Añadir el paso con detalles
            step = f"**Paso {idx + 1}: Integrar respecto a {var_eliminar}**\n"
            step += f"Expresión antes de integrar: {sp.latex(expr_before)}\n"
            step += rf"\(\int_{{{sp.latex(lim_inf)}}}^{{{sp.latex(lim_sup)}}} {sp.latex(expr_before)} \, d{var_eliminar} = {sp.latex(integral)}\)"
            steps.append(step)

        # Resultado final con simplificación adicional
        result = sp.expand(integral)
        result = sp.simplify(result)
        result_str = str(result)

        return render_template('integrales_2x2.html', result=f'Resultado de la integral: {result_str}', steps=steps)

    except ValueError as e:
        return render_template('integrales_2x2.html', result=f"Error en la entrada: {e}")
    except Exception as e:
        return render_template('integrales_2x2.html', result=f"Error al calcular la integral: {e}")