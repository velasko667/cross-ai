import os
import openai
import json
from flask import Flask, request, jsonify
from datetime import datetime
from playwright.sync_api import sync_playwright

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

YOUTUBE_CHANNELS = {"jctech": "demo", "timesaver": "demo"}
TIKTOK_ACCOUNTS = ["@tech", "@business"]

class CrossMediaAI:
    def get_demo_videos(self):
        """Données demo réalistes"""
        return {
            "youtube": [
                {"title": "Notion IA révolutionne productivité 2026", "url": "yt1"},
                {"title": "Setup trading ultra efficace", "url": "yt2"},
                {"title": "Gadgets tech indispensables", "url": "yt3"}
            ],
            "tiktok": [
                {"title": "Notion hacks productivité max", "url": "tk1"},
                {"title": "Setup bureau trader parfait", "url": "tk2"},
                {"title": "Gadgets qui changent vie", "url": "tk3"}
            ]
        }
    
    def find_best_crossings(self, yt_videos, tk_videos):
        """Matching mots-clés simple"""
        pairs = []
        keywords = ['notion', 'productivité', 'trading', 'setup', 'tech', 'gadgets']
        
        for yt in yt_videos:
            for tk in tk_videos:
                score = sum(1 for k in keywords if k in yt['title'].lower() and k in tk['title'].lower())
                if score > 0:
                    pairs.append({"youtube": yt, "tiktok": tk, "score": score})
        return sorted(pairs, key=lambda x: x['score'], reverse=True)[:2]
    
    def generate_script(self, pair):
        prompt = f"""YouTube: {pair['youtube']['title']}
TikTok: {pair['tiktok']['title']}

Script 45s croisant les 2 (tech/business/productivité):
JSON: {{"title": "viral", "script": "45s texte", "hashtags": ["#IA","#Tech"]}}"""
        
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return json.loads(response.choices[0].message.content)
    
    def run_pipeline(self):
        print("🚀 IA Cross YouTube/TikTok")
        
        videos = self.get_demo_videos()
        pairs = self.find_best_crossings(videos["youtube"], videos["tiktok"])
        
        results = []
        for pair in pairs:
            script = self.generate_script(pair)
            results.append({
                "title": script["title"],
                "script": script["script"],
                "hashtags": script["hashtags"],
                "score": pair["score"],
                "ready_to_post": True
            })
        
        with open("reels.json", "w") as f:
            json.dump(results, f, indent=2)
        
        print(f"✅ {len(results)} Reels/scripts prêts !")
        return results

ai = CrossMediaAI()

@app.route('/run-daily', methods=['POST'])
def run_daily():
    try:
        results = ai.run_pipeline()
        return jsonify({"success": True, "videos": len(results), "results": results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "OK", "ready": True})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
