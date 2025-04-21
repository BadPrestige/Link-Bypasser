<h1 align="center">🔗 Link Bypasser</h1>

## 🧠 Descripción

**Link Bypasser** es una herramienta creada para desenmascarar URLs acortadas, redireccionadas o disfrazadas.  
Permite ver el destino real de un enlace, útil en tareas de análisis de amenazas, OSINT, pentesting o simplemente para evitar trampas.

---

## 🚀 Características

- ✅ Soporte para decenas de acortadores populares y monetizados
- 🔁 Sigue múltiples redirecciones hasta el enlace final
- 🤖 Usa Selenium para sitios que requieren carga dinámica o JavaScript
- 🧠 Detecta si el resultado es **otro** redireccionador y te pregunta si querés continuar
- 📁 Escaneo individual o por lotes desde archivo `.txt`
- 🎨 Interfaz por terminal colorida y profesional
- ⏱️ Muestra tiempo total de escaneo

---

## 📦 Requisitos

Instala las dependencias con:

```bash
pip install -r requirements.txt
```

---

## 🧪 Uso

```bash
python3 link_bypasser.py -u "<URL>"
```

O para múltiples enlaces:

```bash
python3 link_bypasser.py -f lista.txt
```

---

## 📸 Ejemplos visuales

### 🧾 Menú de ayuda

<img src="https://i.ibb.co/d0jgHL36/screenshot-21042025-010925.png" width="800" alt="Menú de ayuda"/>

### ▶️ Ejecución básica

<img src="https://i.ibb.co/gbZ14QrN/screenshot-21042025-010601.png" width="800" alt="Ejemplo de ejecución"/>

---

## 📌 Argumentos

| Parámetro | Descripción                          | Ejemplo                           |
|-----------|--------------------------------------|-----------------------------------|
| `-u`      | URL a desenmascarar                  | `-u "https://bit.ly/3xyz"`        |
| `-f`      | Archivo `.txt` con URLs por línea     | `-f urls.txt`                     |

---

## 🎯 Ejemplo en archivo `.txt`

```
https://shorturl.at/FhBmk [Google.com]
https://shorturl.at/QOnDQ [Twitter.com]
https://shorturl.at/H4tjL [Instagram.com]
```

---

## 📖 Licencia

MIT License
