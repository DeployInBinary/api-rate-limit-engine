# 🚦 API Rate Limit Engine

A lightweight, extensible rate-limiting engine implemented in Python using a sliding window algorithm.

This project simulates API rate limiting with configurable limits per client and persistent storage using JSON.

---

## ✨ Features

- Sliding window rate limiting
- Per-client configurable limits
- Premium client overrides
- Persistent request history (JSON-based)
- CLI interface
- Modular, testable architecture
- Clean separation of concerns

---

## 🧠 Architecture

The system is divided into:

- `engine.py` → Core rate-limiting logic
- `storage.py` → Persistence layer
- `cli.py` → Command-line interface
- `config.py` → Configuration constants

This structure follows clean architecture principles and makes the engine easy to integrate into:

- REST APIs (FastAPI / Flask)
- Microservices
- Distributed systems (with Redis storage swap)

---

## 🚀 Installation

```bash
git clone https://github.com/DeployInBinary/api-rate-limit-engine.git
cd api-rate-limit-engine
pip install -e .
```

---

## 🖥 Usage

### Simulate Request

```bash
python -m rate_limit_engine.cli request John
```

### Check Status

```bash
python -m rate_limit_engine.cli status John
```

### List Clients

```bash
python -m rate_limit_engine.cli list
```

---

## 📈 Default Limits

| Client Type | Requests / 30s |
|------------|---------------|
| Default    | 5             |
| John       | 10            |
| Terry      | 15            |
| Michael    | 20            |
| Eric       | 30            |

---

## 🔮 Future Improvements

- Redis backend support
- Token bucket implementation
- REST API wrapper
- Docker containerization
- Unit test coverage (pytest)
- GitHub Actions CI pipeline

---

## 📄 License

MIT License
