from datetime import datetime
from sqlalchemy import JSON, DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Client(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    client_code: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    brand_name: Mapped[str] = mapped_column(String(255), index=True)
    industry: Mapped[str] = mapped_column(String(255))
    city: Mapped[str] = mapped_column(String(255))
    core_services: Mapped[list] = mapped_column(JSON, default=list)
    target_persona: Mapped[str] = mapped_column(Text)
    competitors: Mapped[list] = mapped_column(JSON, default=list)
    website_url: Mapped[str] = mapped_column(String(512), default="")
    social_accounts: Mapped[list] = mapped_column(JSON, default=list)
    pain_points: Mapped[str] = mapped_column(Text, default="")
    promise_scope: Mapped[str] = mapped_column(String(64), default="visibility_only")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class DiagnosticPrompt(Base):
    __tablename__ = "diagnostic_prompts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"), index=True)
    category: Mapped[str] = mapped_column(String(64))
    platform: Mapped[str] = mapped_column(String(64))
    text: Mapped[str] = mapped_column(Text)
    batch: Mapped[str] = mapped_column(String(32), default="baseline")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class PlatformResponse(Base):
    __tablename__ = "platform_responses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"), index=True)
    prompt_id: Mapped[int] = mapped_column(ForeignKey("diagnostic_prompts.id"), index=True)
    platform: Mapped[str] = mapped_column(String(64))
    prompt_text: Mapped[str] = mapped_column(Text)
    response_text: Mapped[str] = mapped_column(Text)
    source: Mapped[str] = mapped_column(String(32), default="manual")
    queried_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"), index=True)
    response_id: Mapped[int] = mapped_column(ForeignKey("platform_responses.id"), index=True)
    brand_mentioned: Mapped[int] = mapped_column(Integer, default=0)
    brand_rank: Mapped[int] = mapped_column(Integer, default=0)
    sentiment: Mapped[str] = mapped_column(String(32), default="neutral")
    accuracy_score: Mapped[float] = mapped_column(Float, default=0.7)
    competitor_mentions: Mapped[list] = mapped_column(JSON, default=list)
    evidence_items: Mapped[list] = mapped_column(JSON, default=list)
    hallucination_note: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class ContentAsset(Base):
    __tablename__ = "content_assets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"), index=True)
    platform: Mapped[str] = mapped_column(String(64))
    topic: Mapped[str] = mapped_column(String(255))
    draft_text: Mapped[str] = mapped_column(Text)
    quality_status: Mapped[str] = mapped_column(String(64), default="draft")
    quality_notes: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class PublishSchedule(Base):
    __tablename__ = "publish_schedules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"), index=True)
    platform: Mapped[str] = mapped_column(String(64))
    asset_id: Mapped[int] = mapped_column(ForeignKey("content_assets.id"), index=True, nullable=True)
    scheduled_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    status: Mapped[str] = mapped_column(String(64), default="scheduled")


class TrackingReport(Base):
    __tablename__ = "tracking_reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"), index=True)
    period: Mapped[str] = mapped_column(String(32))
    geo_score_total: Mapped[float] = mapped_column(Float, default=0)
    score_breakdown: Mapped[dict] = mapped_column(JSON, default=dict)
    delta_vs_baseline: Mapped[float] = mapped_column(Float, default=0)
    evidence_summary: Mapped[list] = mapped_column(JSON, default=list)
    disclaimer_text: Mapped[str] = mapped_column(Text)
    next_actions: Mapped[list] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    task_type: Mapped[str] = mapped_column(String(64), index=True)
    status: Mapped[str] = mapped_column(String(32), default="queued")
    payload: Mapped[dict] = mapped_column(JSON, default=dict)
    result: Mapped[dict] = mapped_column(JSON, default=dict)
    error: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id"), index=True, nullable=True)
    action: Mapped[str] = mapped_column(String(128))
    detail: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(128), unique=True)
    role: Mapped[str] = mapped_column(String(64), default="admin")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

