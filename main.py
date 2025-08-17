# Run the app with Uvicorn
import uvicorn
#It runs the main application file named api.py and binds it to the host 0.0.0.0 on port 8084.
if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8085, reload=True)