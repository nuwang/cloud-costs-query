from fastapi import FastAPI, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html
from google.cloud import bigquery
from google.cloud.bigquery import QueryJobConfig

app = FastAPI()

@app.get("/", include_in_schema=False)
async def root():
    return get_swagger_ui_html(openapi_url=app.openapi_url, title=app.title + " - Swagger UI")

@app.get("/runtime_90th_percentile/")
async def query_runtime_90th_percentile(tool_name: str):
    client = bigquery.Client()

    query = f"""
    SELECT APPROX_QUANTILES(runtime_seconds, 100)[OFFSET(90)] AS runtime_90th_percentile
    FROM `anvil_cost_modeling.cost_info.job_metrics`
    WHERE tool_id = @tool_name
    """
    
    job_config = QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("tool_name", "STRING", tool_name)
        ]
    )

    job = client.query(query, job_config=job_config)

    results = await job.result()
    runtime_90th_percentile = None

    for row in results:
        runtime_90th_percentile = row.runtime_90th_percentile

    if runtime_90th_percentile is None:
        raise HTTPException(status_code=404, detail=f"No data found for tool: {tool_name}")

    return {"tool_name": tool_name, "90th_percentile_runtime_seconds": runtime_90th_percentile}
