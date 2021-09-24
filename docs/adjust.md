# !adjust

## Uso

`!adjust <segundos>` ajustará el tiempo de tu última tag la cantidad de segundos especificados. El bot reaccionará con 👍 para indicar que el tiempo de la tag se ajustó exitosamente. 
La cantidad puede ser positiva (Ej: `!ajust 5` la tag se ubicará 5 segundos después del tiempo en el que fue declarada) o negativa (Ej: `!ajust -15` la tag se ubicará 15 segundos antes). 

**Ejemplo:**

- Creación de una tag:

  ![](/images/adjust.png)

- Ajuste del tiempo:

  ![](/images/adjust2.png)

No es posible ajustar el tiempo de tags de otros usuarios o de tags anteriores propias. 

El tiempo transcurrido entre la tag y el comando `!adjust` no afecta el tiempo ajustado, es decir, no hay diferencia entre usar `!adjust -15` al instante o hacerlo 5 minutos después, la tag se ajustará con 15 segundos menos. 

## Ajustar tiempo en el mismo mensaje

Como medida contra el slowmode de los stream-chat, es posible ajustar el tiempo de una tag en el mismo mensaje utilizando el comando `!adjust` después de la tag `!t <texto>`. 

**Ejemplo:**

- Tag y adjust en la misma línea:

  ![](/images/t_adjust.png)

- Tag y adjust en el mismo mensaje separados con un *Enter*:

  ![](/images/t_adjust2.png)

El bot reaccionará con ⭐, ❌ y 👍 debido a que es una tag con adjust. Si el bot no reacciona con 👍 es porque la parte de `!adjust` fue mal escrita y el bot tomó todo el texto como tag.

Cuando se edita una tag que contiene `!adjust` en el mismo mensaje, el bot ignora todo lo que vaya después de `!adjust`. Así, editar un tag con `!adjust` no influye en el tiempo ajustado.