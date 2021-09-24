# !t Tag 

## Uso

`!t <texto>` crea una timestamp en el stream activo con `<texto>` como descripción. MeidochanTagger reaccionará a la tag con:
- ⭐: Cualquiera puede darle un voto a la tag utilizando esta reacción. El número de votos de una tag pueden indicar qué tan útil es: 
  - Tag con pocos votos = Probablemente algo sin importancia.
  - Tag con muchos votos = Algo digno de clip.
- ❌: El autor de la tag puede eliminar la tag PERMANENTEMENTE utilizando esta reacción (Ejemplo: en caso de duplicados/taggear algo no importante). El mensaje se eliminará del chat de discord y no será posible devolver la tag eliminada.

**Ejemplo:**

  ![](/images/t.png)

## Edición de tags

Cuando se edita un mensaje que contiene una tag, la base de datos actualiza la tag automáticamente:

**Ejemplo:**

- Antes de editar:

  ![](/images/edit_before.png)

- Mensaje editado:

  ![](/images/edit_after.png)

- Tag actualizada:

  ![](/images/edit_after2.png)

## Ajustar tiempo en el mismo mensaje

Como medida contra el slowmode de los stream-chat, es posible ajustar el tiempo de una tag en el mismo mensaje utilizando el comando [!adjust](/docs/adjust.md) después de la tag `!t <texto>`. 

**Ejemplo:**

- Tag y adjust en la misma línea:

  ![](/images/t_adjust.png)

- Tag y adjust en el mismo mensaje separados con un *Enter*:

  ![](/images/t_adjust2.png)

El bot reaccionará con ⭐, ❌ y 👍 debido a que es una tag con adjust. Si el bot no reacciona con 👍 es porque la parte de `!adjust` fue mal escrita y el bot tomó todo el texto como tag.

Cuando se edita una tag que contiene `!adjust` en el mismo mensaje, el bot ignora todo lo que vaya después de `!adjust`. Así, editar un tag con `!adjust` no influye en el tiempo ajustado.