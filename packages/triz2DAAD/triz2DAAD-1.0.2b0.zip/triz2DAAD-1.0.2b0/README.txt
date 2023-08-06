Triz2DAAD
*********

English instructions below!

Triz2DAAD versión 1.0.2b1 191013 (c) 2019 Pedro Fernández

Triz2DAAD es la fusión de los anteriores scripts de Python Triz2sce y Trizio2sce, que cargaban, en cada caso, ficheros procedentes de las utilidades Trizbort y Trizbort.io respectivamente. Este nuevo script carga indistintamente de una o de otra y realiza internamente la conversión necesaria para que un sólo script se puedan manjar ambos formatos.

Triz2DAAD.py es un script de Python 3.x que transforma un fichero generado con la utilidad de escritorio Trizbort (a partir de la versión 1.7.0) o su variante on-line Trizbort.io para mapear aventuras en un código fuente compatible con el compilador del DAAD. No es un diseñador visual de aventuras ni una aplicación para su desarrollo completo. Está concebido como herramienta para hacer prototipos iniciales de aventuras con rapidez y facilidad y, a su vez, como herramienta de apoyo a autores nóveles, ideal para su uso en talleres de aprendizaje.

Uso:
====

Usar "Python triz2DAAD.py -h" en una línea de comandos o powershell para ver las opciones.

El script requiere como argumentos un fichero de entrada (que debe ser un mapa generado por la utilidad Trizbort en formato XML, aunque con la extensión .trizbort,  o por Trizbort.io en formato json) y, opcionalmente, el nombre de un fichero de salida, que será un código fuente en formato .SCE compatible con la versión 2.40-2.42 del compilador del DAAD. Si no se especifica se creará un fichero con el mismo nombre y la extensión .SCE

- La opción -p1 generará un listado SCE con los mensajes del sistema en primera persona. Por defecto éstos se crearán en segunda persona.
- La opción -e generará un listado SCE con los textos y el vocabulario en inglés. Por defecto se crearán en español.
- La opción -md añadirá código (de compilación condicional) para el modo "dibujo invisible" en los Amstrad CPC.
- La opción -dsf generará un fichero DSF compatible con el nuevo compilador DAAD Reborn Compiler.

Enlaces:
========
- Trizbort:

 - http://trizbort.com

- Trizbort.io:

 - http://trizbort.io/

- DAAD

 - http://wiki.caad.es/DAAD
 - http://www.caad.es/fichas/daad.html
 - http://www.rockersuke.com/if/ebbp/
 - http://8-bit.info/infinite-imaginations-aventuras-ad/
 - https://github.com/Utodev/DRC


Hasta el momento parece convertir correctamente:

- Habitaciones, incluyendo sus descripciones y estableciendo la localidad de comienzo.
- Conexiones comunes por puntos cardinales (N,S,E,O,NE,NO,SE,SO).
- Conexiones up/down o in/out.
- Conexiones de una sola dirección.
- Objetos incluidos en las habitaciones.
- Localidades marcadas como "oscuras".

Triz2DAAD añade por su cuenta una barra de estado con el nombre de la localidad actual y el número de turnos transcurridos en la aventura.
También añade un listado automático de salidas y soporte para respuestas por defecto a los comandos "SALIDAS", "MIRAR","EXAMINAR", "AYUDA", "METER", "SACAR" Y "VACIAR". Esto gastará un número variable de mensajes en la sección /MTX y las banderas 100 y 101.

Triz2DAAD usa los textos del cuadro de diálogo "map settings" como pantalla de presentación y créditos (añadiendo frases por defecto en caso de que estuviesen vacíos). Creará un texto por defecto de introducción a la aventura editable en el mensaje nº 14 que en el caso del Trizbort original se corresponderá con el campo "History" (inexistente en Trizbort.io).

A su vez usará el campo "subtitle" de cada localidad como texto para su descripción corta en la barra de estado (máximo 26 caracteres). Si no lo hubiera usará el campo "name" y si éste fuera el elegido por defecto ("Room" o "Cave") lo cambiará por "Localidad xx". A su vez usará el campo "description" para la descripción larga de la localidad en la ventana de texto de la aventura (usando de nuevo un texto por defecto "Descripción localidad xx" si no encontrase ninguno).

Igualmente, triz2DAAD usará el campo "Name" de los objetos como su palabra en el vocabulario. El campo "Description" se usará en los listados de objetos.

- Para Trizbort.io se recomienda usar el mismo nombre con el artículo indeterminado apropiado según género y número para su óptimo procesamiento por el motor del DAAD. Ej: "Libro" -> "Un libro", "Gafas" -> "Unas gafas".
- En el caso de partir del Trizbrt de escritorio se reconocerán los atributos [f] y [2] en el campo "name" como indicadores de "femenino" y "plural" respectivamente (entendiéndose por defecto que el objeto tiene un nombre masculino y singular si no se indica nada) y se añadirá el artículo indeterminado (un, unos, una, unas) correspondiente al texto de los listados.

Siguiendo las convenciones del Trizbort original, Triz2DAAD buscará las cadenas [w] y [c] en el nombre de los objetos para añadirles los atributos ropa y contenedor (tanto en la aplicación de escritorio como en la de web).

Y por el momento triz2DAAD no puede manejarse con:

- Textos personalizados en los extremos de las conexiones.
- Conexiones con puntos intermedios en los espacios del mapa. Cualquier cosa que no sea una conexión directa entre una habitación y otra la ignorará.

Bugs conocidos:
===============

