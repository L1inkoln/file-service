from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.api.files import router as files_router


app = FastAPI(
    title="File Manager API",
    description="API for managing files with streaming support for large files",
    version="1.0.0",
)

app.include_router(files_router)


@app.get("/")
async def root():
    """Корневая страница с информацией об API"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>File Manager API</title>
        <style>
            body { font-family: Arial, sans-serif; line-height: 1.6; margin: 2rem; }
            h1 { color: #333; }
            ul { list-style-type: none; padding: 0; }
            li { margin-bottom: 0.5rem; }
            a { color: #007bff; text-decoration: none; }
            a:hover { text-decoration: underline; }
            .container { max-width: 800px; margin: 0 auto; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>File Manager API</h1>
            <p>This API provides file management capabilities with support for large file streaming.</p>
            <h2>API Documentation</h2>
            <ul>
                <li><a href="/docs">Swagger UI</a> - Interactive API documentation</li>
                <li><a href="/redoc">ReDoc</a> - Alternative documentation</li>
            </ul>
            <h2>Available Endpoints</h2>
            <ul>
                <li><strong>POST /files/</strong> - Upload a file</li>
                <li><strong>POST /files/multiple/</strong> - Upload multiple files</li>
                <li><strong>GET /files/</strong> - List all files</li>
                <li><strong>GET /files/{filename}</strong> - Download a file</li>
                <li><strong>DELETE /files/{filename}</strong> - Delete a file</li>
            </ul>
            <h2>Features</h2>
            <ul>
                <li>Streaming support for large files</li>
                <li>File validation</li>
                <li>Async I/O operations</li>
            </ul>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
