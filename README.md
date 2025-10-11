# 🔐 Cryptography Hash Function Visualization Project

Interactive Streamlit app that explains classic hash-function behaviour through simulations:

- observe the avalanche effect of bit flips,
- watch birthday collisions emerge,
- follow Pollard’s tortoise and hare pointers, and
- demonstrate a Merkle–Damgård length-extension forgery.

The project is tailored for lectures and workshops where quick, visual intuition matters.

---

## 🧰 Tech Stack

| Layer           | Tooling                                                        |
| --------------- | -------------------------------------------------------------- |
| Language        | Python 3.11                                                    |
| UI              | Streamlit + Plotly                                             |
| Data            | pandas, numpy                                                  |
| Core algorithms | `core/` module (toy hash, birthday, pollard, length extension) |

---

## 🚀 Quickstart

1. **Create the environment with `uv`:**
   ```bash
   uv venv .venv
   source .venv/bin/activate
   uv sync
   ```
2. **Launch the visualiser:**
   ```bash
   uv run streamlit run app.py
   ```
3. **Console fallback:** running `uv run python app.py` prints a reminder to use Streamlit.

---

## 🧪 Tests & Quality

- Unit tests mirror the `core/` modules under `tests/core/`.
- Execute the suite with:
  ```bash
  uv run pytest --maxfail=1 --disable-warnings
  ```
- Formatting and linting follow Black and Ruff defaults (see `AGENTS.md`).

---

## 📦 Project Layout

```
app.py                 # Streamlit entry point
core/                  # Simulation logic and toy hash primitives
visualization/         # Streamlit widgets, graphs, and animations
static/demo_data/      # Example data snapshots for quick demos
tests/core/            # Pytest coverage for algorithmic modules
```

Further architectural notes live in [`docs.md`](docs.md).

---

## 📊 Demo Highlights

- **Birthday Attack:** scatter of trials-to-collision plus theoretical curve.
- **Pollard’s Rho:** pointer trajectories and state transition table.
- **Avalanche Test:** flip each input bit and chart output changes.
- **Length Extension:** forge a new digest given an observed tag or known secret.

---

## 🪪 License

MIT License — free for educational and demonstration use.
