# MeidochanTagger manual

El bot funciona para taggear streams en los siguientes canales de texto:

* miu-chat
* lia-chat
* laila-chat
* hana-chat
* piyoko-chat
* hina-chat
* rose-chat
* suzu-chat
* rui-chat
* pal-chat
* luna-chat

## Setup

`!stream <stream URL>` configura manualmente el stream a taggear. Este comando se requiere cada vez que empieza un nuevo stream. No se aceptan URL de streams que no hayan empezado (Sala de espera).

## Tagging

`!t <texto>` crea una timestamp en el stream activo con `<texto>` como descripción. MeidochanTagger reaccionará a la tag con:
- ⭐: Cualquiera puede darle un voto a la tag utilizando esta reacción. 
- ❌: El autor de la tag puede eliminar la tag PERMANENTEMENTE utilizando esta reacción (En caso de duplicados/taggear algo no importante). Quitar la reacción NO devolverá la tag eliminada.

`!adjust <segundos>` ajustará el tiempo de tu última tag la cantidad de segundos especificados. 
  
`!tags` Enlista las tags del stream que se encuentre actualmente configurado en el canal de texto, agregando urls embebidas que pueden ser clickeadas para redirigirse al vídeo de Youtube en el minuto exacto.

`!tags <stream URL>` Enlista las tags del stream proporcionado, agregando urls embebidas en caso de existir tags en la base de datos. Al contrario del resto de comandos que funcionan únicamente dentro de los canales "stream-chat", este comando puede funcionar en otros canales de texto (#stream-tags de preferencia).   

## Comandos para mods/admins

`!offset <posición (segundos)> <cantidad (segundos)>` realizará un desplazamiento de la "cantidad" específicada afectando a todas las tags que se encuentren después del tiempo dado en "posición". La cantidad puede ser negativa.
  
- ❌: Moderadores pueden reaccionar para eliminar la tag de otro usuario PERMANENTEMENTE (En caso de tags indebidas o innecesarias). Quitar la reacción NO devolverá la tag eliminada.

## Documentación completa de todos los comandos

* [!hello](/docs/hello.md)
* [!stream](/docs/stream.md)
* [!t](/docs/t.md)
* [!adjust](/docs/adjust.md)
* [!offset](/docs/offset.md)
* [!tags](/docs/tags.md)
* [!time](/docs/time.md)
* [!find](/docs/find.md)
* [!findall](/docs/findall.md)
* [!movistar](/docs/movistar.md)

## About
Este bot está inspirado en el bot "KoroTagger" de Nyar#3343 y fue programado por Dova#6348.
