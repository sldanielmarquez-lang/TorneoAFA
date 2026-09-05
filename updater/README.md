# Actualizador de Torneo AFA para Windows

Este proyecto genera `Actualizador.exe`, un launcher autónomo para Windows
(win-x64) que consulta la última release pública de
`sldanielmarquez-lang/TorneoAFA`.

No hay un proyecto Unity dentro de este repositorio. Por eso, la instalación
de Windows debe abrir siempre `Actualizador.exe`, nunca `TorneoApp.exe`
directamente. Al iniciarse muestra “Buscando actualizaciones”, consulta GitHub,
actualiza si encuentra una versión mayor y recién después inicia el juego.

## Compilar

Se necesita el SDK de .NET 8 o posterior. Desde PowerShell:

```powershell
.\updater\build.ps1
```

El ejecutable queda en `updater\publish\Actualizador.exe`. Copie ese archivo
junto a `TorneoApp.exe` y a `version.txt` dentro de la instalación del juego.
`version.txt` y los tags de GitHub deben usar exactamente `MAJOR.MINOR.PATCH`,
con un prefijo `v` opcional en el tag; por ejemplo, `version.txt` puede
contener `1.2.0` y la release debe usar `v1.2.0`.

## Publicar una actualización

1. Prepare un ZIP para Windows que contenga `TorneoApp.exe`, `version.txt` con
   la misma versión de la release y todos los archivos necesarios para
   ejecutarlo. El ejecutable puede estar en la raíz o dentro de una única
   carpeta contenedora.
2. Cree una GitHub Release en este repositorio con un tag como `v1.2.0` y
   adjunte ese ZIP como asset.
3. Para la instalación inicial, distribuya `Actualizador.exe`, el contenido
   del ZIP y `version.txt` en la misma carpeta.

El actualizador selecciona el primer asset `.zip` de la última release. Descarga
el archivo a un directorio temporal, valida las rutas del ZIP y extrae antes de
copiar. No reemplaza `Actualizador.exe` mientras está ejecutándose ni
`Torneo_Datos.json`, por lo que las partidas guardadas se conservan. Si una
actualización falla, muestra el error en español e intenta iniciar la versión
local existente.

El instalador conserva el `Torneo_Datos.json` local aunque el ZIP contenga uno,
y nunca reemplaza el `Actualizador.exe` que está ejecutándose. No se requieren
tokens ni otros secretos: la API y las releases son públicas.
