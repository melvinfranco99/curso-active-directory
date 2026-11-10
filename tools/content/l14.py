# -*- coding: utf-8 -*-
LESSON = {
 "id": "14",
 "module": "Módulo 4 · Defensa",
 "accent": "green",
 "title": "Hardening de Active Directory",
 "slides": [
  {"type":"cover","accent":"green",
   "kicker":"MÓDULO 4 · LECCIÓN 14",
   "title_lines":["Hardening de","Active Directory"],
   "subtitle":"Las medidas concretas que convierten un dominio vulnerable en uno defendible.",
   "footer":"Curso Active Directory · Hacking & Defensa",
   "footer2":"De la teoría de los ataques a las contramedidas prácticas",
   "narration":"Hemos visto cómo se ataca un dominio de principio a fin. Ahora toca blindarlo. En esta lección reunimos, de forma práctica y ordenada, las medidas de hardening que convierten un Active Directory vulnerable en uno defendible. No hay una bala de plata; la seguridad de AD es la suma de muchas decisiones correctas. Vamos a recorrer las más importantes, conectándolas con los ataques concretos que neutralizan."},

  {"type":"table","accent":"green","title":"Cada ataque, su contramedida",
   "lead":"El hardening se entiende mejor como respuesta a amenazas concretas.",
   "headers":["Ataque visto","Contramedida principal"],"weights":[1.2,1.8],
   "rows":[
     ["Kerberoasting","gMSA y mínimos privilegios en cuentas de servicio"],
     ["AS-REP Roasting","Exigir preautenticación; contraseñas fuertes"],
     ["Pass-the-Hash","Credential Guard, LAPS y Tier Model"],
     ["NTLM Relay","Firma de SMB y LDAP; reducir NTLM"],
     ["DCSync","Auditar permisos de replicación; detección"],
     ["Golden Ticket","Proteger y rotar krbtgt; detección de anomalías"],
   ],
   "narration":"La mejor forma de entender el hardening es como una respuesta directa a los ataques que ya conocemos. Contra el Kerberoasting, cuentas gMSA y mínimos privilegios en las cuentas de servicio. Contra el AS-REP Roasting, exigir la preautenticación y usar contraseñas fuertes. Contra Pass-the-Hash, la tríada Credential Guard, LAPS y Tier Model. Contra el NTLM Relay, firmar SMB y LDAP y reducir el uso de NTLM. Contra DCSync, auditar estrictamente quién tiene permisos de replicación y vigilar su uso. Y contra el Golden Ticket, proteger al máximo la cuenta krbtgt, rotarla con regularidad y detectar anomalías en los tickets. Fíjate en que ninguna medida es exótica: son configuraciones y buenas prácticas. El reto no es técnico, es de disciplina y mantenimiento. Vamos a profundizar en las más transversales."},

  {"type":"bullets","accent":"green","title":"LAPS: el fin de la contraseña local compartida",
   "lead":"Una de las medidas con mejor relación esfuerzo-impacto.",
   "items":[
     {"h":"El problema","b":"La misma contraseña de administrador local en miles de equipos."},
     {"h":"La solución","b":"LAPS pone una contraseña única y aleatoria en cada equipo."},
     {"h":"Rotación automática","b":"Se cambia sola cada pocos días y se guarda en AD, protegida."},
     {"h":"El efecto","b":"Pass-the-Hash deja de propagarse: cada equipo es una isla."},
   ],
   "narration":"Detengámonos en LAPS, porque es una de las medidas con mejor relación entre esfuerzo e impacto. El problema que resuelve es clásico y grave: en muchísimas organizaciones, todos los equipos comparten la misma contraseña de administrador local, a menudo heredada de la imagen de instalación. Eso significa que, si un atacante roba ese hash en un solo equipo, puede usarlo en todos los demás con Pass-the-Hash. LAPS acaba con esto: pone en cada equipo una contraseña de administrador local única y aleatoria. Esa contraseña se rota automáticamente cada pocos días y se almacena en Active Directory, protegida de forma que solo quien debe pueda leerla. El efecto es enorme: el Pass-the-Hash deja de propagarse, porque la credencial robada en un equipo no sirve en ningún otro. Cada máquina se convierte en una isla. Si solo pudieras implantar una medida esta semana, LAPS sería una candidata excelente."},

  {"type":"bullets","accent":"green","title":"Proteger las cuentas y credenciales privilegiadas",
   "items":[
     {"h":"PAW","b":"Estaciones de administración dedicadas, sin correo ni navegación."},
     {"h":"Protected Users","b":"Grupo que bloquea NTLM, delegación y cacheo de credenciales."},
     {"h":"Credential Guard","b":"Aísla LSASS con virtualización: frena a Mimikatz."},
     {"h":"Cuentas separadas y MFA","b":"Una cuenta por nivel; segundo factor en los accesos sensibles."},
   ],
   "narration":"El segundo gran pilar es proteger las cuentas y credenciales privilegiadas, que son el objetivo final del atacante. Las PAW, las estaciones de trabajo de acceso privilegiado, son equipos dedicados exclusivamente a tareas de administración, sin correo ni navegación web, de modo que no puedan ser comprometidos por un phishing. El grupo Protected Users es un contenedor especial: las cuentas que metes en él quedan automáticamente protegidas, porque se les bloquea el uso de NTLM, de la delegación y del cacheo de credenciales, cerrando varios vectores a la vez. Credential Guard, que ya mencionamos, usa virtualización por hardware para aislar el proceso LSASS y frenar a Mimikatz. Y, de forma transversal, cuentas separadas por nivel según el Tier Model, reforzadas con autenticación multifactor en los accesos sensibles. Estas medidas, juntas, hacen que robar y reutilizar credenciales privilegiadas pase de ser trivial a ser muy difícil."},

  {"type":"bullets","accent":"green","title":"Higiene continua del directorio",
   "lead":"La seguridad de AD se degrada sola si no se mantiene.",
   "items":[
     {"h":"Revisar grupos privilegiados","b":"¿Quién está en Domain Admins y por qué? Vaciarlos casi siempre."},
     {"h":"Limpiar ACLs y delegaciones","b":"Usar BloodHound en modo defensa para cerrar caminos."},
     {"h":"Eliminar cuentas obsoletas","b":"Usuarios inactivos, SPN innecesarios, confianzas antiguas."},
     {"h":"Parchear y seguir líneas base","b":"Security Baselines de Microsoft y guías CIS."},
   ],
   "narration":"El tercer pilar es la higiene continua, porque la seguridad de Active Directory se degrada sola con el tiempo si nadie la mantiene. Primero, revisa periódicamente los grupos privilegiados: pregúntate quién está en Domain Admins y por qué; lo ideal es que ese grupo esté casi vacío en el día a día y solo se use mediante elevación temporal. Segundo, limpia las ACLs y las delegaciones: usa BloodHound en modo defensivo, igual que lo usaría un atacante, para encontrar y cerrar los caminos de escalada antes que él. Tercero, elimina lo obsoleto: cuentas de usuarios que ya no están, SPN innecesarios, relaciones de confianza antiguas que nadie recuerda. Y cuarto, mantén todo parcheado y aplica líneas base reconocidas, como las Security Baselines de Microsoft o las guías CIS, que endurecen cientos de parámetros con configuraciones probadas. Esta higiene no es glamurosa, pero es exactamente lo que diferencia a un dominio defendible de uno que caerá en la primera auditoría."},

  {"type":"compare","accent":"green","title":"Un plan de hardening por prioridades",
   "cols":[
     {"title":"Primero (alto impacto)","color":"green","items":[
        {"h":"Tier Model y cuentas separadas","b":"Corta la escalada por credenciales."},
        {"h":"LAPS","b":"Elimina la reutilización local."},
        {"h":"Vaciar Domain Admins","b":"Reduce la superficie más crítica."}]},
     {"title":"Después (refuerzo)","color":"amber","items":[
        {"h":"Credential Guard y Protected Users","b":"Blindaje de memoria y cuentas."},
        {"h":"Firma SMB/LDAP, reducir NTLM","b":"Cierra relay y Pass-the-Hash."},
        {"h":"gMSA y limpieza de ACLs","b":"Neutraliza Kerberoasting y caminos ocultos."}]},
   ],
   "narration":"Como todo esto puede abrumar, terminemos con un plan por prioridades, porque no se puede hacer todo a la vez. En la primera oleada, céntrate en lo de mayor impacto estructural: implantar el Tier Model con cuentas separadas, que corta la escalada por credenciales de raíz; desplegar LAPS, que elimina la reutilización local; y vaciar el grupo de administradores de dominio, reduciendo la superficie más crítica. En la segunda oleada, refuerza: activa Credential Guard y usa el grupo Protected Users para blindar la memoria y las cuentas sensibles; exige firma en SMB y LDAP y reduce NTLM para cerrar el relay y Pass-the-Hash; y migra a gMSA mientras limpias las ACLs con BloodHound para neutralizar el Kerberoasting y los caminos ocultos. Avanzar por este orden te da seguridad real desde la primera semana, en lugar de perderte en una lista infinita. La defensa es un proceso, no un proyecto que se termina."},

  {"type":"bullets","accent":"cyan","title":"Resumen de la lección",
   "items":[
     {"h":"Cada ataque tiene su contramedida","b":"El hardening es la respuesta ordenada a amenazas concretas."},
     {"h":"LAPS","b":"Contraseña local única por equipo: fin del Pass-the-Hash masivo."},
     {"h":"Proteger credenciales privilegiadas","b":"PAW, Protected Users, Credential Guard, MFA."},
     {"h":"Higiene continua y prioridades","b":"Vaciar grupos, limpiar ACLs, parchear; empezar por lo de alto impacto."},
   ],
   "narration":"Recapitulemos. El hardening de Active Directory se entiende mejor como la respuesta ordenada a cada ataque concreto que hemos estudiado. LAPS pone una contraseña local única en cada equipo y acaba con el Pass-the-Hash masivo. La protección de las credenciales privilegiadas, con PAW, Protected Users, Credential Guard y MFA, blinda el objetivo final del atacante. Y la higiene continua, vaciar grupos privilegiados, limpiar ACLs y delegaciones, eliminar lo obsoleto y parchear, mantiene la seguridad en el tiempo. Empieza siempre por las medidas de alto impacto estructural. En la última lección cerramos el curso con la otra mitad imprescindible de la defensa: detectar al atacante y responder cuando, pese a todo, logra entrar. Nos vemos en la lección quince."},
 ]
}
