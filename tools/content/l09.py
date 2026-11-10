# -*- coding: utf-8 -*-
LESSON = {
 "id": "09",
 "module": "Módulo 3 · Hacking",
 "accent": "red",
 "title": "AS-REP Roasting y Kerberoasting",
 "slides": [
  {"type":"cover","accent":"red",
   "kicker":"MÓDULO 3 · LECCIÓN 09",
   "title_lines":["AS-REP Roasting","y Kerberoasting"],
   "subtitle":"Dos ataques a Kerberos que solo necesitan una cuenta de dominio normal.",
   "footer":"Curso Active Directory · Hacking & Defensa",
   "footer2":"Los ataques de cracking offline más habituales en empresas",
   "narration":"En esta lección vemos dos de los ataques más habituales y rentables contra Active Directory: el AS-REP Roasting y el Kerberoasting. Ambos tienen una característica temible: solo necesitan una cuenta de dominio normal y corriente, sin ningún privilegio especial. Y ambos permiten obtener material cifrado que se puede crackear tranquilamente offline, sin hacer ruido en la red. Son, en muchas auditorías, el primer gran salto del atacante. Recuerda: practícalos solo en tu laboratorio."},

  {"type":"diagram","accent":"red","title":"AS-REP Roasting: el fallo de la preautenticación",
   "lead":"Abusa de cuentas que tienen desactivada la preautenticación de Kerberos.",
   "nodes":{
     "att":{"x":120,"y":330,"w":200,"h":80,"label":"Atacante","sub":"sin credenciales del user","color":"red"},
     "kdc":{"x":540,"y":320,"w":230,"h":100,"label":"KDC","color":"amber","shape":"cyl"},
     "rep":{"x":540,"y":170,"w":240,"h":60,"label":"AS-REP","sub":"cifrado con hash del user","color":"purple","shape":"hex"},
     "crack":{"x":920,"y":330,"w":210,"h":80,"label":"Hashcat","sub":"cracking offline","color":"green"},
   },
   "edges":[
     {"from":"att","to":"kdc","color":"red","label":"1. AS-REQ (sin preauth)"},
     {"from":"kdc","to":"rep","color":"purple","label":"2. responde"},
     {"from":"kdc","to":"att","color":"purple","label":"3. AS-REP"},
     {"from":"att","to":"crack","color":"green","label":"4. crackea"},
   ],
   "narration":"Empecemos por el AS-REP Roasting. Recuerda de la lección de Kerberos que, normalmente, para pedir un TGT hay que preautenticarse: enviar un timestamp cifrado con tu contraseña. Pero algunas cuentas tienen esa preautenticación desactivada, a veces por compatibilidad con sistemas antiguos. Y ahí está el fallo. Paso uno: el atacante pide un TGT para esa cuenta vulnerable, sin preautenticarse, es decir sin conocer su contraseña. Paso dos: como la cuenta no exige preautenticación, el KDC responde tan tranquilo. Paso tres: en esa respuesta, el AS-REP, viaja una parte cifrada con el hash de la contraseña de la víctima. Paso cuatro: el atacante se lleva ese material a casa y lo crackea offline con Hashcat. Si la contraseña es débil, la recupera. Lo peligroso es que el atacante no necesitaba conocer la contraseña de la víctima para empezar: le bastaba con saber que esa cuenta existía y era vulnerable."},

  {"type":"code","accent":"red","title":"AS-REP Roasting en la práctica",
   "term_title":"kali@attacker: ~",
   "code":[
     {"k":"cmt","t":"# Buscar cuentas sin preautenticación y pedir su AS-REP"},
     {"k":"cmd","t":"GetNPUsers.py empresa.local/ -usersfile users.txt -no-pass"},
     {"k":"out","t":"[-] carlos: KDC_ERR_PREAUTH_REQUIRED (protegido)"},
     {"k":"hi","t":"$krb5asrep$23$legacy@EMPRESA.LOCAL:a1b2...f9 (vulnerable)"},
     {"k":"cmd","t":"hashcat -m 18200 asrep.txt rockyou.txt"},
     {"k":"good","t":"legacy : Primavera2023   (contraseña recuperada)"},
   ],
   "narration":"Veámoslo con comandos reales. Con el script GetNPUsers de Impacket, le pasamos una lista de usuarios y la opción no guion pass, que significa sin contraseña. La herramienta pregunta al KDC por cada uno. Para la mayoría, como carlos, el KDC responde que exige preautenticación, así que están protegidos. Pero para la cuenta legacy, una cuenta antigua con la preautenticación desactivada, obtenemos su AS-REP: ese hash que empieza por krb5asrep. Acto seguido se lo pasamos a Hashcat con el modo dieciocho mil doscientos, junto a un diccionario como el famoso rockyou. Como la contraseña era débil, Primavera dos mil veintitrés, la recuperamos en segundos. Ya tenemos una credencial válida más del dominio, y todo el cracking se hizo offline, sin tocar la red de la víctima."},

  {"type":"diagram","accent":"red","title":"Kerberoasting: cazar cuentas de servicio",
   "lead":"Cualquier usuario puede pedir un TGS y crackear el hash del servicio.",
   "nodes":{
     "att":{"x":120,"y":330,"w":200,"h":80,"label":"Atacante","sub":"cuenta de dominio","color":"red"},
     "kdc":{"x":540,"y":320,"w":230,"h":100,"label":"KDC","color":"amber","shape":"cyl"},
     "tgs":{"x":540,"y":170,"w":250,"h":60,"label":"TGS","sub":"cifrado con hash de svc_sql","color":"purple","shape":"hex"},
     "crack":{"x":920,"y":330,"w":210,"h":80,"label":"Hashcat","sub":"cracking offline","color":"green"},
   },
   "edges":[
     {"from":"att","to":"kdc","color":"red","label":"1. pide TGS del SPN"},
     {"from":"kdc","to":"tgs","color":"purple","label":"2. emite"},
     {"from":"kdc","to":"att","color":"purple","label":"3. entrega TGS"},
     {"from":"att","to":"crack","color":"green","label":"4. crackea offline"},
   ],
   "narration":"Pasemos al Kerberoasting, probablemente el ataque más característico de AD. Recuerda que, en la segunda fase de Kerberos, cuando pides un ticket de servicio, el KDC te lo entrega cifrado con el hash de la cuenta que ejecuta ese servicio. Y aquí está la clave: cualquier usuario del dominio puede pedir un ticket para cualquier servicio con SPN. Paso uno: el atacante, con su cuenta normal, pide al KDC un ticket de servicio para el SPN de, por ejemplo, el servidor SQL, cuya cuenta es svc guion sql. Paso dos: el KDC emite el ticket, sin sospechar nada, porque es una petición totalmente legítima. Paso tres: se lo entrega al atacante. Paso cuatro: ese ticket va cifrado con el hash de svc guion sql, así que el atacante se lo lleva y lo crackea offline. Si la cuenta de servicio tiene una contraseña débil, cosa muy habitual, recupera su clave en claro. Y las cuentas de servicio suelen tener privilegios altos."},

  {"type":"code","accent":"red","title":"Kerberoasting en la práctica",
   "term_title":"kali@attacker: ~",
   "code":[
     {"k":"cmt","t":"# Listar SPN y pedir sus tickets de servicio"},
     {"k":"cmd","t":"GetUserSPNs.py empresa.local/ana:'Passw0rd' -request"},
     {"k":"out","t":"ServicePrincipalName    Name       MemberOf"},
     {"k":"out","t":"MSSQL/srv-sql:1433      svc_sql    Domain Admins"},
     {"k":"hi","t":"$krb5tgs$23$*svc_sql*$e3f...a9c"},
     {"k":"cmd","t":"hashcat -m 13100 tgs.txt rockyou.txt"},
     {"k":"good","t":"svc_sql : Verano2024!   -> ¡y es Domain Admin!"},
   ],
   "narration":"Veamos el Kerberoasting con comandos. Con el script GetUserSPNs de Impacket, usando nuestra cuenta de dominio y la opción request, pedimos los tickets de todas las cuentas que tienen SPN. La herramienta nos lista los servicios y, fíjate en algo inquietante, nos muestra a qué grupos pertenece cada cuenta: svc guion sql está nada menos que en Domain Admins. Obtenemos su ticket, ese hash que empieza por krb5tgs, y se lo pasamos a Hashcat con el modo trece mil cien y un diccionario. La contraseña, Verano dos mil veinticuatro con admiración, era débil y cae enseguida. Y como esa cuenta de servicio es administradora de dominio, acabamos de pasar de un usuario normal a controlar todo el dominio con un único ataque. Este escenario, una cuenta de servicio con contraseña débil y privilegios excesivos, es dolorosamente frecuente en empresas reales."},

  {"type":"compare","accent":"green","title":"Cómo defenderse de ambos ataques",
   "cols":[
     {"title":"Contra AS-REP Roasting","color":"amber","items":[
        {"h":"Exigir preautenticación","b":"No desactivarla salvo necesidad absoluta; auditar quién la tiene."},
        {"h":"Contraseñas fuertes","b":"Si no hay contraseña débil, no hay cracking."}]},
     {"title":"Contra Kerberoasting","color":"green","items":[
        {"h":"gMSA","b":"Contraseñas de 120+ caracteres, imposibles de crackear."},
        {"h":"Menos privilegios","b":"Una cuenta de servicio nunca debería ser Domain Admin."},
        {"h":"Detección","b":"Evento 4769 con cifrado RC4 = posible ataque."}]},
   ],
   "narration":"Vamos con la defensa, que en ambos casos es muy concreta. Contra el AS-REP Roasting, la medida principal es no desactivar la preautenticación salvo necesidad absoluta, y auditar periódicamente qué cuentas la tienen apagada para corregirlas. Y, como en todo cracking, unas contraseñas fuertes hacen el ataque inútil: si no hay contraseña débil, no hay nada que recuperar. Contra el Kerberoasting, la solución reina son las cuentas gMSA, cuya contraseña de más de cien caracteres generada y rotada por el sistema es, en la práctica, imposible de crackear. Igual de importante es aplicar mínimos privilegios: una cuenta de servicio jamás debería ser administradora de dominio. Y en el lado de la detección, hay una señal valiosísima: el evento cuatro mil setecientos sesenta y nueve, que registra las peticiones de tickets de servicio; cuando llegan muchas usando el cifrado débil RC4, es un indicio claro de Kerberoasting en curso."},

  {"type":"bullets","accent":"cyan","title":"Resumen de la lección",
   "items":[
     {"h":"Solo hace falta una cuenta de dominio","b":"Ambos ataques parten de un usuario sin privilegios."},
     {"h":"AS-REP Roasting","b":"Cuentas sin preautenticación entregan material crackeable."},
     {"h":"Kerberoasting","b":"Cualquiera pide tickets de servicio y crackea la cuenta de servicio."},
     {"h":"Defensa","b":"Preautenticación, gMSA, mínimos privilegios y vigilar RC4 (4769)."},
   ],
   "narration":"Recapitulemos. Lo más importante de estos dos ataques es que parten de una simple cuenta de dominio, sin privilegios. El AS-REP Roasting explota las cuentas que tienen desactivada la preautenticación, obteniendo material cifrado crackeable offline. El Kerberoasting aprovecha que cualquier usuario puede pedir tickets de servicio, que vienen cifrados con el hash de la cuenta de servicio, a menudo con contraseña débil y privilegios altos. La defensa pasa por exigir la preautenticación, usar gMSA, aplicar mínimos privilegios a las cuentas de servicio y vigilar el evento cuatro mil setecientos sesenta y nueve con cifrado RC4. En la próxima lección atacaremos las credenciales directamente, con NTLM, Pass-the-Hash y Pass-the-Ticket. Nos vemos en la lección diez."},
 ]
}
