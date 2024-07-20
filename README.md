# pdf2png-resizer
This should resize any 1920x1080px .pdf file (or all .pngs and .jpg/jpegs in a folder)
into a 1920x810px set of pngs, and add a "watermark".

### Dependencies
`pip install python-pptx PyMuPDF moviepy pillow`
(or: `pip3 install python-pptx PyMuPDF moviepy pillow`)

**requires:**
- PyMuPDF
- Pillow
- tkinter
- moviepy
- python-pptx
- libreoffice
    - installs based on platform:
        - Win (PS): `choco install libreoffice --confirm`
        - Mac (Homebrew): `brew install libreoffice`
        - Linux/Debian: `sudo apt-get install libreoffice`