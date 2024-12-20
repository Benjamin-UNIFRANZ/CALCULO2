from flask import Blueprint, request, render_template, url_for
import sympy as sp
import numpy as np
import plotly.graph_objects as go
from pathlib import Path
import logging

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

integrales_3x3_bp = Blueprint('integrales_3x3', __name__)

# Configurar directorio para gráficas
STATIC_DIR = Path(__file__).parent / 'static' / 'plots'
STATIC_DIR.mkdir(parents=True, exist_ok=True)
logger.debug(f"STATIC_DIR: {STATIC_DIR}")

def create_3d_plot(func, x, y, z, x_lower, x_upper, y_lower, y_upper):
    """Crear gráfica 3D interactiva"""
    try:
        # Convertir límites a valores numéricos
        x_min = float(x_lower.evalf())
        x_max = float(x_upper.evalf())
        y_min = float(y_lower.subs(y, 0).evalf())
        y_max = float(y_upper.subs(y, 0).evalf())

        logger.debug(f"x_min: {x_min}, x_max: {x_max}, y_min: {y_min}, y_max: {y_max}")

        # Generar puntos
        x_vals = np.linspace(x_min, x_max, 50)
        y_vals = np.linspace(y_min, y_max, 50)
        X, Y = np.meshgrid(x_vals, y_vals)
        Z = np.zeros_like(X)
        
        # Evaluar función
        for i in range(len(x_vals)):
            for j in range(len(y_vals)):
                try:
                    subs_dict = {x: X[i,j], y: Y[i,j], z: 0}
                    Z[i,j] = float(func.subs(subs_dict).evalf())
                except Exception as e:
                    logger.error(f"Error al evaluar la función en ({X[i,j]}, {Y[i,j]}): {e}")
                    Z[i,j] = np.nan

        # Crear figura
        fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y)])
        fig.update_layout(
            title=f'Función: {func}',
            scene = dict(
                xaxis_title='X',
                yaxis_title='Y',
                zaxis_title='Z'
            ),
            width=800,
            height=600
        )
        
        # Guardar gráfica
        filename = f'plot_{hash(str(func))}.html'
        plot_path = STATIC_DIR / filename
        fig.write_html(str(plot_path))
        logger.debug(f"Gráfica guardada en: {plot_path}")
        return f'plots/{filename}'
    except Exception as e:
        logger.error(f"Error en create_3d_plot: {e}")
        return None

@integrales_3x3_bp.route('/')
def index():
    return render_template('index.html')


