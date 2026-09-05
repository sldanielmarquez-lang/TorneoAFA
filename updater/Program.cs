using System.Diagnostics;
using System.IO.Compression;
using System.Net.Http.Headers;
using System.Text.Json;
using System.Windows.Forms;

namespace TorneoAFA.Updater;

internal static class Program
{
    private const string Repository = "sldanielmarquez-lang/TorneoAFA";
    private const string GameExecutable = "TorneoApp.exe";
    private const string UpdaterExecutable = "Actualizador.exe";
    private const string SaveFile = "Torneo_Datos.json";
    private static readonly TimeSpan RequestTimeout = TimeSpan.FromSeconds(30);

    private static async Task<int> Main()
    {
        var installationDirectory = AppContext.BaseDirectory;
        try
        {
            ShowInfo("Buscando actualizaciones...");
            using var client = CreateHttpClient();
            var localVersion = ReadLocalVersion(installationDirectory);
            var release = await GetLatestReleaseAsync(client);

            if (release.Version > localVersion)
            {
                ShowInfo($"Hay una actualización disponible ({release.Version}). Se descargará ahora.");
                await DownloadAndInstallAsync(client, release, installationDirectory);
                WriteLocalVersion(installationDirectory, release.Version);
                ShowInfo($"Actualización {release.Version} instalada correctamente.");
            }
            else
            {
                ShowInfo("El juego ya está actualizado.");
            }

            LaunchGame(installationDirectory);
            return 0;
        }
        catch (Exception exception)
        {
            var message = $"No se pudo actualizar el juego.{Environment.NewLine}{Environment.NewLine}{exception.Message}";
            ShowError(message);

            if (File.Exists(Path.Combine(installationDirectory, GameExecutable)))
            {
                try
                {
                    LaunchGame(installationDirectory);
                    return 0;
                }
                catch (Exception launchException)
                {
                    ShowError($"Tampoco se pudo iniciar el juego.{Environment.NewLine}{Environment.NewLine}{launchException.Message}");
                }
            }

            return 1;
        }
    }

    private static HttpClient CreateHttpClient()
    {
        var client = new HttpClient { Timeout = RequestTimeout };
        client.DefaultRequestHeaders.UserAgent.Add(new ProductInfoHeaderValue("TorneoAFA-Updater", "1.0"));
        client.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/vnd.github+json"));
        return client;
    }

    private static async Task<ReleaseInfo> GetLatestReleaseAsync(HttpClient client)
    {
        using var response = await client.GetAsync(
            $"https://api.github.com/repos/{Repository}/releases/latest",
            HttpCompletionOption.ResponseHeadersRead);
        if (!response.IsSuccessStatusCode)
        {
            throw new InvalidOperationException($"GitHub respondió con {(int)response.StatusCode} ({response.StatusCode}).");
        }

        await using var stream = await response.Content.ReadAsStreamAsync();
        using var document = await JsonDocument.ParseAsync(stream);
        var root = document.RootElement;
        var tag = root.GetProperty("tag_name").GetString() ?? string.Empty;
        if (!TryParseVersion(tag, out var version))
        {
            throw new InvalidDataException($"La versión de la release '{tag}' no es válida.");
        }

        var zipAsset = root.GetProperty("assets")
            .EnumerateArray()
            .FirstOrDefault(asset =>
                (asset.GetProperty("name").GetString() ?? string.Empty)
                .EndsWith(".zip", StringComparison.OrdinalIgnoreCase));
        if (zipAsset.ValueKind == JsonValueKind.Undefined)
        {
            throw new InvalidDataException("La última release no contiene un archivo ZIP.");
        }

        var downloadUrl = zipAsset.GetProperty("browser_download_url").GetString();
        if (string.IsNullOrWhiteSpace(downloadUrl))
        {
            throw new InvalidDataException("El archivo ZIP de la release no tiene una URL de descarga.");
        }

        return new ReleaseInfo(version, downloadUrl);
    }

    private static async Task DownloadAndInstallAsync(HttpClient client, ReleaseInfo release, string installationDirectory)
    {
        var temporaryRoot = Path.Combine(Path.GetTempPath(), "TorneoAFA-Updater", Guid.NewGuid().ToString("N"));
        var archivePath = Path.Combine(temporaryRoot, "release.zip");
        var extractedDirectory = Path.Combine(temporaryRoot, "extracted");
        Directory.CreateDirectory(extractedDirectory);

        try
        {
            using (var response = await client.GetAsync(release.DownloadUrl, HttpCompletionOption.ResponseHeadersRead))
            {
                if (!response.IsSuccessStatusCode)
                {
                    throw new InvalidOperationException($"No se pudo descargar la release ({(int)response.StatusCode}).");
                }

                await using var source = await response.Content.ReadAsStreamAsync();
                await using var target = File.Create(archivePath);
                await source.CopyToAsync(target);
            }

            ExtractZipSafely(archivePath, extractedDirectory);
            var packageRoot = FindPackageRoot(extractedDirectory);
            CopyPackage(packageRoot, installationDirectory);
        }
        finally
        {
            try
            {
                if (Directory.Exists(temporaryRoot))
                {
                    Directory.Delete(temporaryRoot, recursive: true);
                }
            }
            catch
            {
                // La actualización ya terminó; los temporales no afectan al juego.
            }
        }
    }

