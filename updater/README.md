# Actualizador de Torneo AFA para Windows

Este proyecto genera `Actualizador.exe`, un launcher autónomo para Windows
(win-x64) que consulta la última release pública de
`sldanielmarquez-lang/TorneoAFA`.

## Compilar

Se necesita el SDK de .NET 8 o posterior. Desde PowerShell:

```powershell
.\updater\build.ps1
```

El ejecutable queda en `updater\publish\Actualizador.exe`. Copie ese archivo
junto a `TorneoApp.exe` y a `version.txt` dentro de la instalación del juego.
`version.txt` debe contener una versión SemVer compatible con `System.Version`,
por ejemplo `1.2.0`.

## Publicar una actualización

1. Prepare un ZIP para Windows que contenga `TorneoApp.exe` y todos los
   archivos necesarios para ejecutarlo.
2. Cree una GitHub Release en este repositorio con un tag numérico, por ejemplo
   `v1.2.0`, y adjunte el ZIP.
3. Distribuya el nuevo `Actualizador.exe` y el ZIP en la instalación inicial.

El actualizador selecciona el primer asset `.zip` de la última release. Descarga
el archivo a un directorio temporal, valida las rutas del ZIP y extrae antes de
copiar. No reemplaza `Actualizador.exe` mientras está ejecutándose ni
`Torneo_Datos.json`, por lo que las partidas guardadas se conservan. Si una
actualización falla, muestra el error en español e intenta iniciar la versión
local existente.

El ZIP debe incluir `TorneoApp.exe` en su raíz o dentro de una única carpeta
contenedora. No se requieren tokens ni otros secretos: la API y las releases
son públicas.
