# -*- coding: utf-8 -*-
LESSON = {
 "id": "03",
 "module": "Módulo 1 · Fundamentos",
 "accent": "cyan",
 "title": "Protocolos: DNS, LDAP y NTLM",
 "slides": [
  {"type":"cover","accent":"cyan",
   "kicker":"MÓDULO 1 · LECCIÓN 03",
   "title_lines":["DNS, LDAP y NTLM","los protocolos de AD"],
   "subtitle":"Cómo se localiza, se consulta y se autentica en un dominio Windows.",
   "footer":"Curso Active Directory · Hacking & Defensa",
   "footer2":"Los cimientos técnicos sobre los que viven los ataques",
   "narration":"Active Directory no es magia: por debajo funciona gracias a un conjunto de protocolos de red bien conocidos. En esta lección vamos a diseccionar tres de ellos: DNS, que localiza los servicios; LDAP, que consulta el directorio; y NTLM, el protocolo de autenticación heredado. Entenderlos es imprescindible, porque son exactamente los puntos sobre los que se construyen la mayoría de los ataques que veremos más adelante."},

  {"type":"diagram","accent":"green","title":"DNS: cómo un cliente encuentra el dominio",
   "lead":"Sin DNS no hay dominio. Es el primer paso de cada inicio de sesión.",
   "nodes":{
     "cli":{"x":120,"y":320,"w":200,"h":70,"label":"Cliente","sub":"quiere iniciar sesión","color":"cyan"},
     "dns":{"x":470,"y":200,"w":230,"h":70,"label":"Servidor DNS","sub":"registros SRV","color":"green"},
     "dc":{"x":470,"y":420,"w":230,"h":80,"label":"Controlador","sub":"DC localizado","color":"amber","shape":"cyl"},
     "svc":{"x":860,"y":320,"w":240,"h":70,"label":"_ldap._tcp.dc._msdcs","sub":"registro SRV","color":"purple"},
   },
   "edges":[
     {"from":"cli","to":"dns","color":"cyan","label":"¿dónde está el DC?"},
     {"from":"dns","to":"svc","color":"purple","label":"consulta SRV"},
     {"from":"dns","to":"dc","color":"green","label":"aquí: 10.0.0.10"},
     {"from":"cli","to":"dc","color":"amber","dashed":True,"label":"ya puede autenticar"},
   ],
   "narration":"Empecemos por DNS, el sistema de nombres de dominio. En Active Directory, DNS no es opcional: es el GPS sin el cual nada funciona. Veamos qué ocurre cuando un cliente quiere iniciar sesión. Lo primero que hace no es contactar con el controlador, porque todavía no sabe dónde está. Lo que hace es preguntar al servidor DNS: oye, ¿dónde está un controlador para mi dominio? El servidor DNS consulta unos registros especiales llamados registros SRV, con nombres como guion bajo ldap, guion bajo tcp, punto dc, que anuncian qué máquinas ofrecen cada servicio de AD. El DNS devuelve la dirección del controlador y, solo entonces, el cliente puede contactar con él para autenticarse. Por eso, para un atacante, el servidor DNS es una mina de información sobre la topología del dominio."},

  {"type":"table","accent":"green","title":"Registros DNS clave en AD",
   "headers":["Registro","Para qué sirve"],"weights":[1.3,2],"mono_cols":[0],
   "rows":[
     ["_ldap._tcp.dc._msdcs","Localiza controladores de dominio"],
     ["_kerberos._tcp","Localiza el servicio Kerberos (KDC)"],
     ["_gc._tcp","Localiza el catálogo global"],
     ["dominio.local (A)","Resuelve el nombre del dominio a IPs de DC"],
   ],
   "narration":"Conviene conocer los registros DNS más importantes de un dominio. El registro que empieza por guion bajo ldap, guion bajo tcp, punto dc, punto msdcs, localiza los controladores de dominio. El que empieza por guion bajo kerberos localiza el servicio Kerberos, es decir el centro de distribución de claves. El registro guion bajo gc localiza el catálogo global, del que hablaremos en un momento. Y el registro de tipo A del propio nombre del dominio resuelve directamente a las direcciones de los controladores. Un atacante que puede consultar el DNS del dominio obtiene, con una simple petición, un mapa de dónde están las piezas más valiosas de la red. Herramientas de enumeración como nslookup o nmap explotan precisamente estos registros."},

  {"type":"diagram","accent":"blue","title":"LDAP: el idioma del directorio",
   "lead":"El protocolo con el que se leen y escriben los objetos de AD.",
   "nodes":{
     "app":{"x":120,"y":320,"w":210,"h":70,"label":"Cliente LDAP","sub":"PowerShell, ldapsearch","color":"cyan"},
     "dc":{"x":520,"y":320,"w":230,"h":80,"label":"Controlador","sub":"servidor LDAP","color":"amber","shape":"cyl"},
     "q":{"x":470,"y":180,"w":330,"h":58,"label":"(objectClass=user)","sub":"filtro de consulta","color":"purple"},
     "r":{"x":880,"y":320,"w":230,"h":70,"label":"Resultados","sub":"objetos + atributos","color":"green"},
   },
   "edges":[
     {"from":"app","to":"dc","color":"cyan","label":"389 / 636"},
     {"from":"q","to":"dc","color":"purple"},
     {"from":"dc","to":"r","color":"green"},
   ],
   "narration":"El segundo protocolo es LDAP, el protocolo ligero de acceso a directorios. Si DNS es el GPS, LDAP es el idioma con el que se habla con el directorio. Todo lo que AD almacena se consulta y se modifica mediante LDAP. Un cliente, que puede ser PowerShell, la herramienta ldapsearch o una aplicación corporativa, se conecta al controlador por el puerto trescientos ochenta y nueve en claro, o el seiscientos treinta y seis cuando va cifrado. Las consultas se expresan con filtros; por ejemplo, el filtro objectClass igual a user devuelve todos los usuarios. El controlador responde con los objetos que coinciden y sus atributos. Lo crucial desde el punto de vista de seguridad es que, por defecto, cualquier usuario autenticado del dominio puede leer una enorme cantidad de información mediante LDAP. Esa lectura es la base de la enumeración y de herramientas como BloodHound."},

  {"type":"bullets","accent":"green","title":"El catálogo global",
   "items":[
     {"h":"Un índice de todo el bosque","b":"Guarda una copia parcial de todos los objetos de todos los dominios."},
     {"h":"Búsquedas rápidas entre dominios","b":"Permite encontrar un objeto sin saber en qué dominio está."},
     {"h":"Puertos 3268 y 3269","b":"LDAP contra el catálogo global, en claro y cifrado."},
     {"h":"Útil para el atacante","b":"Enumerar el catálogo global revela el bosque completo de una sola vez."},
   ],
   "narration":"Relacionado con LDAP está el catálogo global. Imagina un índice que resume todo el bosque: guarda una copia parcial de todos los objetos de todos los dominios. Gracias a él, una búsqueda puede encontrar a un usuario sin necesidad de saber en qué dominio concreto está almacenado. El catálogo global escucha en los puertos tres mil doscientos sesenta y ocho en claro, y tres mil doscientos sesenta y nueve cifrado. Para un administrador es una herramienta de eficiencia; para un atacante, es un atajo perfecto, porque enumerar el catálogo global le revela de golpe la estructura completa del bosque, no solo la de un dominio. De nuevo vemos el mismo patrón: lo que hace cómoda la administración hace también cómodo el reconocimiento."},

  {"type":"diagram","accent":"red","title":"NTLM: autenticación por reto-respuesta",
   "lead":"El protocolo heredado. Nunca envía la contraseña, pero sí su hash.",
   "nodes":{
     "cli":{"x":120,"y":330,"w":200,"h":70,"label":"Cliente","color":"cyan"},
     "srv":{"x":520,"y":330,"w":200,"h":70,"label":"Servidor","color":"amber"},
     "ch":{"x":320,"y":180,"w":200,"h":56,"label":"Reto (nonce)","color":"purple"},
     "rs":{"x":320,"y":470,"w":260,"h":56,"label":"Respuesta cifrada con hash","color":"red"},
     "dc":{"x":880,"y":330,"w":200,"h":80,"label":"Controlador","sub":"valida","color":"green","shape":"cyl"},
   },
   "edges":[
     {"from":"cli","to":"srv","color":"cyan","label":"1. quiero entrar"},
     {"from":"srv","to":"ch","color":"purple","label":"2. reto"},
     {"from":"cli","to":"rs","color":"red","label":"3. respuesta"},
     {"from":"srv","to":"dc","color":"green","label":"4. ¿es válida?"},
   ],
   "narration":"Llegamos al tercer protocolo: NTLM, el sistema de autenticación heredado, anterior a Kerberos. Aunque es antiguo, sigue activo en casi todas las redes por compatibilidad. Funciona por reto-respuesta, en cuatro pasos. Primero, el cliente le dice al servidor que quiere entrar. Segundo, el servidor le envía un reto, que es un número aleatorio. Tercero, el cliente cifra ese reto usando el hash de su contraseña y devuelve la respuesta. Y cuarto, el servidor le pasa el reto y la respuesta al controlador de dominio, que es quien conoce el hash y verifica si todo cuadra. La idea importante es que la contraseña nunca viaja por la red. Pero fíjate en un detalle enorme: lo que demuestra la identidad no es saber la contraseña, sino poseer su hash. Y de ahí nace su gran debilidad."},

  {"type":"compare","accent":"red","title":"NTLM: por qué es peligroso",
   "cols":[
     {"title":"Debilidad de diseño","color":"red","items":[
        {"h":"El hash es la credencial","b":"Si robas el hash, te autenticas sin la contraseña."},
        {"h":"Pass-the-Hash","b":"Reutilizar un hash NTLM robado en otros sistemas."},
        {"h":"NTLM Relay","b":"Reenviar la autenticación de una víctima a otro servicio."}]},
     {"title":"Qué hacer","color":"green","items":[
        {"h":"Reducir su uso","b":"Forzar Kerberos y auditar dónde se sigue usando NTLM."},
        {"h":"Firmar SMB y LDAP","b":"Mitiga los ataques de relay."},
        {"h":"Vigilar NTLMv1","b":"Desactivar la versión 1, débil, en favor de la 2."}]},
   ],
   "narration":"Veamos por qué NTLM es tan peligroso y cómo se defiende. Su debilidad de diseño es que el hash es, en la práctica, la credencial. Como el cliente demuestra su identidad cifrando con el hash, a un atacante le basta con robar ese hash, sin necesidad de conocer la contraseña en texto claro. De ahí surge el ataque Pass-the-Hash, que consiste en reutilizar un hash NTLM robado para autenticarse en otros sistemas. Y de ahí surge también el NTLM relay, en el que el atacante reenvía la autenticación de una víctima hacia otro servicio, haciéndose pasar por ella. ¿Qué se puede hacer? Reducir el uso de NTLM todo lo posible y forzar Kerberos; firmar las comunicaciones SMB y LDAP para frenar el relay; y desactivar la vieja versión uno de NTLM, aún más débil. Estudiaremos estos ataques en detalle en el módulo de hacking."},

  {"type":"table","accent":"amber","title":"Los puertos que delatan a un DC",
   "lead":"Un escaneo de estos puertos grita: aquí hay un controlador de dominio.",
   "headers":["Puerto","Servicio","Uso"],"weights":[0.7,1.1,1.7],"mono_cols":[0],
   "rows":[
     ["53","DNS","Localización de servicios"],
     ["88","Kerberos","Autenticación por tickets"],
     ["389 / 636","LDAP / LDAPS","Consulta del directorio"],
     ["445","SMB","Ficheros, GPO (SYSVOL) y RPC"],
     ["3268 / 3269","Catálogo global","Búsquedas en todo el bosque"],
   ],
   "narration":"Antes de cerrar, fijémonos en algo muy práctico para la fase de reconocimiento. Un controlador de dominio tiene una huella de puertos abiertos muy característica. El puerto cincuenta y tres es DNS; el ochenta y ocho es Kerberos; el trescientos ochenta y nueve y el seiscientos treinta y seis son LDAP en claro y cifrado; el cuatrocientos cuarenta y cinco es SMB, que sirve ficheros, las GPO a través del recurso SYSVOL y llamadas RPC; y los puertos tres mil doscientos sesenta y ocho y sesenta y nueve son el catálogo global. Cuando un atacante lanza un escaneo con nmap y ve esta combinación de puertos, sabe con casi total certeza que está ante un controlador de dominio. Por eso la segmentación de red y el filtrado de estos servicios son medidas defensivas de primer orden."},

  {"type":"bullets","accent":"cyan","title":"Resumen de la lección",
   "items":[
     {"h":"DNS localiza","b":"Con registros SRV, los clientes encuentran a los DC. Sin él, no hay dominio."},
     {"h":"LDAP consulta","b":"Lee y modifica objetos. Base de toda la enumeración."},
     {"h":"NTLM autentica (heredado)","b":"Reto-respuesta donde el hash es la credencial: Pass-the-Hash y relay."},
     {"h":"La huella de puertos","b":"88, 389, 445, 3268... delatan a un controlador de dominio."},
   ],
   "narration":"Hagamos el resumen. DNS localiza los servicios del dominio mediante registros SRV; sin él, los clientes no encuentran a los controladores. LDAP es el idioma con el que se consulta y se modifica el directorio, y es la base de toda la enumeración. NTLM es el protocolo de autenticación heredado, por reto-respuesta, en el que el hash funciona como credencial, lo que abre la puerta a Pass-the-Hash y a los ataques de relay. Y hemos visto la huella de puertos que delata a un controlador. En la próxima lección nos centraremos en los objetos del directorio: usuarios, grupos, equipos, los SPN y los permisos. Nos vemos en la lección cuatro."},
 ]
}
