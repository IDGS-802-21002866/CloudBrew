# Cloud brew

Sistema de gestion de producción de cervezas artesanales

## Pasos para iniciar el proyecto

- Una vez clonado el repositorio crea el entorno virtual con el siguiente comando:`py -m venv env`
- Activate tu entorno virtual con el comando `env\Script\activate`
- Instala las dependencias necesarias con el comando `pip install -r requirements.txt`
- Corre el proyecto con el comando `flask --app main --debug run`

## Pasos para compilar los estilos de tailwind

- En la carpeta static crea otra carpeta que se llame dist
- Asegurate de tener instalada la version LTS de Node.js, si no la tienes instalala: https://nodejs.org/en/download/current
- Usaremos la libreria de pnpm en lugar de la npm para mejorar eficiencia, entonces previamente ejecutaremos este comando: `npm install -g pnpm@latest-10`
- Posteriormente, en el proyecto ejecutaras el siguiente comando: `pnpm install`
- Espera a que se instalen las dependencias y ya luego ejecuta el siguiente comando: `pnpm exec tailwindcss -i ./app/static/src/input.css -o ./app/static/dist/output.css --watch`
- Recuerda mantener abierta la terminal para que se carguen los estilos correctamente.

### Notas:

- Dentro del repositorio existe un documento llamada AGENTS.md, con las instrucciones para los agentes de IA, para que sigan el patron de la arquitectura, los estilos y el naming. Asegurate de agregarlo en tu configuracion de agentes del editor de codigo.
