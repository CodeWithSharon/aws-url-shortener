# AWS URL Shortener

A serverless URL shortener built on AWS with automated CI/CD deployment.

## Architecture
API Gateway → Lambda → DynamoDB

## Tech Stack
- AWS Lambda (Python 3.12)
- Amazon API Gateway
- Amazon DynamoDB
- GitHub Actions (CI/CD)

## How it works
1. Send a POST request with a long URL
2. Lambda generates a short ID and stores it in DynamoDB
3. Returns a shortened URL instantly

## API Usage
POST /url
```json
{
  "long_url": "https://www.example.com"
}
```

Response:
```json
{
  "short_id": "aB3xYz",
  "short_url": "https://short.ly/aB3xYz",
  "long_url": "https://www.example.com"
}
```

## Deployment
Every push to main automatically deploys to AWS Lambda via GitHub Actions.

## Screenshots
### CI/CD Pipeline
![GitHub Actions](screenshots/github-actions.png)

### DynamoDB Items
![DynamoDB](screenshots/dynamodb.png)

### Live API Response
![CloudShell](screenshots/cloudshell.png)
