import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import speech_recognition as sr
import os
from datetime import datetime
from transformers import pipeline

# -------------------
# Database setup
# -------------------
DB_FILE = "journal.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS mood_entries
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  timestamp TEXT,
                  mood_text TEXT,
                  emotion TEXT)''')
    conn.commit()
    conn.close()

def insert_entry(mood_text, emotion):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO mood_entries (timestamp, mood_text, emotion) VALUES (?, ?, ?)",
              (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), mood_text, emot_