- Debido al comportamiento ligeramente distinto del intérprete inglés, intentar meter un objeto contenedor dentro de sí mismo (o de un objeto inexistente) en una obra inglesa, en lugar de un mensaje de error hace que el jugador deje el objeto en la localidad actual.

- Debido a que los condactos para meter y/o sacar objetos de contenedores usan un único mensaje del sistema, es probable que haya disonancias con el número (singular/plural) del objeto.

HISTORIA
========

- **1.0.2b0**

 - Permite objetos con el mismo nombre (avisando y evitando repetirlo en el vocabulario)

- **1.0.1** 190603

 - Actualizado a la nueva marca de inicio de entrada en formato DSF.
 - Arreglado: los mensajes de 1ª y 2ª persona estaban cambiados en modo DSF en inglés.
 - Arreglado: varios mensajes mal formateados en modo DSF en inglés.

- **1.0** 190501

 - Carga ficheros tanto de Trizbort (aplicación de escritorio) como de Trizbort.io (aplicación web).
 - Opción para exportar a formato DSF del DAAD Reborn Compiler.
 

Triz2DAAD english doc
**********************

Triz2DAAD version 1.0.2b1 191013 (c) 2019 Pedro Fernández

Triz2DAAD is a Python 3.x script that transforms a file generated with either the on-line text-adventure mapping tool Trizbort.io or the Trizbort desktop application into a source code compatible with the DAAD compiler. It's the fussion of former scripts Triz2SCE and Trizio2SCE, admitting both formats.
It's not meant to be either an adventure visual designer or a complete development tool. It's conceived as a fast and easy text-adventure prototyping tool, and also as a supporting tool for novel authors, specially suitable for learning workshops.

Usage:
======

Type "Python triz2DAAD.py -h" in a command line or powershell window to see the options.

The script requires as an argument a file (wwhich must be a map generated with either the Trizbort.io utility in json format or a XML trizbort file generated with the Trizbort desktop application) and, optionally, the name of an output file which will be a SCE formatted source code compatible with version 2.40-2.42 of the DAAD compiler. If it's not specified, a file with the same name and a .SCE extension will be created. 

- Option -p1 will create a SCE listing with first-person system messages. Default is second-person.
- Option -e will create a SCE listing with english texts and vocabulary. Default is spanish.
- Option -md will add some conditional code to support "Invisible string" mode in Amstrad CPC.
- Option -dsf will create a DSF file compatible with the new DAAD Reborn Compiler.

Links:
======

-Trizbort:

 - http://trizbort.com

- Trizbort.io:

 - http://trizbort.io/

- DAAD

 - http://wiki.caad.es/DAAD
 - http://www.caad.es/fichas/daad.html
 - http://www.rockersuke.com/if/ebbp/
 - http://8-bit.info/infinite-imaginations-aventuras-ad/
 - https://github.com/Utodev/DRC

So far it seems to convert correctly:

- Rooms, including descriptions and setting the initial location.
- Common cardinal points connections (N,S,E,W,NE,NW,SE,SW).
- Up/down and in/out connections.
- One way connections
- Objects included in locations.
- Locations labelled as "dark".

Triz2DAAD adds on its own a status line with the current location name and the number of used turns.
It also adds an automatic exits listing and support for default answers to the "EXITS", "LOOK", "EXAMINE", "HELP" AND "EMPTY" commands. This will use a variable amount of messages in the /MTX section and flags 100 and 101.

Triz2DAAD uses the fields in the "map settings" dialogue as an introduction screen and credits (adding default sentences if they were empty). It will create a default adventure introduction text the user can edit at message number 14 (in desktop trizbort it will use the "history" field).

It will also use each location "subtitle" field as a text for its short description at the status line (max. 26 characters). If it wasn't provided it will use the "name" field and if this was the default text ("Room" or "Cave") it will be changed to "Loaction xx". In turn, the "description" field will form the long room description in the adventure text window (again using a default "Location xx description" if there wasn't any).

Equally, Triz2DAAD will use the objects field "name" as its word in the vocabulary. "Description" will be used in the objects listing.

- When importing from Trizbort.io it's highly recommended tu use the same name with an appropriate indefinite article in order to secure an optimized processing by the DAAD engine. Examples: "Book" -> "a book", "trousers" - "some trousers".
- When working from desktop Trizbort [f] (female) and [2] (plural) atributes will be recognized in the name filed (default is male and singular) adding the relevant indefinite articles in the listing texts.

Following original Trizbort standards, Triz2DAAD will search for the [w] and [c] strings inside objects name, giving them wearable and container atributes.

And for the moment Triz2DAAD cannot handle:

- Personalized texts at the connections extremes.
- Connections with intermediate points along the map. Anything other than a direct connection between a room and another will be ignored.

Known bugs:
===========

- Due to the slighty different behavior of the english interpreter, trying to put a container object inside itself (or into a non-existent object) in an english work, instead of displaying an error message will make player drop the object at current location.

- Number (singular/plural) discordances are to be expected due to the fact that putting in and out condacts use just one system message for both cases.

HISTORY
========

- **1.0.2b0**

 - Objects with the same name are now allowed (with a warning and without repeating the name at the VOC section).

- **1.0.1** 190602

 - Updated support for the new ">" mark for new entries in DSF format.
 - FIXED: 2nd and 1st person system messages were swapped in english DSF format.
 - FIXED: bad formatting in several english DSF messages.

- **1.0** 190501

 - Load files from both Trizbort desktop and web applications.
 - Support forr DAAD Reborn Compiler DSF format.