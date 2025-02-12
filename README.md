# ZeroSum

<p>
Just a simple python <b>api</b> for stock basic requests
</p>

## endpoints:

<p> /genai/resume_market</p>
<p> /genai/resume_ticker/:TICKER.sa</p>
<p> /ticker/:TICKER.sa</p>
<p> /ticker/cashflow/:TICKER.sa</p>
<p> /ticker/fundamentals/:TICKER.sa</p>


## Execute it with docker:
<code>
docker pull raulc27/zerosum
</code>

<p> <a href="https://hub.docker.com/r/raulc27/zerosum">https://hub.docker.com/r/raulc27/zerosum</a></p>

## GenAI Credentials
<p>
GenAi endpoints to work properly, you should have set the GENAI_API_KEY. 
You may use a .env or... set this environment variable in your deployment tool.
</p>

<p>
The last try is once you have your container running, enter in your terminal:
<code>
export GENAI_API_KEY=YOUR_API_KEY
</code>
dont forget to restart the api (not the container...)
</p>
