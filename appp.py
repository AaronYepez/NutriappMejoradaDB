from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "clave-secreta"

# Configuración de MySQL (AJUSTA SOLO SI CAMBIA ALGO EN TU PHPMyAdmin)
DB_CONFIG = {
    "host": "localhost",
    "user": "root",       # Cambia si tu usuario es otro
    "password": "",       # Pon tu contraseña si tienes
    "database": "nutriapp"
}


def get_connection():
    """Crear y devolver una conexión nueva a la base de datos."""
    return mysql.connector.connect(**DB_CONFIG)


# =====================
#        RUTAS BASE
# =====================

@app.route("/")
def index():
    # Página de inicio (puedes cambiar yepez.html por otra si quieres)
    return render_template("yepez.html")


@app.route("/principal/<int:cal>")
def principal(cal):
    # Solo dejar entrar si hay sesión
    if not session.get("valida"):
        flash("Primero inicia sesión", "error")
        return redirect(url_for("sesion"))
    return render_template("index.html", cal=cal)


@app.route("/buscar", methods=["POST", "GET"])
def buscar():
    if request.method == "POST":
        busqueda = request.form["busqueda"].strip().lower()

        if busqueda in ("calendario", "agenda", "plan"):
            return redirect(url_for("calendary"))
        elif busqueda in ("control alimenticio", "contar calorias", "comparar alimentos"):
            return redirect(url_for("crtlComida"))

    return render_template("index.html")


# =====================
#       CALENDARIO
# =====================

@app.route("/calendary")
def calendary():
    if not session.get("valida"):
        flash("Primero inicia sesión", "error")
        return redirect(url_for("sesion"))
    return render_template("calendario.html")


@app.route("/macroscal", methods=["POST", "GET"])
def macroscal():
    if request.method == "POST":
        peso = float(request.form["peso"])
        altura = float(request.form["altura"])
        edad = float(request.form["edad"])
        grasa = float(request.form["grasa"])
        genero = request.form["genero"]
        actividad = request.form["actividad"]
        objetivos = request.form["objetivos"]

        # Tasa metabólica basal (Mifflin-St Jeor)
        if genero == "hombre":
            tmb = 10 * peso + 6.25 * altura - 5 * edad + 5
        else:
            tmb = 10 * peso + 6.25 * altura - 5 * edad - 161

        factores = {
            "sedentario": 1.2,
            "ligero": 1.375,
            "moderado": 1.55,
            "intenso": 1.725,
            "muy_intenso": 1.9,
        }
        factor_act = factores.get(actividad, 1.2)
        gct = tmb * factor_act  # gasto calórico total

        # Ajuste por objetivo
        if objetivos == "bajar":
            calorias_objetivo = gct - 400
        elif objetivos == "subir":
            calorias_objetivo = gct + 300
        else:
            calorias_objetivo = gct

        # Masa magra
        masa_magra = peso * (1 - grasa / 100.0)

        # Proteínas
        if objetivos in ("bajar", "subir"):
            prot_g = masa_magra * 2.0
        else:  # mantener
            prot_g = masa_magra * 1.6

        prot_kcal = prot_g * 4

        # Grasas (25% de las calorías objetivo)
        grasa_kcal = calorias_objetivo * 0.25
        grasa_g = grasa_kcal / 9

        # Carbohidratos = calorías restantes
        carb_kcal = calorias_objetivo - prot_kcal - grasa_kcal
        if carb_kcal < 0:
            carb_kcal = 0
        carb_g = carb_kcal / 4

        resultados = {
            "cal": int(calorias_objetivo),
            "pro": int(prot_g),
            "carbo": int(carb_g),
            "grasa": int(grasa_g),
        }

        return render_template("calendario.html", resultados=resultados)

    return render_template("calendario.html")


@app.route("/macros")
def macros():
    return render_template("calendario.html")


# =====================
#      CONTROL DE COMIDA
# =====================

@app.route("/crtlComida")
def crtlComida():
    if not session.get("valida"):
        flash("Primero inicia sesión", "error")
        return redirect(url_for("sesion"))
    return render_template("ctrl.html")


@app.route("/control", methods=["GET", "POST"])
def control():
    if not session.get("valida"):
        return redirect(url_for("sesion"))

    resultado = None
    if request.method == "POST":
        peso = float(request.form["peso"])
        altura = float(request.form["altura"])
        edad = float(request.form["edad"])
        genero = request.form["genero"]
        actividad = request.form["actividad"]

        if genero == "hombre":
            resultado = 88.362 + 13.397 * peso + 4.799 * altura - 5.677 * edad
        else:
            resultado = 447.593 + 9.247 * peso + 3.098 * altura - 4.330 * edad

        if actividad == "sedentario":
            resultado *= 1.2
        elif actividad == "activo":
            resultado *= 1.55
        elif actividad == "altoRendimiento":
            resultado *= 1.9

        return render_template("ctrl.html", resultado=resultado)

    return render_template("ctrl.html")


# =====================
#       LOGIN / LOGOUT
# =====================

@app.route("/inciosecion")
def sesion():
    # Página de inicio de sesión
    return render_template("sesinguardada.html")


