import streamlit as st
import json
import os
from collections import defaultdict

FILE_NAME = "notes.json"

st.title("📑 Нотатки")

EMOJI_OPTIONS = {
    "🎬 Фільми": "🎬",
    "📖 Книги": "📖",
    "🍳 Рецепти": "🍳",
    "🎵 Музика": "🎵",
    "📝 Завдання": "📝",
    "📍 Місця": "📍",
    "💡 Ідеї": "💡",
    "🎮 Ігри": "🎮",
    "Інше": ""
}

def load_notes():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_notes(notes):
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(notes, f, ensure_ascii=False, indent=2)

if "notes" not in st.session_state:
    st.session_state.notes = load_notes()
if "show_add_form" not in st.session_state:
    st.session_state.show_add_form = False
if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = {}

# Кнопка "Створити нотатку" змінюється на "Скасувати"
if st.session_state.show_add_form:
    if st.button("❌ Скасувати"):
        st.session_state.show_add_form = False
        st.rerun()
else:
    if st.button("➕ Створити нотатку"):
        st.session_state.show_add_form = True
        st.rerun()

# Форма створення нотатки
if st.session_state.show_add_form:
    selected_emoji_label = st.selectbox("🔽 Оберіть категорію", list(EMOJI_OPTIONS.keys()))
    note_title = st.text_input("🏷️ Назва нотатки")
    note_text = st.text_area("✏️ Введіть нотатку")
    
    if st.button("✅ Додати") and note_title.strip() and note_text.strip():
        new_note = {"category": selected_emoji_label, "title": note_title.strip(), "text": note_text.strip()}
        st.session_state.notes.append(new_note)
        save_notes(st.session_state.notes)
        st.session_state.show_add_form = False
        st.rerun()

notes_by_category = defaultdict(list)
for note in st.session_state.notes:
    notes_by_category[note["category"].strip()].append(note)

for category, notes in notes_by_category.items():
    st.header(category)
    for idx, note in enumerate(notes):
        key = f"edit_{category}_{idx}"
        if key not in st.session_state:
            st.session_state[key] = False

        st.subheader(note["title"])
        
        if st.session_state[key]:
            new_note_text = st.text_area("", note["text"], key=f"text_{category}_{idx}")
            if st.button("✅ Зберегти", key=f"save_{category}_{idx}"):
                note["text"] = new_note_text.strip()
                save_notes(st.session_state.notes)
                st.session_state[key] = False
                st.rerun()
        else:
            st.text(note["text"])
        
        cols = st.columns([1, 1, 1])
        if cols[0].button("✏️ Редагувати", key=f"edit_btn_{category}_{idx}"):
            st.session_state[key] = not st.session_state[key]
            st.rerun()
        
        if cols[1].button("❌ Видалити", key=f"delete_{category}_{idx}"):
            st.session_state.notes.remove(note)
            save_notes(st.session_state.notes)
            st.rerun()
