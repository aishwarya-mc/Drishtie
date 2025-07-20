# check_db_schema.py
from supabase import create_client, Client
import settings as settings
from uuid import uuid4

supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

def check_table_schema():
    """Check the current table schema"""
    try:
        # Try to get table info
        response = supabase.table("drishti details").select("*").limit(1).execute()
        print("✅ Table exists and is accessible")
        
        # Get all entries to see current data
        all_entries = supabase.table("drishti details").select("*").execute()
        print(f"📊 Current entries in table: {len(all_entries.data)}")
        
        if all_entries.data:
            print("📋 Sample entry structure:")
            sample = all_entries.data[0]
            for key, value in sample.items():
                print(f"  {key}: {type(value).__name__} = {value}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error accessing table: {str(e)}")
        return False

def test_insert():
    """Test inserting a new entry"""
    try:
        test_data = {
            "id": str(uuid4()),  # Use proper UUID format
            "user_id": str(uuid4()),  # Use proper UUID format
            "description": "Test description",
            "summary": "Test summary",
            "urgency": "low",
            "animal_type": "dog",
            "image_url": "https://example.com/image.jpg",
            "lat": 12.345,
            "lon": 67.890,
            "note": "Test note",
            "created_at": "2024-01-01T00:00:00"
        }
        
        response = supabase.table("drishti details").insert(test_data).execute()
        print("✅ Test insert successful")
        print(f"📝 Inserted data: {response.data}")
        
        # Clean up test data
        supabase.table("drishti details").delete().eq("id", test_data["id"]).execute()
        print("🧹 Test data cleaned up")
        
        return True
        
    except Exception as e:
        print(f"❌ Test insert failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔍 Checking database schema...")
    check_table_schema()
    
    print("\n🧪 Testing insert functionality...")
    test_insert()
    
    print("\n💡 Recommendations:")
    print("1. If you see unique constraint errors, you may need to modify your database schema")
    print("2. The 'id' field should be the primary key, not 'user_id'")
    print("3. 'user_id' should allow duplicates to support multiple entries per user")
    print("4. Consider running this SQL in your Supabase dashboard:")
    print("   ALTER TABLE \"drishti details\" DROP CONSTRAINT IF EXISTS \"drishti details_user_id_key\";")
    print("   ALTER TABLE \"drishti details\" ADD PRIMARY KEY (id);") 