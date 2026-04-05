
from agent import create_agent
from tools import generate_pdf

if __name__ == "__main__":

    print("\n AI Research Assistant")

agent = create_agent()

while True:
    question = input("\nAsk me anything (or type 'exit'): ").strip()

    if question.lower() == "exit":
        print("Goodbye!")
        break

    if question:
        try:
            print("\n Processing...\n")

            response = agent.invoke({
                "messages": [
                    {
                        "role": "user",
                        "content": question
                    }
                ]
            })
            answer = response["messages"][-1].content[0]["text"]          
            pdf_file = generate_pdf(answer) 
            print(f"\n {pdf_file}")

            

        except Exception as e:
            print(f"\n Error: {e}")


           

p