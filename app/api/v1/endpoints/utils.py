from typing import List
from fastapi.responses import JSONResponse, StreamingResponse
from io import BytesIO, StringIO
import pandas as pd

def export_documents_data(results: List[dict], format: str):
    if format == "json":
        return JSONResponse(content=results)

    df = pd.json_normalize(results)

    if format == "csv":
        stream = StringIO()
        df.to_csv(stream, index=False)
        stream.seek(0)
        return StreamingResponse(stream, media_type="text/csv", headers={
            "Content-Disposition": f"attachment; filename=documents.csv"
        })

    elif format == "excel":
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)
        output.seek(0)
        return StreamingResponse(output, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={
            "Content-Disposition": f"attachment; filename=documents.xlsx"
        })

    else:
        raise HTTPException(status_code=400, detail="Invalid format. Use json, csv, or excel.")
