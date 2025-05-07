from dotenv import load_dotenv

load_dotenv()


from graph.setup.setup_sample_db import vector_store
from graph.graph import app

if __name__ == "__main__":
    print("Enter your question:")
    try:
        response = app.invoke(input={"question": input("> ")})
        #response = app.invoke(input={"question": "who is olcay ozyilmaz?"})
        print(response["generation"])
        #print(app.invoke(input={"question": "who is olcay ozyilmaz?"}))
    except Exception as e:  
        print(f"An error occurred: {e}")    
