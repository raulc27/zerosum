# ZeroSum

<p>
Just a simple python <b>api</b> for stock basic requests
</p>

## endpoints:

<p> /genai/resume_market</p>
<p> /genai/resume_ticker/:TICKER.sa</p>
<p> /brapi/sync_quote_list</p>
<p> /brapi/async_quote/:TICKER.sa</p>
<p> /brapi/sync_quote/:TICKER.sa</p>


## Execute it with docker:
<code>
docker pull raulc27/zerosum
</code>

<p> <a href="https://hub.docker.com/r/raulc27/zerosum">https://hub.docker.com/r/raulc27/zerosum</a></p>

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file or deployment environment:

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `GENAI_API_KEY` | API key for Google Generative AI features | Yes | - |
| `BRAPI_TOKEN` | Token for accessing Brapi.dev API | Yes | - |
| `CLIENT_API_KEY` | Secret key to authenticate clients accessing this API | Yes | - |
| `CORS_ORIGIN` | Allowed origin for CORS | No | `*` |

### Setting up variables

You can create a `.env` file in the root directory:

```bash
GENAI_API_KEY=your_genai_key
BRAPI_TOKEN=your_brapi_token
CLIENT_API_KEY=your_client_secret_key
CORS_ORIGIN=http://localhost:3000
```

Or export them in your terminal:

```bash
export GENAI_API_KEY=your_genai_key
export BRAPI_TOKEN=your_brapi_token
export CLIENT_API_KEY=your_client_secret_key
```
