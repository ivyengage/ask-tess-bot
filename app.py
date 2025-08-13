import os
import openai
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from flask import Flask, request
import re

# Initialize Flask app
flask_app = Flask(__name__)

# Initialize Slack app
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

# Initialize OpenAI
openai.api_key = os.environ.get("OPENAI_API_KEY")

handler = SlackRequestHandler(app)

@app.event("app_mention")
def handle_mention(event, say, client):
    """Handle when the bot is mentioned in a channel"""
    
    message = event['text']
    channel = event['channel']
    
    # Remove the bot mention from the message
    clean_message = re.sub(r'<@[A-Z0-9]+>', '', message).strip()
    
    if not clean_message:
        say("Hi! I'm your Benefits Expert. Ask me any questions about benefit plans, coverage limits, or plan details!")
        return
    
    try:
        # Get channel info to determine employer group context
        channel_info = client.conversations_info(channel=channel)
        channel_name = channel_info['channel']['name']
        
        # Determine employer group from channel name
        employer_group = determine_employer_group(channel_name)
        
        # Generate response using GPT-4
        response = generate_benefits_response(clean_message, employer_group)
        
        say(response)
        
    except Exception as e:
        say(f"Sorry, I encountered an error: {str(e)}")

def determine_employer_group(channel_name):
    """Determine employer group from channel name"""
    patterns = [
        r'enrollment[_-]([a-zA-Z0-9]+)',
        r'([a-zA-Z0-9]+)[_-]enrollment',
        r'([a-zA-Z0-9]+)[_-]benefits',
        r'benefits[_-]([a-zA-Z0-9]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, channel_name, re.IGNORECASE)
        if match:
            return match.group(1).title()
    
    return "General"

def generate_benefits_response(question, employer_group):
    """Generate response using GPT-4"""
    
    system_prompt = f"""You are a benefits expert helping an enrollment team. 
    You are currently discussing benefits for: {employer_group}
    
    Provide accurate, helpful responses about:
    - Plan details and coverage limits
    - Benefit definitions and explanations  
    - Coverage scenarios and benefit coordination
    - Plan comparisons and recommendations
    
    Always be professional and cite when you need more specific plan documents to give a complete answer.
    If you're unsure about specific details, recommend checking the actual plan documents."""
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            max_tokens=500,
            temperature=0.3
        )
        
        answer = response.choices[0].message.content
        formatted_response = f"**Benefits Question for {employer_group}:**\n\n{answer}\n\n_💡 For specific plan details, please refer to the current proposal documents._"
        
        return formatted_response
        
    except Exception as e:
        return f"I'm having trouble accessing my knowledge base right now. Please try again in a moment. Error: {str(e)}"

@app.event("message")
def handle_message_events(body, logger):
    """Handle message events (required but we only respond to mentions)"""
    logger.info(body)

@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)

@flask_app.route("/", methods=["GET"])
def health_check():
    return "Ivy Benefits Bot is running!"

if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))

