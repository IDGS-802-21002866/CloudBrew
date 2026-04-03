# INSTRUCCIONES OBLIGATORIAS PARA AGENTES IA

Estas reglas son para cualquier agente de IA que modifique este proyecto.
Tu objetivo es respetar arquitectura por capas, naming y convenciones para evitar conflictos de integración.

## 1) Arquitectura modular obligatoria

Cada modulo debe mantener esta estructura:

/modulo
routes.py
forms.py
service.py
repository.py
model.py
/templates
listar.html
crear.html

Rutas compartidas del proyecto:

- core: configuraciones y conexion a BD.
- templates: plantillas globales compartidas (base, layout, macros).
- shared: validaciones comunes, helpers y decoradores reutilizables.
- static: recursos del frontend (css, js, imagenes).

## 2) Responsabilidad por capa (estricto)

Routes/Controllers:

- Exponen endpoints y renderizan vistas.
- Solo orquestan flujo HTTP y llaman al service.
- No contienen logica de negocio.
- Capturan excepciones y muestran mensajes flash.
- Realizan validaciones basicas de entrada (campos requeridos, formato, estructura).

Service:

- Contiene toda la logica de negocio.
- Aplica reglas del sistema y validaciones de negocio.
- Lanza excepciones de negocio (definidas en shared).
- No accede directo a HTTP ni renderiza vistas.

Repository:

- Encapsula acceso a ORM y base de datos.
- No implementa logica de negocio.
- No decide reglas funcionales del dominio.

Models:

- Definen entidades de BD y relaciones ORM.

## 3) Naming y lenguaje (obligatorio)

- Usar ESPANOL en modulos, variables y funciones, salvo palabras reservadas de framework.
- Archivos de capa se mantienen con nombre fijo: routes.py, service.py, repository.py, model.py, forms.py.
- Funciones y variables Python: snake_case.
- Clases ORM y clases normales: PascalCase y singular.
- URL paths: snake_case.
- Templates: snake_case.
- Tablas BD: snake_case y singular.
- Nombres de modulos siempre en snake_case: usuario, inventario, ordenes_compra.

## 4) Convencion de metodos por capa

Repository (formato obligatorio):

- get*<entidad>\_by*<campo>
- get*all*<entidad>
- create\_<entidad>
- update\_<entidad>
- delete\_<entidad>

Service (formato obligatorio):

- crear\_<entidad>
- actualizar\_<entidad>
- eliminar\_<entidad>
- obtener\_<entidad>
- listar\_<entidades>

Si agregas funciones extra, usar verbo en infinitivo y nombre descriptivo.

## 5) Convencion de rutas Flask

Reglas obligatorias:

- Blueprint siempre en variable bp.
- Definir url_prefix en cada modulo.
- Funciones de endpoint con verbos en infinitivo.

Patron base:

bp = Blueprint("usuarios", **name**, url_prefix="/usuarios")

@bp.route("/")
def listar():

@bp.route("/crear", methods=["GET", "POST"])
def crear():

@bp.route("/<int:id>/editar", methods=["GET", "POST"])
def editar():

@bp.route("/<int:id>/eliminar", methods=["POST"])
def eliminar():

## 6) Generalidades tecnicas

Manejo de errores:

- Las excepciones de negocio se generan en service.
- Repository no maneja errores de negocio.
- Routes captura excepciones y comunica al usuario con flash.
- Estandarizar excepciones en shared.

Validaciones:

- Validacion basica en routes/forms.
- Validacion de negocio unicamente en service.

Imports:

- Usar imports absolutos desde app.
- Orden obligatorio:
  1.  Librerias estandar.
  2.  Librerias externas.
  3.  Modulos internos.
- Importar elementos de una misma libreria en una sola linea cuando sea posible.

## 7) Reglas frontend obligatorias

- DO NOT USE IN LINE STYLES, ALWAYS USE CLASSES ONLY
- DO NOT USE CSS, ALWAYS USE TAILWIND CSS
- ALWAYS USE THE MACRO campoNuevo FOR ANY NEW THE INPUT IN HTML

## 8) Politica de cumplimiento para agentes IA

Antes de crear o editar codigo:

- Verifica la capa correcta para cada cambio.
- No mezcles responsabilidades entre routes, service y repository.
- No introduzcas naming fuera de estandar.

Al finalizar cambios:

- Confirmar que la logica de negocio quedo en service.
- Confirmar que repository solo hace acceso a datos.
- Confirmar que routes no tiene reglas de negocio.
- Confirmar que naming, imports y rutas cumplen esta guia.
