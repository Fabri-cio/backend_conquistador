import polib
import os

# Ruta del archivo .po
po_path = os.path.join('locale', 'en', 'LC_MESSAGES', 'django.po')
# Ruta de salida del archivo .mo
mo_path = os.path.join('locale', 'en', 'LC_MESSAGES', 'django.mo')

# Abrir y compilar
po = polib.pofile(po_path)
po.save_as_mofile(mo_path)

print("✔ Traducción compilada a .mo correctamente.")