    private static void ExtractZipSafely(string archivePath, string destination)
    {
        using var archive = ZipFile.OpenRead(archivePath);
        var destinationRoot = Path.GetFullPath(destination) + Path.DirectorySeparatorChar;
        foreach (var entry in archive.Entries)
        {
            var targetPath = Path.GetFullPath(Path.Combine(destination, entry.FullName));
            if (!targetPath.StartsWith(destinationRoot, StringComparison.OrdinalIgnoreCase))
            {
                throw new InvalidDataException("El ZIP contiene una ruta no segura.");
            }

            if (string.IsNullOrEmpty(entry.Name))
            {
                Directory.CreateDirectory(targetPath);
                continue;
            }

            Directory.CreateDirectory(Path.GetDirectoryName(targetPath)!);
            entry.ExtractToFile(targetPath, overwrite: true);
        }
    }

    private static string FindPackageRoot(string extractedDirectory)
    {
        var executable = Directory.EnumerateFiles(extractedDirectory, GameExecutable, SearchOption.AllDirectories)
            .FirstOrDefault();
        if (executable is null)
        {
            throw new InvalidDataException($"El ZIP no contiene {GameExecutable}.");
        }

        return Path.GetDirectoryName(executable)!;
    }

    private static void CopyPackage(string sourceDirectory, string installationDirectory)
    {
        foreach (var directory in Directory.EnumerateDirectories(sourceDirectory, "*", SearchOption.AllDirectories))
        {
            var relativeDirectory = Path.GetRelativePath(sourceDirectory, directory);
            Directory.CreateDirectory(Path.Combine(installationDirectory, relativeDirectory));
        }

        foreach (var sourceFile in Directory.EnumerateFiles(sourceDirectory, "*", SearchOption.AllDirectories))
        {
            var fileName = Path.GetFileName(sourceFile);
            if (fileName.Equals(UpdaterExecutable, StringComparison.OrdinalIgnoreCase)
                || fileName.Equals(SaveFile, StringComparison.OrdinalIgnoreCase))
            {
                continue;
            }

            var relativePath = Path.GetRelativePath(sourceDirectory, sourceFile);
            var destinationPath = Path.Combine(installationDirectory, relativePath);
            Directory.CreateDirectory(Path.GetDirectoryName(destinationPath)!);
            File.Copy(sourceFile, destinationPath, overwrite: true);
        }
    }

    private static Version ReadLocalVersion(string installationDirectory)
    {
        var versionPath = Path.Combine(installationDirectory, "version.txt");
        if (!File.Exists(versionPath))
        {
            return new Version(0, 0, 0);
        }

        var value = File.ReadAllText(versionPath).Trim();
        return TryParseVersion(value, out var version)
            ? version
            : new Version(0, 0, 0);
    }

    private static void WriteLocalVersion(string installationDirectory, Version version)
    {
        File.WriteAllText(Path.Combine(installationDirectory, "version.txt"), version.ToString(3));
    }

    private static bool TryParseVersion(string value, out Version version)
    {
        value = value.Trim();
        if (value.StartsWith('v') || value.StartsWith('V'))
        {
            value = value[1..];
        }

        if (!Version.TryParse(value, out version!))
        {
            return false;
        }

        // Releases and local files use the stable MAJOR.MINOR.PATCH form.
        return version.Revision == -1
            && version.Build >= 0
            && version.Minor >= 0
            && version.Major >= 0;
    }

    private static void LaunchGame(string installationDirectory)
    {
        var gamePath = Path.Combine(installationDirectory, GameExecutable);
        if (!File.Exists(gamePath))
        {
            throw new FileNotFoundException($"No se encontró {GameExecutable}.", gamePath);
        }

        Process.Start(new ProcessStartInfo
        {
            FileName = gamePath,
            WorkingDirectory = installationDirectory,
            UseShellExecute = true
        });
    }

    private static void ShowInfo(string message) =>
        System.Windows.Forms.MessageBox.Show(message, "Torneo AFA", MessageBoxButtons.OK, MessageBoxIcon.Information);

    private static void ShowError(string message) =>
        System.Windows.Forms.MessageBox.Show(message, "Actualizador Torneo AFA", MessageBoxButtons.OK, MessageBoxIcon.Error);

    private sealed record ReleaseInfo(Version Version, string DownloadUrl);
}
