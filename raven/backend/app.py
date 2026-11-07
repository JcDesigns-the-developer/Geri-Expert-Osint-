from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import json
import sqlite3
from typing import Literal

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "raven_cases.sqlite3"
app = FastAPI(title="RAVEN Local Workbench", version="0.1.0")
app.mount("/static", StaticFiles(directory=ROOT / "frontend"), name="static")

class ObservationIn(BaseModel):
    description: str = Field(min_length=3, max_length=500)
    category: Literal["terrain", "roads", "vegetation", "architecture", "signage", "infrastructure", "other"] = "other"
    reliability: float = Field(default=0.7, ge=0.0, le=1.0)

class CandidateIn(BaseModel):
    label: str = Field(min_length=2, max_length=120)
    supporting_tags: list[str] = Field(default_factory=list, max_length=30)
    contradicting_tags: list[str] = Field(default_factory=list, max_length=30)

class AnalysisIn(BaseModel):
    title: str = Field(default="Untitled case", max_length=120)
    observations: list[ObservationIn] = Field(default_factory=list, max_length=40)
    candidates: list[CandidateIn] = Field(default_factory=list, max_length=20)

def db():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    with db() as con:
        con.execute("""CREATE TABLE IF NOT EXISTS cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            title TEXT NOT NULL,
            request_json TEXT NOT NULL,
            result_json TEXT NOT NULL
        )""")

@app.on_event("startup")
def startup():
    init_db()

@app.get("/", response_class=HTMLResponse)
def home():
    return (ROOT / "frontend" / "index.html").read_text(encoding="utf-8")

@app.get("/api/health")
def health():
    return {"name": "RAVEN", "version": "0.1.0", "mode": "local", "language_model": "not required"}

@app.post("/api/analyze")
def analyze(payload: AnalysisIn):
    if not payload.observations:
        raise HTTPException(400, "Add at least one observation.")
    if not payload.candidates:
        raise HTTPException(400, "Add at least one candidate area to compare.")
    results = []
    for idx, candidate in enumerate(payload.candidates):
        positive = negative = possible = 0.0
        evidence = []
        for obs_idx, obs in enumerate(payload.observations):
            possible += obs.reliability
            desc = obs.description.casefold()
            supported = next((tag for tag in candidate.supporting_tags if tag.casefold() in desc), None)
            contradicted = next((tag for tag in candidate.contradicting_tags if tag.casefold() in desc), None)
            if supported:
                positive += obs.reliability
                evidence.append({"observation": obs.description, "tag": supported, "type": "support", "weight": obs.reliability})
            if contradicted:
                negative += obs.reliability
                evidence.append({"observation": obs.description, "tag": contradicted, "type": "contradiction", "weight": obs.reliability})
        score = round(100 * max(0.0, positive - 1.5 * negative) / possible, 1) if possible else 0.0
        results.append({
            "candidate": candidate.label, "fit_score": score, "evidence": evidence,
            "interpretation": "Contradictory evidence found; review this candidate." if negative else
                ("Some supporting evidence; verify independently." if positive else "No matching evidence.")
        })
    results.sort(key=lambda x: x["fit_score"], reverse=True)
    result = {
        "case_title": payload.title, "ranked_candidates": results,
        "score_warning": "Fit scores are heuristic evidence indices, not probabilities or verified geolocation.",
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    with db() as con:
        cur = con.execute(
            "INSERT INTO cases(created_at,title,request_json,result_json) VALUES(?,?,?,?)",
            (result["generated_at"], payload.title, payload.model_dump_json(), json.dumps(result)),
        )
        result["case_id"] = cur.lastrowid
    return result

@app.get("/api/cases")
def list_cases():
    with db() as con:
        rows = con.execute("SELECT id,created_at,title FROM cases ORDER BY id DESC LIMIT 100").fetchall()
    return [dict(row) for row in rows]

@app.get("/api/cases/{case_id}")
def get_case(case_id: int):
    with db() as con:
        row = con.execute("SELECT * FROM cases WHERE id=?", (case_id,)).fetchone()
    if not row:
        raise HTTPException(404, "Case not found")
    return {"id": row["id"], "created_at": row["created_at"], "title": row["title"],
            "request": json.loads(row["request_json"]), "result": json.loads(row["result_json"])}
