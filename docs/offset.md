# !offset

## Uso únicamente para admins/mods del bot

`!offset <posición (segundos)> <cantidad (segundos)>` realizará un desplazamiento de la "cantidad" específicada afectando a todas las tags que se encuentren después del tiempo dado en "posición". La cantidad puede ser negativa.

**Ejemplo 1: En caso de un stream con la intro recortada**

- La intro termina en el minuto 2 con 12 segundos (total = 132 segundos) y se da inicio al stream:

  ![](/images/offset.png)

- Desplazando todas las tags del stream (tags desde el segundo cero) 132 segundos hacia atrás:

  ![](/images/offset2.png)

**Ejemplo 2: En caso de un stream recortado a la mitad**

- El stream ha sido recortado 238 segundos después del momento 2:22:00, por lo que las tags apartir de "Arigatou  moment" se encuentran con el tiempo incorrecto:

  ![](/images/offset3.png)

- Se desplazan las tags desde el momento 2:22:00 (total = 8520 segundos) 238 segundos hacia atrás:

  ![](/images/offset4.png)

  ![](/images/offset5.png)
