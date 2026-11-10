# -*- coding: utf-8 -*-
LESSON = {
 "id": "07",
 "module": "Módulo 2 · Administración",
 "accent": "blue",
 "title": "Diseño seguro: Tier Model y mínimos privilegios",
 "slides": [
  {"type":"cover","accent":"blue",
   "kicker":"MÓDULO 2 · LECCIÓN 07",
   "title_lines":["Diseño seguro:","Tier Model"],
   "subtitle":"Cómo estructurar las cuentas y los privilegios para que un ataque no se propague.",
   "footer":"Curso Active Directory · Hacking & Defensa",
   "footer2":"El marco defensivo más importante de todo el curso",
   "narration":"Antes de entrar en el módulo de hacking, necesitamos un marco defensivo claro, porque de nada sirve conocer los ataques si no sabemos cómo se contienen. En esta lección aprenderás el modelo de niveles, el Tier Model de Microsoft, junto con el principio de mínimos privilegios. Son, posiblemente, las ideas defensivas más importantes de todo el curso, porque están diseñadas específicamente para romper la cadena que lleva de un equipo cualquiera al control del dominio."},

  {"type":"bullets","accent":"red","title":"El problema: la escalada por credenciales","lead":"Así se propaga hoy la mayoría de los ataques a AD.",
   "items":[
     {"h":"Un administrador inicia sesión en muchos sitios","b":"Su credencial queda en la memoria de cada equipo donde entra."},
     {"h":"El atacante compromete un equipo normal","b":"Y encuentra allí el token o el hash de un administrador."},
     {"h":"Reutiliza esa credencial","b":"Salta a sistemas más valiosos. Movimiento lateral."},
     {"h":"Llega al controlador","b":"Fin de la partida: control total del dominio."},
   ],
   "narration":"Entendamos primero el problema que el modelo resuelve. En muchas organizaciones, un mismo administrador usa su cuenta potente para todo: entra en su portátil, en los servidores y también en el controlador de dominio. El problema es que, cada vez que un administrador inicia sesión en un equipo, su credencial, en forma de token o de hash, queda almacenada en la memoria de esa máquina. Entonces un atacante compromete un equipo normal y corriente, por ejemplo mediante phishing a un empleado. Rebusca en la memoria y encuentra allí la credencial de un administrador que había entrado a arreglar algo. La reutiliza, salta a sistemas más valiosos, y repitiendo este salto, el movimiento lateral, acaba llegando al controlador de dominio. Fin de la partida. El fallo de raíz es haber mezclado credenciales de distinto valor en los mismos equipos."},

  {"type":"diagram","accent":"blue","title":"La solución: el modelo de tres niveles",
   "lead":"Separar las credenciales por valor e impedir que bajen de nivel.",
   "nodes":{
     "t0":{"x":380,"y":175,"w":500,"h":70,"label":"TIER 0 — Control de la identidad","sub":"DC, AD, ADFS, PKI","color":"red"},
     "t1":{"x":380,"y":320,"w":500,"h":70,"label":"TIER 1 — Servidores y aplicaciones","sub":"datos de negocio","color":"amber"},
     "t2":{"x":380,"y":465,"w":500,"h":70,"label":"TIER 2 — Estaciones de trabajo","sub":"equipos de usuario","color":"green"},
   },
   "edges":[
     {"from":"t0","to":"t1","color":"red","dashed":True,"label":"NO gestiona hacia abajo con cuentas T0"},
     {"from":"t1","to":"t2","color":"amber","dashed":True,"label":"NO baja de nivel"},
   ],
   "narration":"La solución es el modelo de niveles, que divide la infraestructura en tres capas según su valor. El Tier cero, el más crítico, contiene todo lo que controla la identidad: los controladores de dominio, el propio Active Directory, los servidores de federación, la infraestructura de certificados. El Tier uno agrupa los servidores y las aplicaciones que manejan los datos de negocio. Y el Tier dos son las estaciones de trabajo, los equipos de los usuarios. La regla de oro es sencilla pero estricta: una cuenta de un nivel solo puede administrar objetos de su propio nivel, y nunca debe iniciar sesión en un nivel inferior. Es decir, una cuenta de administrador de dominio, que es Tier cero, jamás debe usarse para entrar en un servidor de aplicaciones ni, muchísimo menos, en el portátil de un usuario. Así, aunque el atacante comprometa el Tier dos, no encontrará allí credenciales que le permitan subir."},

  {"type":"table","accent":"amber","title":"Qué cuenta se usa dónde",
   "headers":["Nivel","Qué protege","Cuenta de administración"],"weights":[0.8,1.6,1.4],
   "rows":[
     ["Tier 0","DC, AD, krbtgt, PKI","Admins de dominio (solo en DC)"],
     ["Tier 1","Servidores, bases de datos, apps","Admins de servidores"],
     ["Tier 2","Portátiles y PCs de usuario","Admins de puesto / soporte"],
   ],
   "narration":"Veámoslo en forma de tabla práctica, que es como se aplica en el día a día. En el Tier cero, que protege los controladores, el propio AD, la cuenta krbtgt y la infraestructura de certificados, solo se usan las cuentas de administrador de dominio, y únicamente para iniciar sesión en los controladores. En el Tier uno, que protege los servidores, las bases de datos y las aplicaciones, se usan cuentas específicas de administrador de servidores, distintas de las anteriores. Y en el Tier dos, que protege los portátiles y los equipos de los usuarios, se usan cuentas de administrador de puesto o de soporte, que no tienen ningún poder sobre los niveles superiores. La consecuencia es que cada administrador tiene, en realidad, varias cuentas: una por cada nivel en el que trabaja, más su cuenta normal sin privilegios para el correo y la navegación. Puede parecer incómodo, pero es lo que corta la escalada de raíz."},

  {"type":"bullets","accent":"green","title":"Mínimos privilegios en la práctica",
   "items":[
     {"h":"Cada cuenta, solo lo justo","b":"Ni un permiso más del que necesita para su función."},
     {"h":"Cuentas de administración separadas","b":"Una cuenta normal para el día a día; otra, solo para administrar."},
     {"h":"Grupos en vez de permisos directos","b":"Asigna acceso por grupos y revisa su pertenencia a menudo."},
     {"h":"Acceso Just-In-Time","b":"Privilegios temporales que caducan, en lugar de permanentes."},
   ],
   "narration":"El modelo de niveles se apoya en un principio más general: el de mínimos privilegios, que dice que cada cuenta debe tener solo los permisos justos para su función, ni uno más. En la práctica se traduce en varias reglas. Primera: separa las cuentas de administración de las de uso diario; nadie debería leer el correo ni navegar por Internet con una cuenta que tiene privilegios, porque un solo correo malicioso comprometería esa credencial potente. Segunda: asigna los accesos mediante grupos, no concediendo permisos directamente a cada usuario, y revisa con frecuencia quién está en cada grupo. Y tercera, la más avanzada: usa acceso Just-In-Time, es decir, concede los privilegios de forma temporal y que caduquen solos, en lugar de dejarlos puestos de forma permanente. Así, aunque una cuenta se vea comprometida, su ventana de poder es mínima."},

  {"type":"compare","accent":"blue","title":"Piezas que refuerzan el modelo",
   "cols":[
     {"title":"Protección de credenciales","color":"green","items":[
        {"h":"PAW","b":"Estaciones de administración dedicadas y blindadas."},
        {"h":"Credential Guard","b":"Aísla los secretos para que no se puedan robar de memoria."},
        {"h":"Protected Users","b":"Grupo que limita el uso de credenciales débiles."}]},
     {"title":"Gestión de secretos","color":"amber","items":[
        {"h":"LAPS","b":"Contraseña de administrador local única y rotada por equipo."},
        {"h":"gMSA","b":"Cuentas de servicio con contraseña gestionada automáticamente."},
        {"h":"PIM / PAM","b":"Elevación temporal y auditada de privilegios."}]},
   ],
   "narration":"El Tier Model no va solo: se apoya en varias tecnologías que refuerzan la protección de credenciales y la gestión de secretos, y que estudiaremos en el módulo de defensa. Para proteger las credenciales tenemos las PAW, estaciones de administración dedicadas y blindadas desde las que se hacen las tareas sensibles; Credential Guard, que usa virtualización para aislar los secretos y que no puedan robarse de la memoria; y el grupo Protected Users, que impide que las cuentas sensibles usen mecanismos débiles. Para la gestión de secretos tenemos LAPS, que pone una contraseña de administrador local distinta y rotada en cada equipo, acabando con la plaga de la contraseña única compartida; las gMSA para las cuentas de servicio; y las soluciones PIM o PAM, que elevan los privilegios de forma temporal y auditada. Todas estas piezas encajan alrededor del modelo de niveles como un sistema coherente de defensa."},

  {"type":"quote","accent":"red",
   "text":"Un administrador de dominio que inicia sesión en un portátil cualquiera acaba de regalar el dominio al primer atacante que comprometa ese equipo.",
   "by":"La regla que el Tier Model existe para evitar",
   "narration":"Quiero que te lleves grabada esta idea, porque resume toda la lección: un administrador de dominio que inicia sesión en un portátil cualquiera acaba de regalar el dominio al primer atacante que comprometa ese equipo. Esa única mala práctica, tan común, es la que permite que la mayoría de las intrusiones escalen hasta el control total. El modelo de niveles existe, literalmente, para hacer imposible ese error. Si de todo el módulo de administración solo recuerdas una cosa, que sea esta."},

  {"type":"bullets","accent":"cyan","title":"Resumen de la lección",
   "items":[
     {"h":"El riesgo es la escalada por credenciales","b":"Las credenciales potentes quedan en la memoria de cada equipo."},
     {"h":"Tier Model","b":"Tres niveles; las cuentas nunca bajan de nivel."},
     {"h":"Mínimos privilegios","b":"Cuentas separadas, acceso por grupos y Just-In-Time."},
     {"h":"Tecnologías de apoyo","b":"PAW, LAPS, gMSA, Credential Guard, Protected Users."},
   ],
   "narration":"Resumamos. El gran riesgo de Active Directory es la escalada por credenciales: las cuentas potentes dejan rastro en la memoria de cada equipo donde se usan. El Tier Model lo ataja dividiendo la infraestructura en tres niveles, con una regla estricta de que las cuentas nunca bajan de nivel. Se complementa con el principio de mínimos privilegios, que exige cuentas de administración separadas de las de uso diario, acceso mediante grupos y privilegios temporales. Y se apoya en tecnologías como PAW, LAPS, gMSA, Credential Guard y el grupo Protected Users. Con este marco defensivo en la cabeza, estamos listos para entrar en el módulo de hacking y ver, con los ojos del atacante, exactamente lo que este modelo trata de impedir. Nos vemos en la lección ocho."},
 ]
}
