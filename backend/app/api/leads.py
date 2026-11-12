from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.core.database import get_db, row_to_dict

router = APIRouter(tags=["leads"])


class LeadIn(BaseModel):
    name: str
    phone: Optional[str] = None
    budget: Optional[str] = None
    location: Optional[str] = None
    property_type: Optional[str] = None
    bhk: Optional[str] = None
    intent: Optional[str] = None
    notes: Optional[str] = None
    transcript: Optional[str] = None
    language: Optional[str] = None
    source: str = "manual"
    status: str = "new"
    priority: str = "medium"
    summary: Optional[str] = None
    next_action: Optional[str] = None
    request_id: Optional[str] = None


class LeadUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    budget: Optional[str] = None
    location: Optional[str] = None
    property_type: Optional[str] = None
    bhk: Optional[str] = None
    intent: Optional[str] = None
    notes: Optional[str] = None
    transcript: Optional[str] = None
    language: Optional[str] = None
    source: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    summary: Optional[str] = None
    next_action: Optional[str] = None


@router.get("/leads")
def list_leads(q: Optional[str] = None, status: Optional[str] = None, intent: Optional[str] = None, limit: int = 100, offset: int = 0):
    with get_db() as conn:
        sql = "SELECT * FROM leads WHERE 1=1"
        params: list = []
        if q:
            sql += " AND (name LIKE ? OR phone LIKE ? OR location LIKE ? OR transcript LIKE ?)"
            like = f"%{q}%"
            params += [like, like, like, like]
        if status:
            sql += " AND status = ?"
            params.append(status)
        if intent:
            sql += " AND intent = ?"
            params.append(intent)
        sql += " ORDER BY id DESC LIMIT ? OFFSET ?"
        params += [limit, offset]
        rows = conn.execute(sql, params).fetchall()
        total = conn.execute("SELECT COUNT(*) FROM leads").fetchone()[0]
        return {"items": [row_to_dict(r) for r in rows], "total": total, "limit": limit, "offset": offset}


@router.get("/leads/stats")
def stats():
    with get_db() as conn:
        total = conn.execute("SELECT COUNT(*) FROM leads").fetchone()[0]
        by_status = {r[0]: r[1] for r in conn.execute("SELECT status, COUNT(*) FROM leads GROUP BY status").fetchall()}
        high = conn.execute("SELECT COUNT(*) FROM leads WHERE priority='high'").fetchone()[0]
        return {"total": total, "by_status": by_status, "high_priority": high}


@router.get("/leads/{lead_id}")
def get_lead(lead_id: int):
    with get_db() as conn:
        row = conn.execute("SELECT * FROM leads WHERE id=?", (lead_id,)).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Lead not found")
        return row_to_dict(row)


@router.post("/leads", status_code=201)
def create_lead(lead: LeadIn):
    now = datetime.now(timezone.utc).isoformat()
    with get_db() as conn:
        cur = conn.execute(
            """INSERT INTO leads (name,phone,budget,location,property_type,bhk,intent,notes,transcript,language,source,status,priority,summary,next_action,request_id,created_at,updated_at)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (lead.name, lead.phone, lead.budget, lead.location, lead.property_type, lead.bhk, lead.intent, lead.notes,
             lead.transcript, lead.language, lead.source, lead.status, lead.priority, lead.summary, lead.next_action,
             lead.request_id, now, now),
        )
        new_id = cur.lastrowid
        row = conn.execute("SELECT * FROM leads WHERE id=?", (new_id,)).fetchone()
        return row_to_dict(row)


@router.patch("/leads/{lead_id}")
def update_lead(lead_id: int, lead: LeadUpdate):
    with get_db() as conn:
        existing = conn.execute("SELECT * FROM leads WHERE id=?", (lead_id,)).fetchone()
        if not existing:
            raise HTTPException(status_code=404, detail="Lead not found")
        data = lead.model_dump(exclude_unset=True)
        if not data:
            return row_to_dict(existing)
        sets = ", ".join(f"{k}=?" for k in data.keys()) + ", updated_at=?"
        params = list(data.values()) + [datetime.now(timezone.utc).isoformat(), lead_id]
        conn.execute(f"UPDATE leads SET {sets} WHERE id=?", params)
        row = conn.execute("SELECT * FROM leads WHERE id=?", (lead_id,)).fetchone()
        return row_to_dict(row)


@router.delete("/leads/{lead_id}", status_code=204)
def delete_lead(lead_id: int):
    with get_db() as conn:
        existing = conn.execute("SELECT * FROM leads WHERE id=?", (lead_id,)).fetchone()
        if not existing:
            raise HTTPException(status_code=404, detail="Lead not found")
        conn.execute("DELETE FROM leads WHERE id=?", (lead_id,))
    return None


@router.post("/leads/extract")
def extract(payload: dict):
    from app.services.extraction import extract_lead
    transcript = payload.get("transcript", "")
    return extract_lead(transcript)
