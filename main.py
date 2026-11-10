from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI(title="Notes API")

# MODELS
# separate input & output models
class NoteCreate(BaseModel):
    title: str
    content: str = ""
    tags: list[str] = []

class Note(NoteCreate):
    id: int

# DATABASE (dict in memory for now)
notes: dict[int, Note] = {}
next_id = 1


# ENDPOINTS

@app.post("/notes", response_model=Note, status_code=status.HTTP_201_CREATED)
def create_note(note: NoteCreate):
    # get next_id
    global next_id
    # creat a new note with the deserialized content
    new_note = Note(id=next_id, **note.model_dump())
    # add new note to "database"
    notes[next_id] = new_note
    # increment next id for next note
    next_id += 1
    return new_note

@app.get("/notes", response_model=list[Note])
def list_notes():
    return list(notes.values())

@app.get("/notes/{note_id}", response_model=Note)
def get_note(note_id: int):
    if note_id not in notes:
        raise HTTPException(status_code=404, detail = "Note not found")
    return notes[note_id]

@app.put("notes/{note_id}", response_model=Note)
def update_note(note_id: int, note: NoteCreate):
    if note_id not in notes:
        raise HTTPException(status_code= 404, detail="Note not found")
    updated = Note(id=note_id, **note.model_dump())
    notes[note_id] = updated
    return updated

@app.delete("/notes/{note_id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_note(note_id:int):
    if note_id not in notes:
        raise HTTPException(status_code=404, detail = "Note not found")
    del notes[note_id]