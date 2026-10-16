"""Servidor HTTP local (stdlib); adaptador web que delega al caso de uso."""
import json
import mimetypes
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse
from application.use_cases import compare, simulate
from domain.models import Config

DIRECTORIO_ESTATICO = Path(__file__).parent / 'static'


class Handler(BaseHTTPRequestHandler):
    def json(self, contenido, codigo_estado=200):
        datos = json.dumps(contenido, ensure_ascii=False, allow_nan=False).encode('utf8')
        self.send_response(codigo_estado)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(datos)))
        self.end_headers()
        self.wfile.write(datos)

    def do_POST(self):
        if urlparse(self.path).path != '/api/simulate':
            return self.json({'error': 'Ruta no encontrada'}, 404)
        try:
            tamano_solicitud = int(self.headers.get('Content-Length', '0'))
            if tamano_solicitud <= 0 or tamano_solicitud > 65536:
                raise ValueError('Tamaño de solicitud inválido')
            datos = json.loads(self.rfile.read(tamano_solicitud))
            configuracion = Config(float(datos['arrival_rate']), float(datos['service_rate']),
                         float(datos['duration']), int(datos['seed']))
            return self.json(simulate(configuracion))
        except (KeyError, ValueError, TypeError) as error:
            return self.json({'error': str(error)}, 400)

    def do_GET(self):
        ruta = urlparse(self.path).path
        if ruta == '/api/scenarios':
            return self.json(compare())
        if ruta == '/':
            ruta = '/index.html'
        ruta_archivo = (DIRECTORIO_ESTATICO / ruta.lstrip('/')).resolve()
        if not ruta_archivo.is_relative_to(DIRECTORIO_ESTATICO.resolve()) or not ruta_archivo.is_file():
            self.send_error(404)
            return
        datos = ruta_archivo.read_bytes()
        self.send_response(200)
        self.send_header('Content-Type', mimetypes.guess_type(ruta_archivo.name)[0] or 'application/octet-stream')
        self.send_header('Content-Length', str(len(datos)))
        self.end_headers()
        self.wfile.write(datos)


def serve(direccion='127.0.0.1', puerto=8501):
    print(f'Simulador disponible en http://{direccion}:{puerto}')
    ThreadingHTTPServer((direccion, puerto), Handler).serve_forever()