@app.route("/valida", methods=["POST"])
def valida():
    # Validar login
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    if not email or not password:
        flash("Todos los campos son obligatorios", "error")
        return redirect(url_for("sesion"))

    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM usuarios WHERE correo = %s", (email,))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if user and user["contraseña"] == password:
        # Guardar datos en sesión
        session["valida"] = True
        session["user_id"] = user["id"]
        session["nombre"] = user["nombre"]
        session["correo"] = user["correo"]
        session["imgPerfil"] = user["imgPerfil"]
        session["genero"] = user["genero"]
        session["actividad"] = user["actividad"]

        flash("Sesión iniciada correctamente", "success")
        return redirect(url_for("principal", cal=1))

    flash("Correo o contraseña incorrectos", "error")
    return redirect(url_for("sesion"))


@app.route("/logout")
def logout():
    # Cerrar sesión
    session.clear()
    flash("Sesión cerrada correctamente", "success")
    return redirect(url_for("sesion"))


# =====================
#        REGISTRO
# =====================

@app.route("/registrosecion/<int:paso>")
def registrosecion(paso):
    # Muestra la pantalla de registro por pasos
    return render_template("iniciosecion.html", paso=paso)


@app.route("/registro/<int:paso>", methods=["GET", "POST"])
def registro(paso):
    if request.method == "POST":

        # PASO 1: guardar datos básicos en la BD
        if paso == 1:
            nombre = request.form["nombre"]
            correo = request.form["correo"]
            contraseña = request.form["contraseña"]
            peso = request.form["peso"]
            altura = request.form["altura"]
            edad = request.form["edad"]
            imgPerfil = request.form["imgPerfil"]
            genero = request.form["genero"]
            actividad = request.form["actividad"]

            if not nombre or not correo or not contraseña or not peso or not altura or not edad:
                flash("Llena todos los campos", "error")
                return redirect(url_for("registrosecion", paso=1))

            if imgPerfil == "":
                imgPerfil = "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png"

            try:
                conn = get_connection()
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO usuarios
                    (nombre, correo, contraseña, peso, altura, edad, imgPerfil, genero, actividad)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (nombre, correo, contraseña, peso, altura, edad, imgPerfil, genero, actividad))
                conn.commit()
                cur.close()
                conn.close()
            except Exception as e:
                print("ERROR:", e)
                flash("Error al guardar usuario", "error")
                return redirect(url_for("registrosecion", paso=1))

            return redirect(url_for("registrosecion", paso=2))

        # PASO 2 (si luego quieres guardar objetivos y demás, aquí va)
        elif paso == 2:
            # Por ahora solo continúa al paso 3
            return redirect(url_for("registrosecion", paso=3))

        # PASO 3: final del registro
        elif paso == 3:
            return redirect(url_for("principal", cal=1))

    # Si llega por GET, mostrar la página del paso actual
    return render_template("iniciosecion.html", paso=paso)


# =====================
#         PERFIL
# =====================

@app.route("/perfil")
def perfil():
    if not session.get("valida"):
        return redirect(url_for("sesion"))

    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM usuarios WHERE id = %s", (session["user_id"],))
    usuario = cur.fetchone()
    cur.close()
    conn.close()

    return render_template("perfil.html", usuario=usuario)


# =====================
#    IMC Y PESO IDEAL
# =====================

def evaluar_imc(imc):
    if imc < 18.5:
        return "Tienes bajo peso. Es recomendable evaluar tu alimentación.", "alert-warning"
    elif 18.5 <= imc < 25:
        return "Tu peso es saludable. ¡Buen trabajo!", "alert-success"
    elif 25 <= imc < 30:
        return "Tienes sobrepeso. Considera mejorar hábitos de alimentación.", "alert-warning"
    else:
        return "Tienes obesidad. Es recomendable acudir con un profesional de la salud.", "alert-danger"


@app.route("/imc", methods=["GET", "POST"])
def imc():
    imc_resultado = None
    mensaje = None
    color = None

    if request.method == "POST":
        try:
            peso = float(request.form["peso"])
            altura_cm = float(request.form["altura"])
            altura = altura_cm / 100  # convertir cm a metros

            imc = peso / (altura ** 2)
            imc = round(imc, 2)

            mensaje, color = evaluar_imc(imc)
            imc_resultado = imc

        except Exception:
            imc_resultado = None

    return render_template("imc.html", imc_resultado=imc_resultado, mensaje=mensaje, color=color)


def calcular_pci(altura_cm, sexo):
    altura_in = altura_cm / 2.54
    if sexo == "hombre":
        peso_ideal = 50 + 2.3 * (altura_in - 60)
    else:
        peso_ideal = 45.5 + 2.3 * (altura_in - 60)
    return round(peso_ideal, 2)


@app.route("/pci", methods=["GET", "POST"])
def pci():
    peso_ideal = None
    if request.method == "POST":
        try:
            altura_cm = float(request.form["altura"])
            sexo = request.form["sexo"]
            peso_ideal = calcular_pci(altura_cm, sexo)
        except Exception:
            peso_ideal = None
    return render_template("idealpeso.html", peso_ideal=peso_ideal)


# =====================
#        MAIN
# =====================

if __name__ == "__main__":
    app.run(debug=True)