@integrales_3x3_bp.route('/calculate', methods=['POST'])
def calculate():
    try:
        # Recibir valores del formulario
        func_str = request.form['func']
        x_lower_str = request.form['x_lower']
        x_upper_str = request.form['x_upper']
        y_lower_str = request.form['y_lower']
        y_upper_str = request.form['y_upper']
        z_lower_str = request.form['z_lower']
        z_upper_str = request.form['z_upper']
        diffs = request.form['differentials']
        action = request.form['action']

        logger.debug(f"Datos recibidos: func={func_str}, x_lower={x_lower_str}, x_upper={x_upper_str}, y_lower={y_lower_str}, y_upper={y_upper_str}, z_lower={z_lower_str}, z_upper={z_upper_str}, diffs={diffs}, action={action}")

        # Variables simbólicas
        x, y, z = sp.symbols('x y z')

        # Convertir función
        func = sp.sympify(func_str, locals={'x': x, 'y': y, 'z': z})

        # Convertir límites de integración a expresiones simbólicas
        x_lower = sp.sympify(x_lower_str, locals={'x': x, 'y': y, 'z': z})
        x_upper = sp.sympify(x_upper_str, locals={'x': x, 'y': y, 'z': z})
        y_lower = sp.sympify(y_lower_str, locals={'x': x, 'y': y, 'z': z})
        y_upper = sp.sympify(y_upper_str, locals={'x': x, 'y': y, 'z': z})
        z_lower = sp.sympify(z_lower_str, locals={'x': x, 'y': y, 'z': z})
        z_upper = sp.sympify(z_upper_str, locals={'x': x, 'y': y, 'z': z})

        # Definir límites de integración
        limits_dict = {
            'x': (x_lower, x_upper),
            'y': (y_lower, y_upper),
            'z': (z_lower, z_upper)
        }

        if action == 'calculate':
            # Orden de integración
            orden_integracion = ['z', 'y', 'x']
            orden_eliminacion = [var for var in diffs.replace('d', '')]

            # Lista para pasos
            steps = []
            
            # Integración paso a paso
            integral = func
            for idx, var in enumerate(orden_integracion):
                var_eliminar = orden_eliminacion[idx]
                lim_inf, lim_sup = limits_dict[var]
                
                expr_before = integral
                integral = sp.integrate(integral, (sp.symbols(var_eliminar), lim_inf, lim_sup))
                integral = sp.expand(integral)
                integral = sp.simplify(integral)
                
                step = f"**Paso {idx + 1}: Integrar respecto a {var_eliminar}**\n"
                step += f"Expresión antes de integrar: {sp.latex(expr_before)}\n"
                step += rf"\(\int_{{{sp.latex(lim_inf)}}}^{{{sp.latex(lim_sup)}}} {sp.latex(expr_before)} \, d{var_eliminar} = {sp.latex(integral)}\)"
                steps.append(step)

            # Resultado final
            result = sp.expand(integral)
            result = sp.simplify(result)
            result_str = str(result)
            
            return render_template('index.html', 
                                 result=f'Resultado: {result_str}', 
                                 steps=steps)

        elif action == 'plot':
            # Crear gráfica 3D
            plot_url = create_3d_plot(
                func, x, y, z,
                x_lower, x_upper,
                y_lower, y_upper
            )

            if plot_url:
                logger.debug(f"Gráfica creada: {plot_url}")
            else:
                logger.error("No se pudo crear la gráfica")

            return render_template('index.html', 
                                 plot_url=plot_url)

    except Exception as e:
        logger.error(f"Error en calculate: {e}")
        return render_template('index.html', 
                             result=f"Error: {str(e)}")
    try:
        # Recibir valores del formulario
        func_str = request.form['func']
        x_lower_str = request.form['x_lower']
        x_upper_str = request.form['x_upper']
        y_lower_str = request.form['y_lower']
        y_upper_str = request.form['y_upper']
        z_lower_str = request.form['z_lower']
        z_upper_str = request.form['z_upper']
        diffs = request.form['differentials']
        action = request.form['action']

        logger.debug(f"Datos recibidos: func={func_str}, x_lower={x_lower_str}, x_upper={x_upper_str}, y_lower={y_lower_str}, y_upper={y_upper_str}, z_lower={z_lower_str}, z_upper={z_upper_str}, diffs={diffs}, action={action}")

        # Variables simbólicas
        x, y, z = sp.symbols('x y z')

        # Convertir función
        func = sp.sympify(func_str, locals={'x': x, 'y': y, 'z': z})

        # Convertir límites de integración a expresiones simbólicas
        x_lower = sp.sympify(x_lower_str, locals={'x': x, 'y': y, 'z': z})
        x_upper = sp.sympify(x_upper_str, locals={'x': x, 'y': y, 'z': z})
        y_lower = sp.sympify(y_lower_str, locals={'x': x, 'y': y, 'z': z})
        y_upper = sp.sympify(y_upper_str, locals={'x': x, 'y': y, 'z': z})
        z_lower = sp.sympify(z_lower_str, locals={'x': x, 'y': y, 'z': z})
        z_upper = sp.sympify(z_upper_str, locals={'x': x, 'y': y, 'z': z})

        if action == 'calculate':
            # Orden de integración
            orden_integracion = ['z', 'y', 'x']
            orden_eliminacion = [var for var in diffs.replace('d', '')]

            # Lista para pasos
            steps = []
            
            # Integración paso a paso
            integral = func
            for idx, var in enumerate(orden_integracion):
                var_eliminar = orden_eliminacion[idx]
                lim_inf, lim_sup = limits_dict[var]
                
                expr_before = integral
                integral = sp.integrate(integral, (sp.symbols(var_eliminar), lim_inf, lim_sup))
                integral = sp.expand(integral)
                integral = sp.simplify(integral)
                
                step = f"**Paso {idx + 1}: Integrar respecto a {var_eliminar}**\n"
                step += f"Expresión antes de integrar: {sp.latex(expr_before)}\n"
                step += rf"\(\int_{{{sp.latex(lim_inf)}}}^{{{sp.latex(lim_sup)}}} {sp.latex(expr_before)} \, d{var_eliminar} = {sp.latex(integral)}\)"
                steps.append(step)

            # Resultado final
            result = sp.expand(integral)
            result = sp.simplify(result)
            result_str = str(result)
            
            return render_template('index.html', 
                                 result=f'Resultado: {result_str}', 
                                 steps=steps)

        elif action == 'plot':
            # Crear gráfica 3D
            plot_url = create_3d_plot(
                func, x, y, z,
                x_lower, x_upper,
                y_lower, y_upper
            )

            if plot_url:
                logger.debug(f"Gráfica creada: {plot_url}")
            else:
                logger.error("No se pudo crear la gráfica")

            return render_template('index.html', 
                                 plot_url=plot_url)

    except Exception as e:
        logger.error(f"Error en calculate: {e}")
        return render_template('index.html', 
                             result=f"Error: {str(e)}")