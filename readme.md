# 🧠 NLP-Based Text Extractor API

A hybrid NLP-powered Flask API that classifies customer service requests and extracts relevant entities using a combination of **machine learning**, **spaCy NER**, and **regex rules** — deployed on **AWS ECS Fargate** with Swagger documentation.

---

## 🚀 Features & Deployment Status

| Feature                              | Status |
| ------------------------------------ | ------ |
| Flask app with ML model              | ✅ Done |
| Hybrid NLP (spaCy + regex)           | ✅ Done |
| Swagger API documentation            | ✅ Done |
| Containerized with Docker            | ✅ Done |
| Deployed to AWS ECS Fargate          | ✅ Done |
| Public API endpoint (tested)         | ✅ Done |
| Browser-safe `/extract` GET route    | ✅ Done |
| Error handling & Content-Type checks | ✅ Done |

---

## 🧲 How It Works

1. Takes a customer support sentence as input.
2. Classifies it (e.g., `address_change`, `beneficiary_change`).
3. Extracts structured entities like:
   - `new_address`
   - `effective_date`
   - `policy_number`
   - `beneficiary_name`
   - `phone_number`
   - `email`

---

## 📦 Tech Stack

- **Flask** + **scikit-learn** for classification
- **spaCy** custom model for NER
- **Regex** for domain-specific patterns
- **Swagger** (via `flasgger`) for API documentation
- **Docker** for containerization
- **AWS ECS Fargate** for serverless deployment

---

## 🧑‍💻 API Usage

### `POST /extract`

**Request:**

```json
{
  "text": "Please update my address to 123 Main Street effective next month"
}
```

**Response:**

```json
{
  "predicted_class": "address_change",
  "entities": {
    "new_address": "123 Main Street",
    "effective_date": "effective next month"
  }
}
```

### `GET /extract`

Returns a friendly message for browser testing:

```json
{
  "message": "Text Extractor API is running. Use POST method with JSON payload to extract entities."
}
```

---

## 📜 Swagger Documentation

Once deployed, access the auto-generated Swagger docs at:

```
http://<your-public-ip>:5000/apidocs
```

---

## 🐳 Local Development

To run locally:

```bash
docker build -t text-extractor-api .
docker run -p 5000:5000 text-extractor-api
```

Access at: `http://localhost:5000/extract`

---

## ☁️ AWS Deployment

Deployed on **ECS Fargate** using:

- Docker image pushed to **Amazon ECR**
- Task definition referencing ECR image
- Security group opened for port `5000`

To redeploy:

1. Rebuild Docker image
2. Push to ECR
3. Force new deployment in ECS

---

## 💰 Billing Note

> ⚠️ ECS Fargate is **not free** — to avoid charges:

- Set ECS **desired task count = 0** when not in use
- Delete unused services/load balancers

---

---

