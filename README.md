# scripts

In this repository, you can find some scripts that can be useful were made on python 3.12 and up versions.

> first I want share a list with comands most used on python, git, conda and scripts python, have a little description in spanish and examples.
> [Comands File](docs/Comands.csv)

The gitignore can use for default in your projects

```bash
# Entornos virtuales
venv/
.env/
*.env

# Compilados de Python
__pycache__/
*.pyc
*.pyo
*.pyd

# Archivos de configuración del sistema operativo
.DS_Store
Thumbs.db

# Archivos de configuración de editores
.vscode/
.idea/

# Carpetas de prueba o de salida
dist/
build/

# Archivos de bases de datos temporales
*.sqlite3

# Logs
*.log

# Configuración de Jupyter
.ipynb_checkpoints/

# Otros
*.bak
*.tmp
```

#### [Script LCM & GCD](docs/mcm_MCD.py)

The script performs the following tasks:

1. Generates Prime Numbers from 1 to n
1. Prime Factorization of a Number
1. Finding the Least Common Multiple (LCM)
1. Finding the Greatest Common Divisor (GCD)

#### [Move your mouse](docs/clic.py)

This script was designed for windows, the idea was to automate some repetitive tasks with your mouse, it has progress bar and some colors, and you can use your clipboard.

#### [Add url to image](docs/mezclarImg.py)

this script allows you to mix images from a URL and a local image.

Functionality:

- The user must enter a web address.
- The script loads a local image named 'url.png' and another local image named 'im.png'.
- Then, it adds the entered web address to the 'url.png' image using the cv2.putText() function.
- Next, resize the 'url.png' and 'im.png' images to have the same minimum width.
- Finally, vertically concatenate the resized images and save the result in a file named 'resized.jpg'.

#### [Copy Headers Email](docs/header_mail.py)

This script opens a file dialog to select an email file, reads its content, and copies the email message
to the clipboard. Displays a temporary label indicating success.

    Steps:
    1. Prompts the user to select an email file with a .eml extension.
    2. Reads the selected file and parses it as an email message.
    3. Copies the email message to the clipboard.
    4. Displays a temporary label in the GUI to confirm the action.

Note:

- Requires the `filedialog`, `email`, `clipboard`, and `Label` modules or classes to be imported.
- The label is automatically destroyed after 3 seconds.

Returns:
None
