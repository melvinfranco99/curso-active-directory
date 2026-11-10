# -*- coding: utf-8 -*-
LESSON = {
 "id": "10",
 "module": "Módulo 3 · Hacking",
 "accent": "red",
 "title": "NTLM, Pass-the-Hash y Pass-the-Ticket",
 "slides": [
  {"type":"cover","accent":"red",
   "kicker":"MÓDULO 3 · LECCIÓN 10",
   "title_lines":["Pass-the-Hash y","Pass-the-Ticket"],
   "subtitle":"Robar y reutilizar credenciales sin conocer jamás la contraseña.",
   "footer":"Curso Active Directory · Hacking & Defensa",
   "footer2":"El motor del movimiento lateral en dominios Windows",
   "narration":"En esta lección atacamos las credenciales directamente. Veremos cómo un atacante roba hashes y tickets de la memoria de un equipo y los reutiliza para hacerse pasar por otros usuarios, sin necesidad de conocer ni una sola contraseña en texto claro. Son las técnicas Pass-the-Hash y Pass-the-Ticket, el auténtico motor del movimiento lateral en Windows. Entenderlas te explicará por qué el Tier Model que vimos antes es tan importante."},

  {"type":"bullets","accent":"red","title":"La raíz del problema: el hash es la credencial",
   "lead":"En Windows, demostrar identidad no siempre exige la contraseña en claro.",
   "items":[
     {"h":"NTLM usa el hash, no la contraseña","b":"Si posees el hash, puedes autenticarte como esa persona."},
     {"h":"Las credenciales quedan en memoria","b":"Cuando alguien inicia sesión, su secreto se cachea en el equipo."},
     {"h":"Un administrador local lo puede leer","b":"Con acceso de SYSTEM se vuelca la memoria del proceso LSASS."},
     {"h":"Reutilización","b":"Ese secreto robado abre otros equipos de la red."},
   ],
   "narration":"La raíz del problema ya la conoces de la lección de NTLM: en Windows, el hash de la contraseña funciona como credencial. Para autenticarte con NTLM no hace falta conocer la contraseña en claro; basta con poseer su hash. A eso se suma un segundo factor: cuando un usuario inicia sesión en un equipo, su secreto, ya sea el hash NTLM o un ticket de Kerberos, queda cacheado en la memoria de esa máquina, concretamente en un proceso llamado LSASS. Y aquí llega el tercer factor: quien tenga privilegios de administrador local en ese equipo, es decir el nivel SYSTEM, puede volcar la memoria de LSASS y extraer esos secretos. El resultado es demoledor: el atacante roba el hash o el ticket de otra persona y lo reutiliza para abrir otros equipos de la red, haciéndose pasar por ella. Esto es, en esencia, el movimiento lateral."},

  {"type":"code","accent":"red","title":"Robo de credenciales con Mimikatz",
   "lead":"Con privilegios de administrador local se vuelcan los secretos de LSASS.",
   "term_title":"PS C:\\ (administrador local)",
   "code":[
     {"k":"ps","t":"mimikatz # privilege::debug"},
     {"k":"good","t":"Privilege '20' OK"},
     {"k":"ps","t":"mimikatz # sekurlsa::logonpasswords"},
     {"k":"out","t":"Usuario   : admin_srv"},
     {"k":"hi","t":"NTLM      : 9f1c...e4d2  (hash robado)"},
     {"k":"out","t":"Usuario   : ana"},
     {"k":"hi","t":"NTLM      : 5a7b...11c0"},
   ],
   "narration":"Veamos el robo en acción con Mimikatz, la herramienta más conocida para esto. Partimos de tener ya privilegios de administrador local en un equipo. Primero ejecutamos privilege dos puntos dos puntos debug, que nos concede el permiso necesario para acceder a la memoria de otros procesos. Después lanzamos sekurlsa dos puntos dos puntos logonpasswords, el comando estrella, que recorre la memoria de LSASS y extrae los secretos de todas las sesiones activas. En la salida vemos credenciales de varios usuarios: por ejemplo admin guion srv, un administrador de servidores que había iniciado sesión en este equipo, con su hash NTLM a la vista. Ese hash es ahora nuestro. Fíjate en lo que acaba de pasar: comprometimos un equipo cualquiera, pero nos llevamos la credencial de un administrador que pasó por allí. Justo el escenario que el modelo de niveles trata de impedir."},

  {"type":"diagram","accent":"red","title":"Pass-the-Hash: reutilizar el hash robado",
   "lead":"Autenticarse en otro equipo presentando el hash, sin la contraseña.",
   "nodes":{
     "att":{"x":120,"y":320,"w":220,"h":80,"label":"Atacante","sub":"tiene el hash de admin_srv","color":"red"},
     "pc2":{"x":540,"y":320,"w":220,"h":80,"label":"Servidor 2","sub":"admin_srv es admin","color":"amber","shape":"cyl"},
     "pwn":{"x":900,"y":320,"w":220,"h":80,"label":"Acceso SYSTEM","sub":"nuevo equipo tomado","color":"purple"},
   },
   "edges":[
     {"from":"att","to":"pc2","color":"red","label":"NTLM auth con el hash"},
     {"from":"pc2","to":"pwn","color":"purple","label":"shell"},
   ],
   "narration":"Con el hash robado en la mano, aplicamos Pass-the-Hash, es decir, pasar el hash. La idea es directa: como NTLM solo necesita el hash para autenticar, el atacante se conecta a otro equipo presentando ese hash en lugar de una contraseña. Si la cuenta robada, admin guion srv, es administradora en ese segundo servidor, el atacante obtiene acceso con los máximos privilegios en una máquina nueva, sin haber conocido jamás la contraseña de admin guion srv. Y una vez dentro de ese segundo servidor, repite la jugada: vuelca su memoria, roba nuevas credenciales, y salta a un tercer equipo. Así es como una única cuenta de administrador, reutilizada en muchos sitios, permite al atacante extenderse por toda la red como una mancha de aceite. Cada salto es un Pass-the-Hash."},

  {"type":"code","accent":"red","title":"Pass-the-Hash y Pass-the-Ticket en la práctica",
   "term_title":"kali@attacker: ~",
   "code":[
     {"k":"cmt","t":"# Pass-the-Hash: autenticarse con el hash NTLM"},
     {"k":"cmd","t":"crackmapexec smb 10.0.0.20 -u admin_srv -H 9f1c...e4d2 -x whoami"},
     {"k":"good","t":"[+] Pwn3d!  nt authority\\system"},
     {"k":"cmt","t":"# Pass-the-Ticket: reutilizar un ticket Kerberos robado"},
     {"k":"cmd","t":"export KRB5CCNAME=ticket.ccache"},
     {"k":"cmd","t":"psexec.py -k -no-pass empresa.local/admin_srv@srv-app"},
     {"k":"good","t":"C:\\Windows\\system32>  (shell como admin_srv)"},
   ],
   "narration":"Veamos las dos variantes con comandos. En Pass-the-Hash, usamos CrackMapExec con la opción mayúscula H para pasar el hash NTLM robado en lugar de la contraseña; si funciona, obtenemos el mensaje Pwned y ejecutamos comandos como SYSTEM en el equipo remoto. La variante hermana es Pass-the-Ticket, pero en lugar de un hash reutilizamos un ticket de Kerberos robado, un TGT o un TGS. Cargamos el ticket en una variable de entorno y luego usamos psexec de Impacket con las opciones de Kerberos y sin contraseña: el sistema acepta el ticket como prueba de identidad y nos da una shell haciéndonos pasar por admin guion srv. La diferencia es sutil pero importante: Pass-the-Hash abusa de NTLM, mientras que Pass-the-Ticket abusa de Kerberos. Ambos logran lo mismo: moverse por la red sin conocer ninguna contraseña."},

  {"type":"diagram","accent":"amber","title":"NTLM Relay: ni siquiera hace falta robar el hash",
   "lead":"Reenviar la autenticación de una víctima a otro servicio en tiempo real.",
   "nodes":{
     "vic":{"x":110,"y":320,"w":190,"h":76,"label":"Víctima","sub":"se autentica","color":"cyan"},
     "att":{"x":470,"y":320,"w":200,"h":76,"label":"Atacante","sub":"intermediario","color":"red"},
     "srv":{"x":860,"y":320,"w":220,"h":80,"label":"Servidor objetivo","sub":"SMB/LDAP sin firma","color":"amber","shape":"cyl"},
   },
   "edges":[
     {"from":"vic","to":"att","color":"cyan","label":"1. autentica (engañada)"},
     {"from":"att","to":"srv","color":"red","label":"2. reenvía la auth"},
     {"from":"srv","to":"att","color":"purple","label":"3. acceso como víctima"},
   ],
   "narration":"Hay una variante aún más astuta que ni siquiera requiere robar y crackear nada: el NTLM Relay. Aquí el atacante se coloca como intermediario. Paso uno: engaña a una víctima para que intente autenticarse contra él, por ejemplo envenenando la resolución de nombres de la red con herramientas como Responder. Paso dos: en lugar de procesar esa autenticación, el atacante la reenvía en tiempo real a un servidor objetivo, haciéndose pasar por la víctima. Paso tres: si ese servidor no exige firma en sus comunicaciones, acepta la autenticación reenviada y le da acceso al atacante con los privilegios de la víctima. El relay es especialmente devastador cuando la víctima es una cuenta de equipo con muchos permisos o un administrador. Por eso una de las mitigaciones más importantes de todo AD es, simplemente, exigir firma en SMB y en LDAP, que rompe este ataque de raíz."},

  {"type":"compare","accent":"green","title":"Defensa contra el robo de credenciales",
   "cols":[
     {"title":"Evitar el robo","color":"green","items":[
        {"h":"Credential Guard","b":"Aísla LSASS con virtualización: Mimikatz no lee los secretos."},
        {"h":"Tier Model","b":"Los admin potentes no pisan equipos de bajo nivel."},
        {"h":"Protected Users / LAPS","b":"Menos credenciales reutilizables en memoria."}]},
     {"title":"Frenar la reutilización","color":"amber","items":[
        {"h":"Firmar SMB y LDAP","b":"Rompe el NTLM Relay."},
        {"h":"Reducir NTLM","b":"Forzar Kerberos y desactivar NTLMv1."},
        {"h":"Segmentar la red","b":"Dificulta saltar de un equipo a otro."}]},
   ],
   "narration":"Veamos cómo defenderse, en dos frentes. Primero, evitar el robo. Credential Guard usa virtualización por hardware para aislar el proceso LSASS, de modo que ni siquiera un administrador local, ni Mimikatz, puede leer los secretos: es una de las mitigaciones más eficaces que existen. El Tier Model, que ya conoces, garantiza que las credenciales potentes no acaben en la memoria de equipos de bajo nivel. Y medidas como el grupo Protected Users o LAPS reducen la cantidad de credenciales reutilizables que quedan expuestas. Segundo frente, frenar la reutilización. Exigir firma en SMB y en LDAP rompe el NTLM Relay. Reducir el uso de NTLM, forzando Kerberos y desactivando la vieja versión uno, cierra Pass-the-Hash en muchos escenarios. Y segmentar la red dificulta que el atacante salte libremente de un equipo a otro. En conjunto, estas medidas convierten el movimiento lateral en algo mucho más difícil y ruidoso."},

  {"type":"bullets","accent":"cyan","title":"Resumen de la lección",
   "items":[
     {"h":"El hash es la credencial","b":"Robar secretos de LSASS permite suplantar a otros."},
     {"h":"Pass-the-Hash","b":"Reutilizar un hash NTLM para abrir otros equipos."},
     {"h":"Pass-the-Ticket","b":"Lo mismo, pero reutilizando tickets de Kerberos."},
     {"h":"NTLM Relay","b":"Reenviar la autenticación de una víctima; se frena firmando SMB/LDAP."},
   ],
   "narration":"Recapitulemos. En Windows, el hash y los tickets funcionan como credenciales, y quedan cacheados en la memoria de cada equipo, de donde un administrador local puede robarlos con herramientas como Mimikatz. Con Pass-the-Hash se reutiliza un hash NTLM robado para autenticarse en otros equipos; con Pass-the-Ticket se hace lo mismo reutilizando tickets de Kerberos. Y el NTLM Relay reenvía en tiempo real la autenticación de una víctima, algo que se frena exigiendo firma en SMB y LDAP. Frente a todo ello, Credential Guard, el Tier Model y la reducción de NTLM son las defensas clave. En la próxima lección conoceremos BloodHound, la herramienta que convierte todos estos permisos y relaciones en un mapa de caminos hacia el control del dominio. Nos vemos en la lección once."},
 ]
}
