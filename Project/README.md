

---

## 📦 Requirements

* Python 3.12.10, may not work with other versions
* Webcam

### Install dependencies

First, set up a virtual environment:

```bash
# Windows PowerShell
python -m venv venv
.\venv\Scripts\Activate
```

Then install the dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ How to Run

```bash
python script.py
```

### Optional:

If you have multiple webcams and want to use a different one, change this line:

```python
cap = cv2.VideoCapture(0)
```

to:

```python
cap = cv2.VideoCapture(1)  # or 2, etc.
```

