from dotenv import load_dotenv

load_dotenv()


from graph.graph import app
from graph.setup.setup_sample_db import vector_store

if __name__ == "__main__":
    print("Welcome to the Graph App!")
    print(app.invoke(input={"question": input("Enter your question: ")}))