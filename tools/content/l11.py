# -*- coding: utf-8 -*-
LESSON = {
 "id": "11",
 "module": "Módulo 3 · Hacking",
 "accent": "red",
 "title": "BloodHound y abuso de ACLs y delegación",
 "slides": [
  {"type":"cover","accent":"red",
   "kicker":"MÓDULO 3 · LECCIÓN 11",
   "title_lines":["BloodHound y","abuso de ACLs"],
   "subtitle":"Convertir miles de permisos en un mapa de caminos hacia Domain Admin.",
   "footer":"Curso Active Directory · Hacking & Defensa",
   "footer2":"La herramienta que cambió el pentesting de Active Directory",
   "narration":"En esta lección conocemos BloodHound, la herramienta que revolucionó el hacking de Active Directory. Su idea es brillante: en lugar de mirar los permisos uno a uno, los representa todos como un grafo y encuentra automáticamente el camino más corto desde cualquier usuario comprometido hasta el administrador de dominio. Veremos cómo funciona y cómo se abusan los permisos y las delegaciones que descubre. Entender BloodHound es entender cómo piensan hoy tanto los atacantes como los equipos de defensa."},

  {"type":"bullets","accent":"amber","title":"La idea: pensar en grafos",
   "lead":"AD es, en el fondo, una red de relaciones. BloodHound la hace visible.",
   "items":[
     {"h":"Nodos","b":"Usuarios, grupos, equipos, OU, GPO y dominios."},
     {"h":"Aristas","b":"Relaciones: miembro de, administra, puede resetear, controla..."},
     {"h":"El problema del defensor","b":"Nadie puede revisar a mano millones de relaciones."},
     {"h":"La ventaja del atacante","b":"Un algoritmo encuentra el camino más corto al poder."},
   ],
   "narration":"La idea central de BloodHound es pensar en grafos. Active Directory es, en el fondo, una enorme red de relaciones, y un grafo es la forma natural de representarla. Los nodos son los objetos: usuarios, grupos, equipos, unidades organizativas, GPO y dominios. Las aristas son las relaciones entre ellos: es miembro de, es administrador de, puede resetear la contraseña de, tiene control total sobre, y muchas más. Aquí aparece la asimetría fundamental de la seguridad en AD: para un defensor es imposible revisar a mano los millones de relaciones que existen en un dominio real, así que los caminos peligrosos quedan ocultos. Para el atacante, en cambio, basta con aplicar un algoritmo de grafos, como el del camino más corto, para que la herramienta le señale la ruta exacta desde la cuenta que ya controla hasta el administrador de dominio. BloodHound automatiza algo que el ojo humano no puede abarcar."},

  {"type":"diagram","accent":"red","title":"Un camino de ataque típico",
   "lead":"Cada flecha es un permiso real que el atacante puede abusar.",
   "nodes":{
     "u":{"x":90,"y":320,"w":170,"h":66,"label":"ana@","sub":"ya comprometida","color":"cyan"},
     "g1":{"x":300,"y":320,"w":170,"h":66,"label":"Soporte TI","sub":"grupo","color":"green"},
     "u2":{"x":510,"y":320,"w":180,"h":66,"label":"carlos@","sub":"reset pwd","color":"amber"},
     "g2":{"x":730,"y":320,"w":180,"h":66,"label":"Admins SRV","color":"amber"},
     "da":{"x":960,"y":310,"w":180,"h":86,"label":"Domain Admins","color":"red","shape":"cyl"},
   },
   "edges":[
     {"from":"u","to":"g1","color":"green","label":"MemberOf"},
     {"from":"g1","to":"u2","color":"amber","label":"ForceChangePwd"},
     {"from":"u2","to":"g2","color":"amber","label":"MemberOf"},
     {"from":"g2","to":"da","color":"red","label":"AdminTo → DCSync"},
   ],
   "narration":"Veamos un camino de ataque típico, como lo dibujaría BloodHound. Partimos de la cuenta de Ana, que ya hemos comprometido. BloodHound nos muestra que Ana es miembro del grupo de soporte. Ese grupo, por un permiso mal puesto, tiene derecho a forzar el cambio de contraseña de Carlos. Así que el atacante resetea la contraseña de Carlos y se hace pasar por él. Resulta que Carlos es miembro del grupo de administradores de servidores. Y ese grupo tiene permisos que, en última instancia, permiten ejecutar un DCSync y hacerse con las credenciales del dominio. Fíjate en lo importante: cada flecha de este grafo es un permiso perfectamente legítimo, configurado por algún administrador en algún momento. Ninguno es un fallo de software. El ataque consiste simplemente en encadenarlos. Y BloodHound encontró esta cadena de cuatro saltos en milisegundos, algo imposible de ver revisando permisos a mano."},

  {"type":"code","accent":"amber","title":"Recolección y análisis con BloodHound",
   "term_title":"kali@attacker: ~",
   "code":[
     {"k":"cmt","t":"# Recolectar el grafo desde Linux, con una cuenta de dominio"},
     {"k":"cmd","t":"bloodhound-python -d empresa.local -u ana -p 'Passw0rd' -c All -ns 10.0.0.10"},
     {"k":"good","t":"Compressing output into bloodhound.zip"},
     {"k":"cmt","t":"# Cargar el ZIP en la GUI y lanzar consultas"},
     {"k":"out","t":"Query: Shortest Paths to Domain Admins"},
     {"k":"hi","t":"ana -> SOPORTE_TI -> carlos -> ADMINS_SRV -> DOMAIN ADMINS"},
     {"k":"out","t":"Query: Find Kerberoastable Users -> svc_sql, svc_web"},
   ],
   "narration":"Veamos el flujo de trabajo. Primero, la recolección: con la utilidad bloodhound guion python, desde nuestra máquina Linux y usando una cuenta de dominio cualquiera, recorremos el directorio y comprimimos todo el grafo en un fichero ZIP. Esta recolección consulta usuarios, grupos, sesiones activas, permisos y confianzas. Segundo, el análisis: cargamos ese ZIP en la interfaz gráfica de BloodHound y lanzamos consultas predefinidas. La consulta estrella es caminos más cortos hacia administradores de dominio, que nos dibuja exactamente la ruta que vimos antes. Pero hay muchas más: encontrar usuarios kerberoasteables, que nos lista svc guion sql y svc guion web; encontrar cuentas con sesiones en equipos sensibles; o analizar las relaciones de confianza entre dominios. En pocos minutos, el atacante pasa de no conocer el dominio a tener un plano detallado de cómo conquistarlo. Por eso los equipos de defensa usan también BloodHound, para encontrar y cerrar esos caminos antes que el adversario."},

  {"type":"table","accent":"red","title":"Abuso de permisos (ACLs)",
   "lead":"Cada permiso peligroso tiene una técnica de abuso concreta.",
   "headers":["Permiso","Cómo se abusa"],"weights":[1.1,2],"mono_cols":[0],
   "rows":[
     ["ForceChangePassword","Resetear la contraseña y suplantar a la víctima"],
     ["GenericAll / GenericWrite","Añadir un SPN y kerberoastear, o cambiar atributos"],
     ["WriteDacl","Concederse a uno mismo control total"],
     ["AddMember","Meterse en un grupo privilegiado"],
     ["WriteOwner","Hacerse dueño del objeto y luego reescribir su ACL"],
   ],
   "narration":"Profundicemos en el abuso de ACLs, el corazón de estos caminos. Cada permiso peligroso tiene su técnica concreta. Con ForceChangePassword, reseteas la contraseña de la víctima y la suplantas directamente. Con GenericWrite sobre un usuario, puedes añadirle un SPN y kerberoastearlo, o modificar otros atributos a tu favor. WriteDacl es de los más potentes: te permite reescribir los permisos del objeto, así que te concedes a ti mismo control total. Con AddMember, te añades a un grupo privilegiado. Y con WriteOwner te conviertes en el dueño del objeto, lo que a su vez te deja reescribir su ACL. El patrón es siempre el mismo: un permiso que parecía menor, concedido por comodidad administrativa, se convierte en un escalón. BloodHound no solo encuentra estos permisos, sino que en sus notas te explica cómo abusar de cada uno. Por eso es tan importante que los defensores auditen y limpien estas ACLs."},

  {"type":"compare","accent":"amber","title":"Delegación de Kerberos: el otro gran abuso",
   "cols":[
     {"title":"Tipos de delegación","color":"red","items":[
        {"h":"No restringida (unconstrained)","b":"El servicio guarda el TGT de quien le visita. Muy peligrosa."},
        {"h":"Restringida (constrained)","b":"Limitada a ciertos servicios, pero abusable."},
        {"h":"Basada en recursos (RBCD)","b":"Abuso muy común si puedes escribir en una cuenta de equipo."}]},
     {"title":"Defensa","color":"green","items":[
        {"h":"Evitar la no restringida","b":"Marcar cuentas sensibles como 'no delegables'."},
        {"h":"Protected Users","b":"Impide delegar las credenciales del grupo."},
        {"h":"Auditar atributos","b":"Revisar quién puede delegar y hacia qué."}]},
   ],
   "narration":"El otro gran abuso que revela BloodHound es la delegación de Kerberos. La delegación es una función legítima que permite que un servicio actúe en nombre de un usuario; por ejemplo, un servidor web que accede a una base de datos como si fuera el usuario conectado. El problema es cómo está configurada. La delegación no restringida es la más peligrosa: el servicio guarda el TGT completo de cualquiera que lo visite, de modo que si comprometes ese servidor, puedes robar los TGT de los usuarios que han pasado por él, incluidos administradores. La delegación restringida limita a qué servicios se puede delegar, pero sigue siendo abusable. Y la delegación basada en recursos, la RBCD, es un vector muy común cuando el atacante consigue escribir en una cuenta de equipo. La defensa pasa por evitar la delegación no restringida, marcar las cuentas sensibles como no delegables, usar el grupo Protected Users y auditar quién puede delegar y hacia dónde."},

  {"type":"bullets","accent":"cyan","title":"Resumen de la lección",
   "items":[
     {"h":"AD es un grafo","b":"Nodos y relaciones; los caminos peligrosos están ocultos a simple vista."},
     {"h":"BloodHound los revela","b":"Encuentra automáticamente la ruta hasta Domain Admin."},
     {"h":"Abuso de ACLs","b":"ForceChangePassword, WriteDacl, GenericAll... escalones de privilegio."},
     {"h":"Delegación de Kerberos","b":"Mal configurada, permite suplantar usuarios y robar TGT."},
   ],
   "narration":"Recapitulemos. Active Directory es, en esencia, un grafo de relaciones en el que los caminos hacia el poder quedan ocultos a simple vista. BloodHound los revela, encontrando de forma automática la ruta más corta desde una cuenta comprometida hasta el administrador de dominio. Esos caminos se componen de abusos de ACLs, como ForceChangePassword, WriteDacl o GenericAll, cada uno un escalón de privilegio nacido de un permiso mal puesto; y de abusos de la delegación de Kerberos, que mal configurada permite suplantar usuarios y robar sus tickets. La lección para el defensor es clara: usa tú también BloodHound para encontrar y cerrar estos caminos antes que el atacante. En la próxima lección veremos cómo se materializan el movimiento lateral y la escalada que estos caminos describen. Nos vemos en la lección doce."},
 ]
}
