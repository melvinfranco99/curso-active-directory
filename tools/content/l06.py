# -*- coding: utf-8 -*-
LESSON = {
 "id": "06",
 "module": "Módulo 2 · Administración",
 "accent": "blue",
 "title": "Kerberos paso a paso",
 "slides": [
  {"type":"cover","accent":"blue",
   "kicker":"MÓDULO 2 · LECCIÓN 06",
   "title_lines":["Kerberos","paso a paso"],
   "subtitle":"El protocolo de autenticación de AD explicado con claridad: tickets, TGT y TGS.",
   "footer":"Curso Active Directory · Hacking & Defensa",
   "footer2":"Entender Kerberos es entender la mitad de los ataques de AD",
   "narration":"Kerberos es el protocolo de autenticación por defecto de Active Directory, y entenderlo bien es, probablemente, lo más rentable de todo el curso. ¿Por qué? Porque la mitad de los ataques famosos a AD, como el Kerberoasting, el AS-REP Roasting o el Golden Ticket, no son más que abusos de una parte concreta del funcionamiento de Kerberos. En esta lección vamos a recorrer el protocolo paso a paso, con calma, hasta que te quede cristalino. Si entiendes esta lección, el módulo de hacking te resultará mucho más fácil."},

  {"type":"bullets","accent":"blue","title":"La idea de Kerberos",
   "lead":"Demostrar quién eres sin enviar nunca tu contraseña por la red.",
   "items":[
     {"h":"Un tercero de confianza","b":"El KDC, que vive en el controlador, media en cada autenticación."},
     {"h":"Tickets en vez de contraseñas","b":"Pruebas temporales de identidad que se presentan a los servicios."},
     {"h":"Basado en el tiempo","b":"Los tickets caducan; por eso el reloj del dominio debe ir sincronizado."},
     {"h":"Dos fases","b":"Primero consigues un TGT; luego, con él, pides tickets de servicio."},
   ],
   "narration":"La idea de Kerberos se puede resumir en una frase: demostrar quién eres sin enviar nunca tu contraseña por la red. Para lograrlo, introduce un tercero de confianza, el centro de distribución de claves o KDC, que vive dentro del controlador de dominio y media en cada autenticación. En lugar de andar enseñando la contraseña, el usuario obtiene tickets: pruebas temporales de identidad que presenta a los servicios. Como los tickets caducan al cabo de unas horas, el protocolo depende mucho del tiempo, y por eso todos los equipos del dominio deben tener el reloj sincronizado; una diferencia de más de cinco minutos rompe la autenticación. Y, muy importante, Kerberos trabaja en dos fases: primero consigues un ticket maestro, el TGT, y después, usando ese TGT, pides tickets concretos para cada servicio al que quieras acceder."},

  {"type":"diagram","accent":"green","title":"Fase 1 — AS-REQ / AS-REP: obtener el TGT",
   "lead":"El usuario se autentica ante el KDC y recibe su ticket maestro.",
   "nodes":{
     "u":{"x":130,"y":330,"w":210,"h":80,"label":"Usuario","sub":"ana.lopez","color":"cyan"},
     "kdc":{"x":560,"y":320,"w":230,"h":100,"label":"KDC","sub":"en el controlador","color":"amber","shape":"cyl"},
     "tgt":{"x":560,"y":170,"w":230,"h":60,"label":"TGT","sub":"cifrado con krbtgt","color":"purple","shape":"hex"},
     "ok":{"x":950,"y":330,"w":200,"h":70,"label":"TGT entregado","color":"green"},
   },
   "edges":[
     {"from":"u","to":"kdc","color":"cyan","label":"1. AS-REQ (timestamp cifrado)"},
     {"from":"kdc","to":"tgt","color":"purple","label":"2. crea"},
     {"from":"kdc","to":"ok","color":"green","label":"3. AS-REP"},
   ],
   "narration":"Veamos la primera fase, el intercambio AS guion REQ y AS guion REP, en la que el usuario obtiene su ticket maestro. Paso uno: Ana envía al KDC una petición llamada AS guion REQ. Dentro, incluye una marca de tiempo, el timestamp actual, cifrada con el hash de su propia contraseña. Esto es la preautenticación: como solo Ana conoce su contraseña, solo ella puede haber cifrado correctamente la hora. Paso dos: el KDC descifra el timestamp con el hash que tiene guardado de Ana; si coincide, confirma que es ella. Entonces crea el TGT, el ticket de concesión de tickets, y lo cifra con una clave secretísima: el hash de una cuenta especial llamada krbtgt. Paso tres: el KDC devuelve ese TGT al usuario en la respuesta AS guion REP. A partir de aquí, Ana tiene su pase maestro. Guarda el nombre krbtgt: esa cuenta es la llave del reino, y volveremos a ella con el Golden Ticket."},

  {"type":"diagram","accent":"blue","title":"Fase 2 — TGS-REQ / TGS-REP: ticket de servicio",
   "lead":"Con el TGT, el usuario pide un ticket para un servicio concreto.",
   "nodes":{
     "u":{"x":130,"y":330,"w":210,"h":80,"label":"Usuario","sub":"presenta su TGT","color":"cyan"},
     "kdc":{"x":560,"y":320,"w":230,"h":100,"label":"KDC","color":"amber","shape":"cyl"},
     "tgs":{"x":560,"y":170,"w":240,"h":60,"label":"TGS","sub":"cifrado con hash del servicio","color":"red","shape":"hex"},
     "srv":{"x":950,"y":330,"w":210,"h":80,"label":"Servicio","sub":"SQL, CIFS, HTTP","color":"green","shape":"cyl"},
   },
   "edges":[
     {"from":"u","to":"kdc","color":"cyan","label":"1. TGS-REQ (TGT + SPN)"},
     {"from":"kdc","to":"tgs","color":"red","label":"2. crea"},
     {"from":"kdc","to":"u","color":"purple","label":"3. TGS-REP"},
     {"from":"u","to":"srv","color":"green","label":"4. presenta el TGS"},
   ],
   "narration":"Pasemos a la segunda fase, el intercambio TGS guion REQ y TGS guion REP, en la que Ana consigue acceder a un servicio concreto, por ejemplo una base de datos. Paso uno: Ana envía al KDC una petición TGS guion REQ en la que presenta su TGT, como prueba de que ya está autenticada, e indica el SPN del servicio al que quiere acceder. Paso dos: el KDC comprueba el TGT y, si es válido, crea un ticket de servicio, el TGS, y lo cifra con el hash de la contraseña de la cuenta que ejecuta ese servicio. Paso tres: devuelve el TGS a Ana en la respuesta TGS guion REP. Paso cuatro: Ana presenta ese TGS directamente al servicio, que lo descifra con su propia clave y le da acceso. Fíjate en el detalle crucial del paso dos: el TGS va cifrado con el hash del servicio. Eso significa que quien reciba un TGS puede intentar crackear ese hash offline. Justo ahí nace el Kerberoasting."},

  {"type":"diagram","accent":"purple","title":"El intercambio completo de un vistazo",
   "lead":"Las dos fases juntas: autenticarse una vez, acceder a muchos servicios.",
   "nodes":{
     "u":{"x":100,"y":320,"w":180,"h":90,"label":"Usuario","color":"cyan"},
     "as":{"x":430,"y":180,"w":220,"h":66,"label":"AS Exchange","sub":"obtiene TGT","color":"green"},
     "tgs":{"x":430,"y":440,"w":220,"h":66,"label":"TGS Exchange","sub":"obtiene TGS","color":"blue"},
     "kdc":{"x":720,"y":300,"w":180,"h":130,"label":"KDC","sub":"krbtgt","color":"amber","shape":"cyl"},
     "svc":{"x":980,"y":320,"w":180,"h":90,"label":"Servicios","color":"purple","shape":"cyl"},
   },
   "edges":[
     {"from":"u","to":"as","color":"green"},
     {"from":"as","to":"kdc","color":"green"},
     {"from":"u","to":"tgs","color":"blue"},
     {"from":"tgs","to":"kdc","color":"blue"},
     {"from":"u","to":"svc","color":"purple","label":"acceso"},
   ],
   "narration":"Veamos las dos fases juntas, porque así se entiende la elegancia del diseño. El usuario pasa por el intercambio AS una sola vez, al principio del día, y obtiene su TGT. A partir de ahí, cada vez que necesita acceder a un servicio nuevo, solo tiene que hacer un intercambio TGS, presentando el TGT que ya tiene, para obtener el ticket de ese servicio. No vuelve a teclear la contraseña. Este es el famoso inicio de sesión único, el single sign on: te autenticas una vez y accedes a todo lo que te corresponde durante horas. El KDC, en el centro, es quien lo orquesta todo, y la cuenta krbtgt es el secreto que sostiene la confianza de todo el sistema. Si un atacante roba el hash de krbtgt, puede fabricar TGT falsos para cualquier usuario: eso es el Golden Ticket, y por eso es tan devastador."},

  {"type":"table","accent":"red","title":"Cada paso tiene su ataque",
   "lead":"Casi todo el hacking de Kerberos abusa de una pieza concreta del protocolo.",
   "headers":["Pieza del protocolo","Ataque que la abusa"],"weights":[1.3,1.7],
   "rows":[
     ["Preautenticación desactivada","AS-REP Roasting"],
     ["TGS cifrado con hash del servicio","Kerberoasting"],
     ["Robo de un TGT o TGS en memoria","Pass-the-Ticket"],
     ["Hash de krbtgt comprometido","Golden Ticket"],
     ["Hash de un servicio comprometido","Silver Ticket"],
     ["Delegación mal configurada","Abuso de delegación Kerberos"],
   ],
   "narration":"Para cerrar, conectemos lo aprendido con el módulo de hacking, porque verás que cada ataque corresponde a una pieza concreta del protocolo. Si un usuario tiene desactivada la preautenticación, un atacante puede pedir su AS guion REP y crackearlo: eso es el AS-REP Roasting. Como el TGS va cifrado con el hash del servicio, se puede pedir y crackear: eso es el Kerberoasting. Si un atacante roba un TGT o un TGS de la memoria de un equipo, puede reutilizarlo: eso es Pass-the-Ticket. Si compromete el hash de krbtgt, fabrica TGT falsos: Golden Ticket. Si compromete el hash de un servicio concreto, fabrica TGS falsos para él: Silver Ticket. Y las delegaciones mal configuradas permiten que un servicio se haga pasar por otros usuarios. Fíjate en que ninguno de estos ataques rompe la criptografía de Kerberos: todos abusan de cómo está diseñado y configurado. Por eso entender el protocolo es la mejor defensa."},

  {"type":"bullets","accent":"cyan","title":"Resumen de la lección",
   "items":[
     {"h":"Kerberos = tickets, no contraseñas","b":"El KDC, en el DC, media con un tercero de confianza."},
     {"h":"Fase 1: AS → TGT","b":"La preautenticación demuestra la identidad; el TGT se cifra con krbtgt."},
     {"h":"Fase 2: TGS → servicio","b":"El TGS se cifra con el hash del servicio (de ahí el Kerberoasting)."},
     {"h":"krbtgt es la llave del reino","b":"Su hash permite fabricar TGT falsos: el Golden Ticket."},
   ],
   "narration":"Recapitulemos esta lección clave. Kerberos autentica con tickets en lugar de contraseñas, mediante el KDC, que actúa como tercero de confianza dentro del controlador. En la primera fase, el intercambio AS, la preautenticación demuestra la identidad del usuario y este recibe su TGT, cifrado con el hash de la cuenta krbtgt. En la segunda fase, el intercambio TGS, el usuario obtiene tickets de servicio cifrados con el hash de cada servicio, lo que abre la puerta al Kerberoasting. Y por encima de todo, recuerda que la cuenta krbtgt es la llave del reino: quien tiene su hash puede fabricar TGT falsos. En la siguiente lección usaremos todo esto para diseñar un Active Directory seguro, con el modelo de niveles. Nos vemos en la lección siete."},
 ]
}
