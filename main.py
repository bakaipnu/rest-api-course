from rest_course import app


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", port=8080, reload=True)
