# -*- coding: utf-8 -*-
LESSON = {
 "id": "15",
 "module": "Módulo 4 · Defensa",
 "accent": "green",
 "title": "Detección y respuesta",
 "slides": [
  {"type":"cover","accent":"green",
   "kicker":"MÓDULO 4 · LECCIÓN 15",
   "title_lines":["Detección y","respuesta"],
   "subtitle":"Ver al atacante dentro del dominio y reaccionar antes de que sea tarde.",
   "footer":"Curso Active Directory · Hacking & Defensa",
   "footer2":"Lección final del curso",
   "narration":"Llegamos a la última lección del curso. Por muy bueno que sea nuestro hardening, debemos asumir que un atacante determinado puede entrar. La defensa madura no solo levanta muros, también instala alarmas y tiene un plan para cuando suenan. En esta lección veremos cómo detectar la actividad de un atacante dentro del dominio a través de los registros de eventos y un SIEM, qué herramientas especializadas existen, y cómo responder a un incidente. Es la pieza que cierra el círculo de la seguridad en Active Directory."},

  {"type":"table","accent":"green","title":"Eventos de Windows que delatan un ataque",
   "lead":"Los controladores registran huellas; hay que saber cuáles mirar.",
   "headers":["Evento","Qué indica","Ataque asociado"],"weights":[0.7,1.6,1.3],
   "rows":[
     ["4769","Petición de ticket de servicio (RC4)","Kerberoasting"],
     ["4768","Petición de TGT anómala","AS-REP Roasting"],
     ["4624 / 4625","Inicio de sesión / fallido","Fuerza bruta, movimiento lateral"],
     ["4662","Acceso a objeto con replicación","DCSync"],
     ["4672","Privilegios especiales asignados","Uso de cuentas privilegiadas"],
     ["7045","Servicio nuevo instalado","PsExec / ejecución remota"],
   ],
   "narration":"Empecemos por lo más fundamental: los registros de eventos que generan los propios controladores. Windows deja huellas de casi todo, pero hay que saber cuáles vigilar. El evento cuatro mil setecientos sesenta y nueve registra las peticiones de tickets de servicio; muchas con cifrado RC4 delatan un Kerberoasting. El cuatro mil setecientos sesenta y ocho registra peticiones de TGT, útil para ver AS-REP Roasting. Los eventos cuatro mil seiscientos veinticuatro y veinticinco son los inicios de sesión, correctos y fallidos, que revelan fuerza bruta y movimiento lateral. El cuatro mil seiscientos sesenta y dos, cuando aparece con permisos de replicación, es una señal clásica de DCSync. El cuatro mil seiscientos setenta y dos indica el uso de cuentas con privilegios especiales. Y el siete mil cuarenta y cinco avisa de la instalación de un servicio nuevo, la firma típica de PsExec. Conocer este puñado de eventos es el abecé de la detección en Active Directory."},

  {"type":"diagram","accent":"green","title":"De los logs al SIEM",
   "lead":"Centralizar, correlacionar y alertar en tiempo casi real.",
   "nodes":{
     "dc":{"x":100,"y":200,"w":180,"h":70,"label":"Controladores","sub":"eventos","color":"amber","shape":"cyl"},
     "ep":{"x":100,"y":330,"w":180,"h":70,"label":"Endpoints","sub":"EDR / Sysmon","color":"cyan"},
     "net":{"x":100,"y":460,"w":180,"h":64,"label":"Red","sub":"tráfico","color":"blue"},
     "siem":{"x":470,"y":320,"w":230,"h":110,"label":"SIEM","sub":"correlación","color":"green","shape":"hex"},
     "soc":{"x":870,"y":320,"w":220,"h":100,"label":"SOC","sub":"analistas + respuesta","color":"purple","shape":"cyl"},
   },
   "edges":[
     {"from":"dc","to":"siem","color":"amber"},
     {"from":"ep","to":"siem","color":"cyan"},
     {"from":"net","to":"siem","color":"blue"},
     {"from":"siem","to":"soc","color":"purple","label":"alertas"},
   ],
   "narration":"Un evento aislado en un controlador no sirve de mucho; la clave es centralizarlo todo. Para eso está el SIEM, el sistema de gestión de eventos de seguridad. El SIEM recoge los registros de varias fuentes a la vez: los eventos de los controladores de dominio, la telemetría de los endpoints a través de soluciones EDR o del agente Sysmon, y los datos del tráfico de red. Con todo junto, el SIEM hace su magia: la correlación. Por ejemplo, un inicio de sesión fallido no alarma, pero cincuenta inicios fallidos seguidos de uno exitoso y, acto seguido, la instalación de un servicio remoto, es un patrón de ataque claro. El SIEM detecta esas combinaciones y genera alertas, que llegan al SOC, el centro de operaciones de seguridad, donde los analistas investigan y lanzan la respuesta. Este flujo, de los logs al SIEM y del SIEM al analista, es la columna vertebral de la detección moderna."},

  {"type":"bullets","accent":"green","title":"Herramientas especializadas en identidad",
   "items":[
     {"h":"Microsoft Defender for Identity","b":"Analiza el tráfico de los DC y detecta DCSync, Golden Ticket, recon..."},
     {"h":"Sysmon","b":"Telemetría detallada de procesos, red y acceso a LSASS."},
     {"h":"Honeytokens","b":"Cuentas y objetos trampa que alertan con altísima fiabilidad."},
     {"h":"Auditoría avanzada + PingCastle","b":"Medir el nivel de exposición del dominio y su evolución."},
   ],
   "narration":"Más allá del SIEM genérico, existen herramientas especializadas en proteger la identidad. Microsoft Defender for Identity, antes conocido como ATA, se instala junto a los controladores, analiza su tráfico y su comportamiento, y detecta de forma nativa ataques como DCSync, Golden Ticket o la fase de reconocimiento, con muy pocos falsos positivos. Sysmon es un agente gratuito de Microsoft que aporta una telemetría riquísima: creación de procesos, conexiones de red y, muy valioso, los accesos al proceso LSASS, que delatan a Mimikatz. Los honeytokens, que ya mencionamos, son cuentas y objetos trampa cuyo único propósito es ser tocados por un atacante; como nadie legítimo los usa jamás, una alerta sobre ellos es casi siempre un incidente real. Y herramientas como PingCastle permiten medir el nivel de exposición del dominio con una puntuación, y seguir su evolución en el tiempo, algo muy útil para justificar y priorizar las mejoras de seguridad."},

  {"type":"diagram","accent":"blue","title":"El ciclo de respuesta a incidentes",
   "lead":"Un plan ensayado marca la diferencia entre un susto y una catástrofe.",
   "nodes":{
     "p":{"x":90,"y":320,"w":165,"h":72,"label":"Preparar","color":"green"},
     "d":{"x":290,"y":320,"w":165,"h":72,"label":"Detectar","color":"cyan"},
     "c":{"x":490,"y":320,"w":165,"h":72,"label":"Contener","color":"amber"},
     "e":{"x":690,"y":320,"w":165,"h":72,"label":"Erradicar","color":"red"},
     "r":{"x":890,"y":320,"w":175,"h":72,"label":"Recuperar","color":"purple"},
   },
   "edges":[
     {"from":"p","to":"d","color":"cyan"},
     {"from":"d","to":"c","color":"amber"},
     {"from":"c","to":"e","color":"red"},
     {"from":"e","to":"r","color":"purple"},
   ],
   "narration":"Cuando la alerta se confirma, entra en juego la respuesta a incidentes, que sigue un ciclo bien definido. Preparar es la fase previa: tener el plan escrito, los contactos claros, las copias de seguridad probadas y, idealmente, haber ensayado el escenario. Detectar es identificar y confirmar que hay un incidente real, apoyándose en todo lo que acabamos de ver. Contener es frenar la hemorragia: aislar los equipos afectados, deshabilitar las cuentas comprometidas, cortar el acceso del atacante sin avisarle antes de tiempo. Erradicar es eliminar su presencia: borrar el malware, cerrar las puertas traseras y, si krbtgt se vio comprometido, rotarlo dos veces. Y recuperar es restaurar los sistemas de forma segura y volver a la normalidad vigilando que el atacante no regrese. Una organización que ha ensayado este ciclo responde en horas; una que improvisa puede tardar semanas y sufrir un daño mucho mayor. El plan marca la diferencia entre un susto y una catástrofe."},

  {"type":"stat","accent":"green","title":"Las ideas que debes recordar del curso",
   "cards":[
     {"big":"Asumir","h":"la brecha","b":"Prevenir, pero también detectar y responder. Nadie es inexpugnable.","color":"cyan"},
     {"big":"Identidad","h":"es el perímetro","b":"En AD, controlar las credenciales es controlarlo todo.","color":"amber"},
     {"big":"Capas","h":"defensa en profundidad","b":"Ninguna medida basta sola; es su suma la que protege.","color":"green"},
   ],
   "narration":"Antes de despedirnos, quedémonos con las tres grandes ideas que atraviesan todo el curso. Primera: asume la brecha. Un defensor maduro no solo intenta prevenir, también detecta y responde, porque ningún sistema es inexpugnable y la pregunta no es si te atacarán, sino cuándo. Segunda: en Active Directory, la identidad es el perímetro. Ya no basta con proteger la frontera de la red; controlar las credenciales y los privilegios es, literalmente, controlarlo todo. Y tercera: defensa en profundidad. A lo largo del curso has visto que ninguna medida basta por sí sola; es la suma de muchas capas, hardening, segmentación, detección y respuesta, la que de verdad protege el dominio. Si interiorizas estas tres ideas, tendrás la mentalidad correcta para administrar o defender cualquier Active Directory."},

  {"type":"quote","accent":"green",
   "text":"La seguridad de Active Directory no es un producto que se instala, sino un proceso que se mantiene cada día.",
   "by":"Conclusión del curso",
   "narration":"Y con esto cerramos el curso. La seguridad de Active Directory no es un producto que se instala una vez y se olvida, sino un proceso que se mantiene cada día. Has recorrido el camino completo: desde qué es un dominio y cómo funciona por dentro, pasando por cómo lo administra una empresa, cómo lo ataca un adversario paso a paso, y cómo se defiende con hardening, detección y respuesta. Ahora tienes una visión de trescientos sesenta grados, la misma que comparten los mejores administradores y los mejores profesionales de seguridad. Te animo a montar tu laboratorio, practicar cada técnica con responsabilidad y seguir profundizando. Gracias por acompañarme en este curso de Active Directory, hacking y defensa. Mucha suerte, y nos vemos en la red."},
 ]
}
