from flask import Flask, request

# Initialize the Flask application
app = Flask(__name__)

# Define a dictionary to store messages
message_store = {}

# Route decorator for handling log requests
@app.route("/log", methods=["POST", "GET"])
def handle_log():
  # Check for POST request to log a message
  if request.method == "POST":
    # Extract message id and content from form data
    message_id = request.form.get("id")
    message_content = request.form.get("msg")

    # Validate presence of required data
    if not message_id or not message_content:
      return "Missing required data (id or message)", 400

    # Store the message with the provided id
    message_store[message_id] = message_content

    # Print received message for debugging
    print(f"Received message: {message_content}")

    return "Success"

  # Check for GET request to retrieve messages
  elif request.method == "GET":
    return message_store

  # Handle unsupported methods with a 400 error
  else:
    return "Unsupported request method", 400

# Run the application if executed directly
if __name__ == "__main__":
  app.run(port=5002)
