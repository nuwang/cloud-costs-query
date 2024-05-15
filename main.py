from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from google.cloud import bigquery
from google.cloud.bigquery import QueryJobConfig

app = FastAPI()

# Mount the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", include_in_schema=False)
async def root():
    with open("static/index.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)


@app.get("/runtime_90th_percentile/")
async def query_runtime_90th_percentile(tool_name: str):
    client = bigquery.Client()

    query = f"""
    SELECT APPROX_QUANTILES(runtime_seconds, 100)[OFFSET(90)] AS runtime_90th_percentile
    FROM `anvil-cost-modeling.cost_info.job_metrics`
    WHERE tool_id = @tool_name
    """
    
    job_config = QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("tool_name", "STRING", tool_name)
        ]
    )

    job = client.query(query, job_config=job_config)

    while not job.done():
        await asyncio.sleep(1)

    results = job.result()
    runtime_90th_percentile = None

    for row in results:
        runtime_90th_percentile = row.runtime_90th_percentile

    if runtime_90th_percentile is None:
        raise HTTPException(status_code=404, detail=f"No data found for tool: {tool_name}")

    return {"tool_name": tool_name, "90th_percentile_runtime_seconds": runtime_90th_percentile}
