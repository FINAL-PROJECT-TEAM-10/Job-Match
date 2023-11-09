from fastapi import FastAPI




app = FastAPI(title='Job_Match', description='to be continued')


if __name__ == "__main__":
    import uvicorn
    uvicorn.run('main:app', host="127.0.0.1", port=8000, reload=True)