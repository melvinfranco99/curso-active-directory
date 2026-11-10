# -*- coding: utf-8 -*-
LESSON = {
 "id": "01",
 "module": "Módulo 1 · Fundamentos",
 "accent": "cyan",
 "title": "¿Qué es Active Directory?",
 "slides": [

  {"type":"cover","accent":"cyan",
   "kicker":"MÓDULO 1 · LECCIÓN 01",
   "title_lines":["¿Qué es","Active Directory?"],
   "subtitle":"Arquitectura, componentes y por qué es el corazón de casi todas las empresas del mundo.",
   "footer":"Curso Active Directory · Hacking & Defensa",
   "footer2":"Fundamentos para administradores y profesionales de seguridad",
   "narration":"Bienvenido al curso de Active Directory, hacking y defensa. En esta primera lección vamos a responder a una pregunta aparentemente sencilla pero fundamental: ¿qué es exactamente Active Directory? Lo entenderemos desde cero, veremos sus componentes y descubriremos por qué es, al mismo tiempo, la pieza más importante de la infraestructura de una empresa y el principal objetivo de cualquier atacante."},

  {"type":"bullets","accent":"cyan","title":"Lo que aprenderás en esta lección",
   "lead":"Una base sólida antes de entrar en administración, ataques y defensa.",
   "items":[
     {"h":"Qué es y para qué sirve un directorio","b":"La idea de identidad centralizada y por qué cambió la gestión de redes."},
     {"h":"Los componentes esenciales","b":"Controladores de dominio, dominios, bosques, objetos y esquema."},
     {"h":"Los protocolos que lo sostienen","b":"DNS, LDAP, Kerberos y NTLM, que veremos en detalle más adelante."},
     {"h":"La perspectiva del atacante","b":"Por qué comprometer el dominio equivale a comprometer toda la empresa."},
   ],
   "narration":"Antes de empezar, este es el mapa de la lección. Primero entenderemos qué es un directorio y la idea de identidad centralizada, que transformó por completo la forma de administrar redes. Después veremos los componentes esenciales: los controladores de dominio, los dominios, los bosques, los objetos y el esquema. Mencionaremos los protocolos que lo hacen funcionar, como DNS, LDAP, Kerberos y NTLM, que estudiaremos en profundidad en lecciones posteriores. Y, muy importante, empezaremos a mirar Active Directory con los ojos de un atacante, porque entender para qué sirve es también entender por qué es el gran premio de cualquier intrusión."},

  {"type":"bullets","accent":"cyan","title":"La idea central: un directorio de identidades",
   "lead":"Imagina la guía telefónica de una empresa, pero viva y con permisos.",
   "items":[
     {"h":"Un lugar único donde vive todo","b":"Usuarios, contraseñas, equipos, impresoras, grupos y permisos, centralizados."},
     {"h":"Una sola identidad para todo","b":"El empleado inicia sesión una vez y accede a los recursos autorizados de la red."},
     {"h":"Administración a escala","b":"Un administrador gestiona diez mil equipos con la misma facilidad que uno solo."},
   ],
   "narration":"La idea central de Active Directory es la de un directorio. Piensa en la guía telefónica de una empresa, pero una guía viva, que además guarda permisos. En lugar de que cada ordenador tenga su propia lista de usuarios y contraseñas, existe un lugar único y central donde vive todo: los usuarios, sus contraseñas, los equipos, las impresoras, los grupos y los permisos. Gracias a eso, un empleado tiene una sola identidad: inicia sesión una vez y accede a todos los recursos para los que está autorizado. Y un administrador puede gestionar diez mil ordenadores con casi la misma facilidad con la que gestionaría uno solo. Esa centralización es, en una frase, el motivo por el que Active Directory existe."},

  {"type":"bullets","accent":"cyan","title":"Definición y servicios que ofrece",
   "lead":"Active Directory es el servicio de directorio de Microsoft para redes Windows.",
   "items":[
     {"h":"Autenticación","b":"Verifica quién eres cuando inicias sesión o accedes a un recurso."},
     {"h":"Autorización","b":"Decide a qué tienes derecho a acceder una vez identificado."},
     {"h":"Directorio y búsqueda","b":"Permite localizar objetos: usuarios, grupos, equipos, servicios."},
     {"h":"Gestión de políticas","b":"Aplica configuración y seguridad de forma masiva mediante GPO."},
   ],
   "narration":"Pongámosle una definición formal. Active Directory es el servicio de directorio de Microsoft para redes Windows, introducido con Windows 2000 y presente hoy en prácticamente todas las organizaciones. Ofrece cuatro grandes servicios. El primero es la autenticación: verificar quién eres cuando inicias sesión o accedes a un recurso. El segundo es la autorización: decidir, una vez que sabe quién eres, a qué tienes derecho a acceder. El tercero es el propio directorio: permite localizar y consultar objetos, como usuarios, grupos, equipos o servicios. Y el cuarto es la gestión de políticas, que aplica configuración y medidas de seguridad de forma masiva mediante las directivas de grupo, las famosas GPO. Autenticar, autorizar, localizar y administrar: esas son sus cuatro funciones."},

  {"type":"stat","accent":"cyan","title":"Por qué importa tanto",
   "cards":[
     {"big":"~90%","h":"de las empresas","b":"usan Active Directory como directorio de identidades principal.","color":"cyan"},
     {"big":"1 brecha","h":"casi siempre toca AD","b":"el directorio es el objetivo final de la mayoría de ataques dirigidos.","color":"red"},
     {"big":"25 años","h":"de legado","b":"compatibilidad histórica que arrastra decisiones de seguridad delicadas.","color":"amber"},
   ],
   "narration":"¿Por qué le dedicamos un curso entero? Por su alcance. Se estima que alrededor del noventa por ciento de las empresas del mundo usan Active Directory como su directorio de identidades principal. Eso significa que, cuando ocurre una brecha de seguridad dirigida, casi siempre acaba pasando por el directorio: es el objetivo final del atacante. Y hay un factor añadido: Active Directory arrastra unos veinticinco años de compatibilidad histórica. Esa herencia es muy valiosa para que todo siga funcionando, pero también mantiene vivos protocolos y configuraciones antiguas que, como veremos, abren la puerta a muchos ataques."},

  {"type":"diagram","accent":"cyan","title":"Componentes esenciales de un dominio",
   "lead":"El controlador de dominio es el cerebro; la base de datos NTDS, su memoria.",
   "nodes":{
     "dc":{"x":520,"y":200,"w":240,"h":90,"label":"Controlador de Dominio","sub":"(DC)","color":"amber","shape":"cyl"},
     "ntds":{"x":540,"y":360,"w":200,"h":70,"label":"NTDS.dit","sub":"Base de datos de AD","color":"purple"},
     "u":{"x":180,"y":200,"w":200,"h":64,"label":"Usuarios","sub":"empleados","color":"cyan"},
     "pc":{"x":180,"y":330,"w":200,"h":64,"label":"Equipos","sub":"estaciones y servidores","color":"cyan"},
     "gpo":{"x":900,"y":200,"w":200,"h":64,"label":"GPO","sub":"políticas","color":"green"},
     "dns":{"x":900,"y":330,"w":200,"h":64,"label":"DNS","sub":"localización","color":"green"},
   },
   "edges":[
     {"from":"dc","to":"ntds","color":"purple","label":"guarda"},
     {"from":"u","to":"dc","color":"cyan","label":"autentica"},
     {"from":"pc","to":"dc","color":"cyan","label":"se une"},
     {"from":"dc","to":"gpo","color":"green","label":"aplica"},
     {"from":"dc","to":"dns","color":"green","label":"usa"},
   ],
   "narration":"Veamos las piezas sobre un diagrama. En el centro está el controlador de dominio, abreviado DC. Es el cerebro del sistema: un servidor Windows que ejecuta los servicios de directorio y atiende todas las peticiones de autenticación. Dentro del controlador vive su memoria: un fichero llamado NTDS punto dit, la base de datos de Active Directory, donde se almacenan todos los objetos y, muy importante, los hashes de las contraseñas. A su alrededor giran los demás elementos: los usuarios, que se autentican contra el DC; los equipos, que se unen al dominio y quedan bajo su control; las GPO, que el controlador distribuye para aplicar políticas; y el servicio DNS, que todos usan para localizar al propio controlador. Memoriza esta imagen, porque todo lo demás encaja sobre ella."},

  {"type":"table","accent":"cyan","title":"Objetos: los habitantes del directorio",
   "lead":"Casi todo en AD es un objeto con atributos.",
   "headers":["Objeto","Qué representa","Ejemplo"],"weights":[1,1.5,1.2],
   "rows":[
     ["Usuario","Una identidad que inicia sesión","ana.lopez"],
     ["Equipo","Una máquina unida al dominio","PC-VENTAS-07$"],
     ["Grupo","Un conjunto para asignar permisos","Domain Admins"],
     ["OU","Un contenedor para organizar y aplicar GPO","OU=RRHH"],
     ["GPO","Un conjunto de ajustes de configuración","Política de contraseñas"],
   ],
   "narration":"Dentro del directorio, casi todo es un objeto, y cada objeto tiene atributos, como su nombre, su descripción o su contraseña. Vamos a conocer a sus habitantes principales. Un usuario representa una identidad que inicia sesión, por ejemplo ana punto lopez. Un equipo representa una máquina unida al dominio; fíjate en que su nombre termina en el símbolo del dólar. Un grupo es un conjunto que sirve para asignar permisos de golpe a muchas identidades; el grupo más peligroso de todos es Domain Admins, los administradores del dominio. Una unidad organizativa, u o u, es un contenedor para organizar objetos y aplicarles políticas. Y una GPO es, como ya vimos, un conjunto de ajustes de configuración. Estos cinco tipos de objeto son el vocabulario básico que usaremos durante todo el curso."},

  {"type":"diagram","accent":"purple","title":"Dominio, árbol y bosque",
   "lead":"La estructura lógica que agrupa y delimita la administración.",
   "nodes":{
     "forest":{"x":470,"y":175,"w":330,"h":58,"label":"Bosque (Forest)","sub":"frontera de seguridad","color":"purple","shape":"hex"},
     "tree":{"x":500,"y":290,"w":270,"h":56,"label":"Árbol (Tree)","sub":"dominios con dns contiguo","color":"blue"},
     "d1":{"x":250,"y":420,"w":240,"h":70,"label":"empresa.com","sub":"dominio raíz","color":"cyan"},
     "d2":{"x":560,"y":420,"w":250,"h":70,"label":"ventas.empresa.com","sub":"subdominio","color":"cyan"},
     "d3":{"x":880,"y":420,"w":240,"h":70,"label":"filial.net","sub":"otro árbol","color":"green"},
   },
   "edges":[
     {"from":"forest","to":"tree","color":"purple"},
     {"from":"tree","to":"d1","color":"blue"},
     {"from":"tree","to":"d2","color":"blue"},
     {"from":"forest","to":"d3","color":"green","dashed":True,"label":"confianza"},
   ],
   "narration":"Los dominios no viven aislados: se agrupan en estructuras más grandes. El dominio es la unidad básica de administración y replicación, por ejemplo empresa punto com. Cuando varios dominios comparten un espacio de nombres continuo, como empresa punto com y ventas punto empresa punto com, forman un árbol. Y el contenedor que engloba uno o varios árboles se llama bosque. Quédate con esta idea, porque es crucial para la seguridad: el bosque, no el dominio, es la verdadera frontera de seguridad en Active Directory. Dentro de un mismo bosque los dominios confían entre sí de forma automática, de modo que comprometer un solo dominio puede, en muchos casos, abrir el camino hacia todo el bosque."},

  {"type":"table","accent":"cyan","title":"Estructura lógica frente a estructura física",
   "lead":"AD separa cómo organizas los objetos de dónde están realmente las máquinas.",
   "headers":["Estructura lógica","Estructura física"],"weights":[1,1],
   "rows":[
     ["Bosques, árboles y dominios","Controladores de dominio (servidores)"],
     ["Unidades organizativas (OU)","Sitios (ubicaciones de red)"],
     ["Usuarios, grupos y objetos","Enlaces y replicación entre sitios"],
     ["Pensada para administrar y delegar","Pensada para rendimiento y disponibilidad"],
   ],
   "narration":"Un punto que suele confundir al principio: Active Directory tiene dos estructuras paralelas. La estructura lógica describe cómo organizas los objetos para administrarlos: bosques, árboles, dominios, unidades organizativas y los propios usuarios y grupos. No depende de dónde estén físicamente las máquinas. La estructura física, en cambio, describe el mundo real: los servidores que actúan como controladores de dominio, los sitios que representan ubicaciones de red, y los enlaces por los que se replica la información entre ellos. En resumen: la estructura lógica está pensada para administrar y delegar, y la física para el rendimiento y la disponibilidad. Las dos conviven y es importante no mezclarlas."},

  {"type":"compare","accent":"amber","title":"Los dos protocolos de autenticación",
   "cols":[
     {"title":"Kerberos","color":"green","items":[
        {"h":"El método moderno y por defecto","b":"Basado en tickets emitidos por el controlador de dominio."},
        {"h":"No envía la contraseña por la red","b":"Más seguro, pero con ataques propios como Kerberoasting."}]},
     {"title":"NTLM","color":"red","items":[
        {"h":"El método heredado","b":"Sistema de reto-respuesta anterior a Kerberos."},
        {"h":"Sigue activo por compatibilidad","b":"Vulnerable a Pass-the-Hash y relay. Un objetivo clásico."}]},
   ],
   "narration":"¿Cómo demuestra un usuario que es quien dice ser? Mediante uno de dos protocolos de autenticación. El moderno, y el que se usa por defecto, es Kerberos. Funciona con tickets que emite el controlador de dominio y tiene una gran virtud: nunca envía la contraseña por la red. Aun así, como veremos, tiene ataques propios, como el Kerberoasting. El otro protocolo es NTLM, el método heredado, un sistema de reto-respuesta anterior a Kerberos. Sigue activo en casi todas las redes por compatibilidad, y es el responsable de ataques clásicos como Pass-the-Hash y los ataques de relay. Toda la parte ofensiva del curso girará, en buena medida, alrededor de estos dos protocolos y de sus debilidades."},

  {"type":"bullets","accent":"green","title":"DNS y LDAP: localizar y consultar",
   "items":[
     {"h":"DNS: el GPS del dominio","b":"Sin DNS, los clientes no encuentran al controlador. AD depende por completo de él."},
     {"h":"Registros SRV","b":"Entradas especiales de DNS que anuncian dónde están los servicios de AD."},
     {"h":"LDAP: el idioma del directorio","b":"El protocolo con el que se consultan y modifican los objetos del directorio."},
     {"h":"Puerto 389 y 636","b":"LDAP en claro y LDAP sobre TLS. La enumeración empieza casi siempre aquí."},
   ],
   "narration":"Dos protocolos más completan el cuadro. El primero es DNS, que funciona como el GPS del dominio. Es tan importante que, sin DNS, los clientes simplemente no encuentran al controlador de dominio y nada funciona. Active Directory publica unos registros especiales, llamados registros SRV, que anuncian dónde están sus servicios. El segundo protocolo es LDAP, que podemos ver como el idioma del directorio: es el mecanismo con el que se consultan y se modifican los objetos. LDAP escucha en el puerto trescientos ochenta y nueve en claro, y en el seiscientos treinta y seis cuando va cifrado sobre TLS. Recuerda LDAP, porque la fase de enumeración de casi cualquier ataque, en la que el intruso cartografía el dominio, empieza precisamente haciendo consultas LDAP."},

  {"type":"diagram","accent":"red","title":"La perspectiva del atacante",
   "lead":"El objetivo final siempre es el mismo: el controlador de dominio.",
   "nodes":{
     "a":{"x":120,"y":300,"w":200,"h":66,"label":"Phishing","sub":"acceso inicial","color":"red"},
     "b":{"x":380,"y":300,"w":200,"h":66,"label":"Credenciales","sub":"robo y reutilización","color":"red"},
     "c":{"x":640,"y":300,"w":210,"h":66,"label":"Movimiento lateral","sub":"de equipo a equipo","color":"amber"},
     "d":{"x":920,"y":280,"w":210,"h":100,"label":"Domain Admin","sub":"control total del dominio","color":"purple","shape":"cyl"},
   },
   "edges":[
     {"from":"a","to":"b","color":"red"},
     {"from":"b","to":"c","color":"amber"},
     {"from":"c","to":"d","color":"purple","label":"meta"},
   ],
   "narration":"Pongámonos ahora en el lado ofensivo, que es el hilo conductor del curso. Un ataque a Active Directory sigue casi siempre el mismo recorrido. Todo empieza con un acceso inicial, normalmente mediante phishing, que le da al atacante el control de un equipo cualquiera. Desde ahí, el intruso roba credenciales y las reutiliza. Con esas credenciales salta de un equipo a otro, lo que llamamos movimiento lateral, recolectando por el camino identidades cada vez más privilegiadas. Y el destino es siempre el mismo: convertirse en administrador del dominio y tomar el control total. La defensa, por tanto, no consiste en levantar un único muro, sino en romper esta cadena en cada uno de sus eslabones. Ese será nuestro marco mental durante todo el curso."},

  {"type":"bullets","accent":"amber","title":"Tu laboratorio para practicar",
   "lead":"Nunca practiques ataques fuera de un entorno controlado y autorizado.",
   "items":[
     {"h":"Un controlador de dominio","b":"Windows Server con el rol de AD DS. Será tu DC de pruebas."},
     {"h":"Una o dos máquinas cliente","b":"Windows 10 u 11 unidas al dominio, como víctimas."},
     {"h":"Una máquina atacante","b":"Kali o Parrot con Impacket, BloodHound, CrackMapExec y Mimikatz."},
     {"h":"Todo aislado","b":"Red privada, sin salida a producción. La ética y la ley primero."},
   ],
   "narration":"Para que este curso te sirva de verdad, necesitas un laboratorio donde practicar sin romper nada ni meterte en problemas legales. El montaje mínimo es sencillo. Necesitas un controlador de dominio, que es un Windows Server con el rol de servicios de dominio instalado. Una o dos máquinas cliente, con Windows diez u once, unidas a ese dominio, que harán de víctimas. Y una máquina atacante, típicamente Kali o Parrot, con herramientas como Impacket, BloodHound, CrackMapExec y Mimikatz, que iremos usando. Y una regla de oro, innegociable: todo debe estar aislado en una red privada, sin conexión con sistemas reales de producción. Las técnicas que aprenderás solo deben usarse en entornos propios o con autorización explícita por escrito. La ética y la ley van primero, siempre."},

  {"type":"bullets","accent":"cyan","title":"Resumen de la lección",
   "items":[
     {"h":"AD es un directorio de identidades","b":"Centraliza autenticación, autorización y administración en redes Windows."},
     {"h":"El DC es el cerebro","b":"Guarda la base de datos NTDS con todos los objetos y los hashes."},
     {"h":"Dominio, árbol y bosque","b":"El bosque es la verdadera frontera de seguridad."},
     {"h":"Kerberos, NTLM, DNS y LDAP","b":"Los protocolos que estudiaremos a fondo y que concentran los ataques."},
   ],
   "narration":"Hagamos un resumen de lo aprendido. Active Directory es un directorio de identidades que centraliza la autenticación, la autorización y la administración en las redes Windows. Su pieza central es el controlador de dominio, que guarda la base de datos NTDS con todos los objetos y los hashes de las contraseñas. Los objetos se organizan en dominios, árboles y bosques, y recuerda que el bosque es la verdadera frontera de seguridad. Y todo se sostiene sobre cuatro protocolos: Kerberos y NTLM para autenticar, DNS para localizar y LDAP para consultar. En torno a ellos giran la mayoría de los ataques."},

  {"type":"quote","accent":"cyan",
   "text":"Quien controla Active Directory controla la organización entera: cada equipo, cada dato y cada usuario.",
   "by":"Principio fundamental de la seguridad en dominios Windows",
   "narration":"Quiero que te lleves una frase de esta lección: quien controla Active Directory controla la organización entera, cada equipo, cada dato y cada usuario. Por eso dominar cómo funciona por dentro no es un lujo técnico, sino la base imprescindible tanto para administrarlo bien como para defenderlo. En la próxima lección bajaremos un nivel y desmenuzaremos los dominios, los árboles, los bosques y las unidades organizativas, para que entiendas con precisión cómo se diseña la estructura de una empresa real. Nos vemos en la lección dos."},
 ]
}
