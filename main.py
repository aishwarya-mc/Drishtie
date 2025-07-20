# main.py
from fastapi import FastAPI, HTTPException
from starlette.responses import JSONResponse
from pydantic import BaseModel
from supabase import create_client, Client
from uuid import uuid4, UUID
from datetime import datetime
import traceback
import settings as settings


supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

app = FastAPI()

# Schema for input
class UserInput(BaseModel):
    user_id: UUID
    description: str
    summary: str
    urgency: str
    animal_type: str
    image_url: str
    lat: float
    lon: float
    note: str

class User(UserInput):
    id: UUID
    created_at: datetime


@app.get("/entries")
def get_entries():
    response = supabase.table("drishti details").select("*").execute()
    return response.data

@app.get("/entries/{user_id}")
def get_entries_by_user(user_id: str):
    response = supabase.table("drishti details").select("*").eq("user_id", user_id).execute()
    return response.data

@app.post("/add")
def add_entry(user: UserInput):
    try:
        # Generate a new UUID for the entry ID
        entry_id = str(uuid4())
        
        insert_data = {
            "id": entry_id,  # Use this as the primary key
            "user_id": str(user.user_id),  # This can be repeated for multiple entries per user
            "description": user.description,
            "summary": user.summary,
            "urgency": user.urgency,
            "animal_type": user.animal_type,
            "image_url": user.image_url,
            "lat": user.lat,
            "lon": user.lon,
            "note": user.note,
            "created_at": datetime.utcnow().isoformat()
        }

        response = supabase.table("drishti details").insert(insert_data).execute()
        
        if response.data:
            return {"status": "Entry added successfully", "data": response.data[0]}
        else:
            raise HTTPException(status_code=500, detail="Failed to add entry")

    except Exception as e:
        tb = traceback.format_exc()
        print(f"Error adding entry: {str(e)}")
        print(f"Traceback: {tb}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "traceback": tb}
        )


@app.put("/update/{id}")
def update_entry(id: str, updated_user: UserInput):
    try:
        update_data = {
            "user_id": str(updated_user.user_id),
            "description": updated_user.description,
            "summary": updated_user.summary,
            "urgency": updated_user.urgency,
            "animal_type": updated_user.animal_type,
            "image_url": updated_user.image_url,
            "lat": updated_user.lat,
            "lon": updated_user.lon,
            "note": updated_user.note,
            "created_at": datetime.utcnow().isoformat()
        }

        # Find and update by ID
        response = supabase.table("drishti details") \
            .update(update_data) \
            .eq("id", id) \
            .execute()

        if response.data:
            return {"status": "Entry updated successfully", "data": response.data[0]}
        else:
            raise HTTPException(status_code=404, detail="Entry not found")

    except Exception as e:
        tb = traceback.format_exc()
        print(f"Error updating entry: {str(e)}")
        print(f"Traceback: {tb}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "traceback": tb}
        )

@app.delete("/delete/{id}")
def delete_entry(id: str):
    try:
        response = supabase.table("drishti details").delete().eq("id", id).execute()
        if response.data:
            return {"message": "Entry deleted successfully", "deleted_data": response.data[0]}
        else:
            raise HTTPException(status_code=404, detail="Entry not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/delete/user/{user_id}")
def delete_entries_by_user(user_id: str):
    try:
        response = supabase.table("drishti details").delete().eq("user_id", user_id).execute()
        if response.data:
            return {"message": f"Deleted {len(response.data)} entries for user", "deleted_data": response.data}
        else:
            raise HTTPException(status_code=404, detail="No entries found for this user")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))