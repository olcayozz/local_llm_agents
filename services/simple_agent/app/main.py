from dotenv import load_dotenv
import os
load_dotenv()


from graph.graph import app, ROUTER_TYPE

if __name__ == "__main__":
    print("Enter your question:")
    try:
        print("ROUTER:" + os.environ.get("ROUTER_TYPE"))
        print("LOCAL_LLM:" + os.environ.get("LOCAL_LLM"))
        response = app.invoke(input={"question": input("> ")})
        #response = app.invoke(input={"question": "who is olcay ozyilmaz?"})
        print(response["generation"])
        #print(app.invoke(input={"question": "who is olcay ozyilmaz?"}))
    except Exception as e:  
        print(f"An error occurred: {e}")    
