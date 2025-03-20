# RA2211003011516

### **calc.py - Number Stream Processor**  
FastAPI service using a sliding window (size 10) to process numbers from a third-party API.  

#### **Endpoint:**  
- **`/numbers/{numberid}`** → Fetches unique numbers, updates the window, and returns the moving average.  

#### **Run:**  
```bash
pip install fastapi uvicorn httpx  
uvicorn calc:app --reload
```

---

### **analytics.py - Social Media Analytics**  
FastAPI service analyzing user posts and engagement.  

#### **Endpoints:**  
- **`/users`** → Top 5 users by post count.  
- **`/posts?type=popular|latest`** → Most commented or latest 5 posts.  

#### **Run:**  
```bash
pip install fastapi uvicorn requests  
uvicorn analytics:app --reload
```