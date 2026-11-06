from fastapi import FastAPI, Query, HTTPException
from models import MenuItem, MenuResponse
import uvicorn
from data import menu_items

app = FastAPI(
    title="Chai Point menu API",
    description=" Reade only menu API for Kiosk display and mobile app",
    
)

@app.get("/")
def root():
    return {
        "message":"Welcome to chaipoint Menu API"
    }
    
# menu -> path
# menu?category=chai

@app.get("/menu", response_model=MenuResponse, tags=["Menu"])
def get_menu(
    category: str | None = Query(
        None,
        description="Filter by category: chai, sandwich, snacks, coffee, or all"
    )
):
    if category:
        filtered = [item for item in menu_items if item["category"] == category.lower()]
        if not filtered:
            raise HTTPException(status_code=404, detail=f"No item found in category={category}")
        return MenuResponse(count=len(filtered), items=filtered)
    
    return MenuResponse(
        count= len(menu_items),
        items= menu_items
    )

@app.get("/menu/{item_id}", response_model=MenuItem, tags=["Menu"])
def get_menu_item_by_id(item_id: int):
    
    for item in menu_items:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail=f"Menu item with id: {item_id} not found!")
    

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
    