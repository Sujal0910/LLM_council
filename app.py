import os
import concurrent.futures
from flask import Flask, render_template, request
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    default_headers={
        "HTTP-Referer": "http://localhost:5000",
        "X-Title": "Human Council"
    }
)


# THE COUNCIL MEMBERS 
COUNCIL = [
    {
        "id": "meta-llama/llama-3.3-70b-instruct:free",
        "name": "Llama 3.3 (The Chairman)",
        "role": "Leader",
        "color": "primary", 
        "icon": "🦁",
        "prompt": "You are the Chairman. You are authoritative, intelligent, and structured. Give a comprehensive answer."
    },
    {
        "id": "x-ai/grok-4.1-fast:free",
        "name": "Grok 4.1",
        "role": "Rebel",
        "color": "dark",
        "icon": "🚀",
        "prompt": "You are a maverick. You hate boring, standard answers. Provide unique, out-of-the-box thinking."
    },
    {
        "id": "tngtech/deepseek-r1t2-chimera:free",
        "name": "DeepSeek Chimera",
        "role": "Engineer",
        "color": "info",
        "icon": "🔧",
        "prompt": "You are a pragmatic engineer. Focus on how things actually work, technical specs, and efficiency."
    },
    {
        # REPLACED GEMINI WITH ARCEE TRINITY MINI
        "id": "arcee-ai/trinity-mini:free",
        "name": "Trinity Mini",
        "role": "Academic",
        "color": "success",
        "icon": "📚",
        "prompt": "You are an academic researcher. Focus on facts, history, and established knowledge."
    }
]

# HELPER FUNCTION 
def talk_to_ai(model_id, system_instruction, user_message):
    try:
        # FIX: Removed 'headers=' from here. It is now handled automatically.
        response = client.chat.completions.create(
            model=model_id,
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_message}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error with {model_id}: {e}")
        return f"Model Error: {str(e)}"

# MAIN ROUTE
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        user_query = request.form.get('query')
        
        drafts = []
        critiques = []
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            
            # === PHASE 1: DRAFTING ===
            future_to_member = {}
            for member in COUNCIL:
                task = executor.submit(talk_to_ai, member['id'], member['prompt'], user_query)
                future_to_member[task] = member
            
            for future in concurrent.futures.as_completed(future_to_member):
                member = future_to_member[future]
                drafts.append({
                    "name": member['name'],
                    "color": member['color'],
                    "icon": member['icon'],
                    "text": future.result()
                })

            # PHASE 2: PEER REVIEW 
            transcript = "Here are the proposed answers from your colleagues:\n\n"
            for i, draft in enumerate(drafts):
                transcript += f"--- Candidate {i+1} ({draft['name']}) ---\n{draft['text']}\n\n"
            
            critique_instruction = "You are a harsh reviewer. Find mistakes, bias, or hallucinations in these answers. Be brief."
            
            future_to_critic = {}
            for member in COUNCIL:
                task = executor.submit(talk_to_ai, member['id'], critique_instruction, transcript)
                future_to_critic[task] = member
            
            for future in concurrent.futures.as_completed(future_to_critic):
                member = future_to_critic[future]
                critiques.append({
                    "name": member['name'],
                    "color": member['color'],
                    "text": future.result()
                })

        # PHASE 3: THE VERDICT 
        final_dossier = f"User Question: {user_query}\n\n=== DRAFTS ===\n{transcript}\n\n=== CRITIQUES ===\n"
        for c in critiques:
            final_dossier += f"{c['name']} says: {c['text']}\n"
            
        chairman_instruction = (
            "You are the Final Judge. Read the Drafts and the Critiques. "
            "Combine the best parts into one perfect answer. "
            "Discard the bad advice."
        )

        verdict = talk_to_ai(COUNCIL[0]['id'], chairman_instruction, final_dossier)

        return render_template('index.html', query=user_query, drafts=drafts, critiques=critiques, verdict=verdict)

    return render_template('index.html', query=None)

if __name__ == '__main__':
    app.run(debug=True)
