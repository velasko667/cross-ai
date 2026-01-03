import os
import openai
import json
from flask import Flask, request, jsonify
from datetime import datetime
import requests
from moviepy.editor import *
import yt_dlp
from playwright.sync_api import sync_playwright

# Config
app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

YOUTUBE_CHANNELS = {
    "jctech": "UCzZTQvWimSsCzEeCNgtaMyw",
    "timesaver": "UC_ID_TimeSaver"  
}
TIKTOK_ACCOUNTS = ["@tech_tiktok1", "@business_tiktok2"]

class CrossMediaAI:
    def __init__(self):
        pass
    
    def get_youtube_videos(self, channel_id, max_videos=3):
        """Simule YouTube - remplace par API réelle"""
        return [
            {"title": "Notion IA révolutionne productivité", "url": "https://youtube.com/watch?v=yt1", "platform": "youtube"},
            {"title": "Setup trading ultra efficace", "url": "https://youtube.com/watch?v=yt2", "platform": "youtube"},
            {"title": "Gadgets tech 2026 indispensables", "url": "https://youtube.com/watch?v=yt3", "platform": "youtube"}
        ]
    
    def scrape_tiktok_video(self, username, max_videos=3):
        """Simule TikTok - Playwright réel après"""
        return [
            {"title": "Notion hacks productivité max", "url": "https://tiktok.com/@user1/video/1", "platform": "tiktok"},
            {"title": "Setup bureau trader parfait", "url": "https://tiktok.com/@user2/video/2", "platform": "tiktok"},
            {"title": "Gadgets tech qui changent vie", "url": "https://tiktok.com/@user3/video/3", "platform": "tiktok"}
        ]
    
    def find_best_crossings(self, youtube_videos, tiktok_videos):
        """Matching MOTS-CLÉS SIMPLE (sans embeddings)"""
        pairs = []
        for yt in youtube_videos:
            for tk in tiktok_videos:
                # Score mots communs
                yt_words = set(yt["title"].lower().split())
                tk_words = set(tk["title"].lower().split())
                common = len(yt_words & tk_words)
                score = common / max(len(yt_words), len(tk_words))
                
                if score > 0.25:  # Seuil light
                    pairs.append({"youtube": yt, "tiktok": tk, "score": score})
        
        return sorted(pairs, key=lambda x: x['score'], reverse=True)[:3]
    
    def generate_narrative_script(self, pair):
        """Génère script croisé YouTube+TikTok"""
        prompt = f"""
        YouTube: {pair['youtube']['title']}
        TikTok: {pair['tiktok']['title']}
        
        Crée script 45s croisant les 2 vidéos :
        - Trouve LE LIEN LOGIQUE tech/business/productivité
        - Accroche 10s → Synthèse 25s → Call-to-action 10s
        
        JSON : {{"title": "viral", "script_45s": "texte", "hashtags": ["#Tech", "#IA"]}}
        """
        
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return json.loads(response.choices[0].message.content)
    
    def montage_hybrid(self, youtube_url, tiktok_url, script):
        """Montage simple 30s"""
        try:
            ydl_opts = {'format': 'best[height<=720]', 'outtmpl': 'temp_%(id)s.%(ext)s'}
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([youtube_url])
                ydl.download([tiktok_url])
            
            # Clips 10s
            yt_clip = VideoFileClip("temp_yt.mp4").subclip(0, 10)
            tk_clip = VideoFileClip("temp_tk.mp4").subclip(0, 10)
            
