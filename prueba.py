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
        diffs = request.form['differentials']  # Obtener el orden de los diferenciales

        # Definir las variables simbólicas
        x, y, z = sp.symbols('x y z')

        # Convertir la función de cadena a expresión simbólica
        func = sp.sympify(func_str, locals={'x': x, 'y': y, 'z': z})

        # Convertir los límites de integración a expresiones simbólicas
        variables = {'x': x, 'y': y, 'z': z}
        limits = {
            'x': (sp.sympify(x_lower, locals=variables), sp.sympify(x_upper, locals=variables)),
            'y': (sp.sympify(y_lower, locals=variables), sp.sympify(y_upper, locals=variables)),
            'z': (sp.sympify(z_lower, locals=variables), sp.sympify(z_upper, locals=variables))
        }

        # Mapear las permutaciones a un orden específico
        orden_dict = {
            'dzdxdy': ('z', 'x', 'y'),
            'dxdzdy': ('x', 'z', 'y'),
            'dydzdx': ('y', 'z', 'x'),
            'dydxdz': ('y', 'x', 'z'),
            'dzdydx': ('z', 'y', 'x'),
            'dxdydz': ('x', 'y', 'z')
        }

        # Obtener el orden de integración según los diferenciales ingresados
        orden = orden_dict.get(diffs, ('z', 'y', 'x'))

        # Lista para almacenar los pasos
        steps = []

        # Integración paso a paso
        integral = func
        for idx, var in enumerate(orden):
            lim_inf, lim_sup = limits[var]

            # Guardar la expresión antes de integrar para mostrar en los pasos
            expr_before = integral

            # Realizar la integración
            integral = sp.integrate(integral, (variables[var], lim_inf, lim_sup))

            # Añadir el paso con detalles
            step = f"**Paso {idx + 1}: Integrar respecto a {var}**\n"
            step += f"Expresión antes de integrar: {sp.latex(expr_before)}\n"
            step += rf"\(\int_{{{sp.latex(lim_inf)}}}^{{{sp.latex(lim_sup)}}} {sp.latex(expr_before)} \, d{var} = {sp.latex(integral)}\)"
            steps.append(step)

        # Resultado final
        result = integral

        return render_template('index.html', result=f'Resultado de la integral: {sp.latex(result)}', steps=steps)

    except ValueError as e:
        return render_template('index.html', result=f"Error en la entrada: {e}")
    except Exception as e:
        return render_template('index.html', result=f"Error al calcular la integral: {e}")
    
    
    
    
    
    
    mmm, creo que no esta bien resultao la integral ya que no debe estar siguiendo las reglas para resolver cualquier integral triple: aqui te digo las reglas tecniva y un ejemplo tambien para que ajustes el algortimo al tecnissismo de este concepto: Introducción a la Integral Triple Una integral triple se utiliza para calcular el volumen de un sólido en el espacio tridimensional, integrando una función sobre una región específica. La forma general de una integral triple es: ∫ a b ∫ c d ∫ e f f ( x , y , z )   d z   d y   d x ∫ a b​∫ c d​∫ e f​f(x,y,z)dzdydx donde f ( x , y , z ) f(x,y,z) es la función a integrar y los límites de integración a a, b b, c c, d d, e e, y f f definen la región de integración. Pasos para Resolver una Integral Triple

Reescribir la Integral Es fundamental reescribir la integral para tener claridad sobre las variables involucradas y sus límites. En el video, se establece que: La integral más externa corresponde a la variable x x con límites de integración de 2 a 3. La segunda integral corresponde a la variable y y con límites de integración de 0 a 2 x 2x. La integral más interna corresponde a la variable z z con límites de integración de 1 a x 2 y 2 + 2 x 2 +y 2 +2. Esto se puede expresar como: ∫ 2 3 ∫ 0 2 x ∫ 1 x 2 + y 2 + 2 x y   d z   d y   d x ∫ 2 3​∫ 0 2x​∫ 1 x 2 +y 2 +2​xydzdydx 2. Identificación de Límites de Integración Los límites de integración son cruciales para definir la región sobre la cual se está integrando. En este caso: Para x x: Entre 2 y 3. Para y y: Entre 0 y 2 x 2x. Para z z: Entre 1 y x 2 + y 2 + 2 x 2 +y 2 +2. El video enfatiza que es útil graficar estas regiones en el plano xy para visualizar mejor el área sobre la que se está trabajando. 3. Visualización de la Región R La región R en el plano xy está delimitada por: La línea vertical en x = 2 x=2 y x = 3 x=3. La línea horizontal en y = 0 y=0. La línea inclinada dada por y = 2 x y=2x. Esta configuración genera un área triangular en el plano xy. 4. Integración Paso a Paso El proceso de integración se realiza comenzando desde la integral más interna hacia afuera: Integrar respecto a z z: Se evalúa la integral interna: ∫ 1 x 2 + y 2 + 2 x y   d z = x y ( z ) ∣ 1 x 2 + y 2 + 2 ∫ 1 x 2 +y 2 +2​xydz=xy(z)​

1 x 2 +y 2 +2​

Esto resulta en: x y ( ( x 2 + y 2 + 2 ) − 1 ) x y ( x 2 + y 2 + 1 ) xy((x 2 +y 2 +2)−1)=xy(x 2 +y 2 +1) Integrar respecto a y y: Ahora se evalúa: ∫ 0 2 x x y ( x 2 + y 2 + 1 )   d y ∫ 0 2x​xy(x 2 +y 2 +1)dy Este paso implica aplicar técnicas de integración para resolver. Integrar respecto a x x: Finalmente, se evalúa: ∫ 2 3 ( r e s u l t a d o   d e   l a   i n t e g r a l   a n t e r i o r )   d x ∫ 2 3​(resultadodelaintegralanterior)dx, yo pienso que deberias utlizar un swtich para lo: dzdxdy dxdzdy dydzdx dydxdz dzdydx dxdydz;para que funcione con esta logica o secuencia establecida: from flask import Blueprint, request, render_template import sympy as sp

integrales_3x3_bp = Blueprint('integrales_3x3', name)

@integrales_3x3_bp.route('/') def index(): return render_template('index.html')

@integrales_3x3_bp.route('/calculate', methods=['POST']) def calculate(): try: # Recibir los valores del formulario func_str = request.form['func'] x_lower = request.form['x_lower'] x_upper = request.form['x_upper'] y_lower = request.form['y_lower'] y_upper = request.form['y_upper'] z_lower = request.form['z_lower'] z_upper = request.form['z_upper']

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