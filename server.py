import uvicorn

if __name__ == '__main__':
    uvicorn.run("coacher:app", reload=True)
