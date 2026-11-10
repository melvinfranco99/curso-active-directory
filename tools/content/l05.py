# -*- coding: utf-8 -*-
LESSON = {
 "id": "05",
 "module": "Módulo 2 · Administración",
 "accent": "blue",
 "title": "Group Policy (GPO) a fondo",
 "slides": [
  {"type":"cover","accent":"blue",
   "kicker":"MÓDULO 2 · LECCIÓN 05",
   "title_lines":["Group Policy (GPO)","a fondo"],
   "subtitle":"Cómo Active Directory configura y asegura miles de equipos de forma centralizada.",
   "footer":"Curso Active Directory · Hacking & Defensa",
   "footer2":"La herramienta de administración más usada en empresas",
   "narration":"Si hay una funcionalidad de Active Directory que los administradores usan todos los días, son las directivas de grupo, las GPO. Son el mecanismo que permite configurar y asegurar miles de equipos desde un único punto. En esta lección vas a entender qué son, cómo se aplican, en qué orden, y por qué son, al mismo tiempo, una herramienta poderosísima de administración y un objetivo muy apetecible para un atacante."},

  {"type":"bullets","accent":"blue","title":"¿Qué es una GPO?",
   "lead":"Un conjunto de ajustes que se aplican automáticamente a usuarios y equipos.",
   "items":[
     {"h":"Configuración centralizada","b":"Define contraseñas, permisos, software, scripts, escritorio y mucho más."},
     {"h":"Dos mitades","b":"Configuración de equipo (al arrancar) y configuración de usuario (al iniciar sesión)."},
     {"h":"Se enlaza a un contenedor","b":"Se vincula a un sitio, a un dominio o, lo más común, a una OU."},
     {"h":"Se guarda en SYSVOL","b":"Un recurso compartido del DC que todos los clientes leen."},
   ],
   "narration":"Empecemos por lo básico. Una GPO es un conjunto de ajustes de configuración que se aplican de forma automática a usuarios y equipos. Con ellas puedes definir la política de contraseñas, los permisos locales, qué software se instala, scripts de inicio, el fondo de escritorio, restricciones de seguridad y literalmente cientos de opciones más. Cada GPO tiene dos mitades: la configuración de equipo, que se aplica cuando la máquina arranca, y la configuración de usuario, que se aplica cuando alguien inicia sesión. Para que surta efecto, una GPO se enlaza a un contenedor: puede ser un sitio, el dominio entero o, lo más habitual, una unidad organizativa. Y, físicamente, las GPO se almacenan en un recurso compartido del controlador llamado SYSVOL, que todos los clientes del dominio pueden leer. Recuerda SYSVOL, porque reaparecerá cuando hablemos de ataques."},

  {"type":"diagram","accent":"blue","title":"Orden de aplicación: LSDOU",
   "lead":"Las GPO se aplican en un orden preciso; la última gana.",
   "nodes":{
     "l":{"x":110,"y":330,"w":175,"h":70,"label":"Local","sub":"1º","color":"cyan"},
     "s":{"x":330,"y":330,"w":175,"h":70,"label":"Sitio","sub":"2º","color":"green"},
     "d":{"x":550,"y":330,"w":175,"h":70,"label":"Dominio","sub":"3º","color":"amber"},
     "o":{"x":770,"y":330,"w":175,"h":70,"label":"OU","sub":"4º (gana)","color":"red"},
     "win":{"x":990,"y":320,"w":175,"h":90,"label":"Config final","color":"purple","shape":"cyl"},
   },
   "edges":[
     {"from":"l","to":"s","color":"green"},
     {"from":"s","to":"d","color":"amber"},
     {"from":"d","to":"o","color":"red"},
     {"from":"o","to":"win","color":"purple","label":"resultado"},
   ],
   "narration":"Un punto que confunde a mucha gente es el orden en que se aplican las GPO cuando hay varias. La regla se resume en el acrónimo LSDOU, que marca la secuencia: primero se aplica la política Local del equipo, después las del Sitio, luego las del Dominio y, por último, las de la OU. ¿Por qué importa el orden? Porque si dos GPO dicen cosas contradictorias, gana la que se aplica en último lugar. Y como la OU es la última, las GPO enlazadas a la OU más cercana al objeto tienen la última palabra y sobrescriben a las de niveles superiores. Existen además dos excepciones que alteran esto: la opción de forzar, enforced, que impide que una GPO superior sea sobrescrita, y el bloqueo de herencia, que corta las políticas que vienen de arriba. Dominar este orden es esencial para depurar por qué un ajuste no se aplica como esperabas."},

  {"type":"table","accent":"blue","title":"Para qué se usan en una empresa real",
   "headers":["Categoría","Ejemplo de uso"],"weights":[1.1,2],
   "rows":[
     ["Seguridad","Política de contraseñas y bloqueo de cuentas"],
     ["Restricciones","Impedir usar USB o el panel de control"],
     ["Despliegue","Instalar software y mapear unidades de red"],
     ["Scripts","Ejecutar tareas al arranque o al inicio de sesión"],
     ["Hardening","Aplicar plantillas CIS o Microsoft Security Baseline"],
   ],
   "narration":"Veamos para qué se usan de verdad las GPO en el día a día de una empresa. En seguridad, definen la política de contraseñas y el bloqueo de cuentas tras varios intentos fallidos. En restricciones, impiden cosas como usar dispositivos USB o acceder al panel de control. En despliegue, instalan software de forma automática y conectan unidades de red. Con scripts, ejecutan tareas al arrancar el equipo o al iniciar sesión el usuario. Y en hardening, es decir en el endurecimiento de la seguridad, aplican plantillas de configuración reconocidas, como las guías CIS o las líneas base de seguridad de Microsoft, que ajustan de golpe cientos de parámetros recomendados. Esta versatilidad es la razón por la que las GPO son la herramienta de administración más usada: un solo cambio bien hecho se propaga a toda la organización."},

  {"type":"compare","accent":"red","title":"Las GPO también son un objetivo","accent2":"red",
   "cols":[
     {"title":"Por qué atraen al atacante","color":"red","items":[
        {"h":"Ejecución remota masiva","b":"Modificar una GPO permite ejecutar código en todos sus equipos."},
        {"h":"SYSVOL es legible","b":"Cualquier usuario puede leer el contenido de las políticas."},
        {"h":"Secretos antiguos","b":"Contraseñas cifradas con una clave pública conocida (MS14-025)."}]},
     {"title":"Cómo protegerlas","color":"green","items":[
        {"h":"Controlar quién edita GPO","b":"Permiso de edición = casi control del dominio."},
        {"h":"Auditar cambios","b":"Vigilar la creación y modificación de directivas."},
        {"h":"Nunca guardar secretos","b":"Prohibir credenciales en GPP; usar LAPS."}]},
   ],
   "narration":"Ahora el lado oscuro: las GPO son un objetivo de primer orden para un atacante, y conviene entender por qué. En primer lugar, quien puede modificar una GPO puede ejecutar código en todos los equipos a los que esa política se aplica; es, en la práctica, ejecución remota masiva. En segundo lugar, el recurso SYSVOL donde se guardan las políticas es legible por cualquier usuario del dominio, así que un atacante puede estudiar toda la configuración. Y en tercer lugar, existe un fallo histórico, conocido como MS catorce guion cero veinticinco, por el que algunas GPO antiguas guardaban contraseñas cifradas con una clave que Microsoft publicó; cualquiera podía descifrarlas leyendo SYSVOL. ¿Cómo se protegen? Controlando estrictamente quién tiene permiso para editar GPO, porque ese permiso equivale casi a controlar el dominio; auditando todos los cambios; y no guardando jamás credenciales dentro de las políticas, usando en su lugar soluciones como LAPS."},

  {"type":"code","accent":"blue","title":"Trabajar con GPO desde PowerShell",
   "lead":"Las GPO también se gestionan y se auditan por línea de comandos.",
   "term_title":"PowerShell · administrador",
   "code":[
     {"k":"ps","t":"Get-GPO -All | Select DisplayName, Id"},
     {"k":"out","t":"Default Domain Policy      31B2F340-..."},
     {"k":"out","t":"Politica-Contrasenas       7A1C9E55-..."},
     {"k":"ps","t":"Get-GPOReport -Name 'Politica-Contrasenas' -ReportType Html -Path rep.html"},
     {"k":"cmt","t":"# Enlazar una GPO a una OU"},
     {"k":"ps","t":"New-GPLink -Name 'Hardening-Base' -Target 'OU=Servidores,DC=empresa,DC=local'"},
     {"k":"good","t":"GpoId : Hardening-Base  Enforced : Yes"},
   ],
   "narration":"Aunque las GPO se suelen gestionar con una consola gráfica, conviene saber que también se manejan por línea de comandos con PowerShell, lo cual es clave para auditarlas a escala. Con el comando Get guion GPO guion All obtienes la lista de todas las directivas del dominio con su nombre y su identificador. Con Get guion GPOReport puedes generar un informe completo en HTML de lo que hace una política concreta, perfecto para revisiones de seguridad. Y con New guion GPLink enlazas una GPO a una unidad organizativa, por ejemplo para aplicar una política de hardening a la OU de servidores, con la opción de forzarla. Estos comandos son también los que usa un defensor para inventariar las políticas, y los que usa un atacante para descubrir dónde apuntar. Conocer la línea de comandos te da visibilidad completa sobre la configuración del dominio."},

  {"type":"bullets","accent":"blue","title":"Buenas prácticas con GPO",
   "items":[
     {"h":"Pocas GPO, bien nombradas","b":"Nombres claros y documentados evitan errores y conflictos."},
     {"h":"Prueba antes de desplegar","b":"Usa una OU de pruebas y filtros de seguridad o WMI."},
     {"h":"Separa seguridad de configuración","b":"GPO distintas para hardening y para ajustes de usuario."},
     {"h":"Revisa permisos de edición","b":"Solo un grupo reducido y de alto nivel debe poder editarlas."},
   ],
   "narration":"Cerremos con buenas prácticas. Primera: mantén pocas GPO y nómbralas con claridad; un bosque con cientos de políticas con nombres crípticos es una pesadilla de mantener y una fuente de errores de seguridad. Segunda: prueba siempre antes de desplegar, aplicando la GPO primero a una OU de pruebas, y apóyate en filtros de seguridad o filtros WMI para acotar a qué equipos llega. Tercera: separa las políticas de seguridad de las de configuración; no mezcles el hardening con el fondo de escritorio en la misma GPO. Y cuarta, la más importante en seguridad: revisa periódicamente quién tiene permiso para editar GPO y redúcelo a un grupo muy reducido y de alto nivel, porque, como hemos visto, ese permiso es casi equivalente a ser administrador del dominio."},

  {"type":"bullets","accent":"cyan","title":"Resumen de la lección",
   "items":[
     {"h":"GPO = configuración centralizada","b":"Dos mitades: equipo y usuario; se enlazan a OU, dominio o sitio."},
     {"h":"Orden LSDOU","b":"Local, Sitio, Dominio, OU; la última gana, salvo enforced o bloqueo."},
     {"h":"Guardadas en SYSVOL","b":"Legibles por todos: cuidado con los secretos."},
     {"h":"Objetivo de ataque","b":"Editar una GPO = ejecutar código en toda la flota."},
   ],
   "narration":"Resumamos. Las GPO son el mecanismo de configuración centralizada de Active Directory, con una mitad de equipo y otra de usuario, y se enlazan a OU, dominios o sitios. Se aplican en el orden LSDOU, local, sitio, dominio y OU, donde la última gana, salvo que se use la opción de forzar o el bloqueo de herencia. Se almacenan en SYSVOL, un recurso legible por todos los usuarios, lo que obliga a no guardar nunca secretos en ellas. Y son un objetivo de ataque de primer nivel, porque modificar una GPO equivale a ejecutar código en toda la flota de equipos. En la próxima lección veremos cómo diseñar un Active Directory seguro desde el principio, con el modelo de niveles o Tier Model. Nos vemos en la lección seis."},
 ]
}
