# Command Line Interface (CLI)

The GEMINI Command Line Interface (CLI) provides a powerful way to manage and interact with the GEMINI pipeline directly from your terminal. This document outlines the available commands and their usage.

## Main Commands

These commands are used for general management of the GEMINI pipeline.

### `gemini build`

Builds the GEMINI pipeline. This command compiles and prepares all necessary components for deployment.

```bash
gemini build
```

### `gemini start`

Starts the GEMINI pipeline. This will bring up all the services required for GEMINI to operate.

```bash
gemini start
```

### `gemini stop`

Stops the GEMINI pipeline. This will shut down all running GEMINI services.

```bash
gemini stop
```

### `gemini clean`

Cleans the GEMINI pipeline. This command removes temporary files and build artifacts.

```bash
gemini clean
```

### `gemini reset`

Resets the GEMINI pipeline. This command saves current settings and then rebuilds the pipeline, effectively bringing it to a clean, re-initialized state.

```bash
gemini reset
```

### `gemini setup`

Sets up the GEMINI pipeline. This command saves current settings and rebuilds the pipeline.

```bash
gemini setup [--default]
```

**Options:**

*   `--default`: Use default settings for the setup.

### `gemini update`

Updates the GEMINI pipeline. This command pulls the latest changes, saves current settings, and then rebuilds the pipeline.

```bash
gemini update
```

## Settings Commands

These commands are used to manage various configuration settings for the GEMINI pipeline. All settings commands are accessed via `gemini settings <command>`.

### `gemini settings set-local`

Enables or disables local mode for the GEMINI pipeline.

```bash
gemini settings set-local --enable
gemini settings set-local --disable
```

**Options:**

*   `--enable`: Enable local mode.
*   `--disable`: Disable local mode.

### `gemini settings set-debug`

Sets the `GEMINI_DEBUG` flag in the `.env` file.

```bash
gemini settings set-debug --enable
gemini settings set-debug --disable
```

**Options:**

*   `--enable`: Enable debug mode.
*   `--disable`: Disable debug mode.

### `gemini settings set-public-domain`

Sets the `GEMINI_PUBLIC_DOMAIN` in the `.env` file and sets `GEMINI_TYPE` to `public`.

```bash
gemini settings set-public-domain --domain <your-domain.com>
```

**Options:**

*   `--domain <your-domain.com>`: The domain to set for the GEMINI pipeline.

### `gemini settings set-public-ip`

Sets the `GEMINI_PUBLIC_IP` in the `.env` file and sets `GEMINI_TYPE` to `public`.

```bash
gemini settings set-public-ip --ip <your-public-ip>
```

**Options:**

*   `--ip <your-public-ip>`: The public IP address to set for the GEMINI pipeline.
