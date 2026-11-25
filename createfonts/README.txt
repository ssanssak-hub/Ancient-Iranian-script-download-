Upload BOTH files to:  https://github.com/ssanssak-hub/Ancient-Iranian-script-download-/tree/main/createfonts

  font-studio.zip        : the studio package the app downloads
  fontstudio.meta.json   : version info the app reads (version, size, sha256, notes ...)

Upload them together in the same commit. Whenever you publish a new studio version,
rebuild with tools/FontStudioPackager.java (a higher --version-code) and replace both files.
