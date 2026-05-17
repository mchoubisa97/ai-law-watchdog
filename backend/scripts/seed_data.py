from datetime import datetime

from sqlalchemy.orm import Session

from app.db.database import SessionLocal

from app.models.jurisdiction import Jurisdiction
from app.models.ai_law import AILaw
from app.models.law_event import LawEvent
from app.models.source_snapshot import SourceSnapshot

def get_or_create_jurisdiction(db: Session, name: str, regulator: str = None, official_source: str = None):
    existing = db.query(Jurisdiction).filter(Jurisdiction.name == name).first()
    if existing:
        return existing
    jurisdiction = Jurisdiction(name=name, regulator=regulator, official_source=official_source)
    db.add(jurisdiction)
    db.commit()
    db.refresh(jurisdiction)
    return jurisdiction

def get_or_create_ai_law(
    db: Session,
    law_name: str,
    jurisdiction_id: int,
    category: str,
    current_status: str,
    official_url: str,
    summary: str,
):
    existing = (
        db.query(AILaw)
        .filter(AILaw.law_name == law_name)
        .first()
    )

    if existing:
        return existing

    law = AILaw(
        law_name=law_name,
        jurisdiction_id=jurisdiction_id,
        category=category,
        current_status=current_status,
        official_url=official_url,
        summary=summary,
    )

    db.add(law)
    db.commit()
    db.refresh(law)

    return law

def create_event(
    db,
    law_id,
    event_type,
    description,
    event_date,
    source_url=None,
):
    event = LawEvent(
        law_id=law_id,
        event_type=event_type,
        description=description,
        event_date=event_date,
        source_url=source_url,
    )

    db.add(event)
    db.commit()
    db.refresh(event)

    return event

def create_snapshot(
    db: Session,
    law_id: int,
    jurisdiction_id: int,
    source_url: str,
    content_hash: str,
    raw_content: str,
):
    snapshot = SourceSnapshot(
        law_id=law_id,
        jurisdiction_id=jurisdiction_id,
        source_url=source_url,
        content_hash=content_hash,
        raw_content=raw_content,
    )

    db.add(snapshot)
    db.commit()

    return snapshot


def seed_data():
    db = SessionLocal()
    try:
        # -------------------------------------------------
        # Jurisdictions
        # -------------------------------------------------

        eu = get_or_create_jurisdiction(db, "European Union", "European Commission", "https://artificialintelligenceact.eu/")
        usa = get_or_create_jurisdiction(db, "United States", "NIST / White House", "https://www.whitehouse.gov/")
        uk = get_or_create_jurisdiction(db, "United Kingdom", "DSIT", "https://www.gov.uk/")
        china = get_or_create_jurisdiction(db, "China", "CAC", "https://www.cac.gov.cn/")
        canada = get_or_create_jurisdiction(db, "Canada", "ISED", "https://ised-isde.canada.ca/")
        india = get_or_create_jurisdiction(db, "India", "MeitY", "https://www.meity.gov.in/")
        singapore = get_or_create_jurisdiction(db, "Singapore", "IMDA", "https://www.imda.gov.sg/")
        australia = get_or_create_jurisdiction(db, "Australia", "DISR", "https://www.industry.gov.au/")
        oecd = get_or_create_jurisdiction(db, "OECD", "OECD", "https://oecd.ai/")
        un = get_or_create_jurisdiction(db, "United Nations", "UNESCO", "https://www.un.org/")

        # -------------------------------------------------
        # AI Laws
        # -------------------------------------------------

        eu_ai_act = get_or_create_ai_law(
            db=db,
            law_name="EU AI Act",
            jurisdiction_id=eu.id,
            category="AI Governance",
            current_status="Approved",
            official_url="https://artificialintelligenceact.eu/",
            summary="Comprehensive European Union regulation for artificial intelligence systems using a risk-based framework.",
        )

        nist_framework = get_or_create_ai_law(
            db=db,
            law_name="NIST AI Risk Management Framework",
            jurisdiction_id=usa.id,
            category="AI Risk Management",
            current_status="Active",
            official_url="https://www.nist.gov/itl/ai-risk-management-framework",
            summary="United States framework for trustworthy and responsible AI risk management.",
        )

        us_ai_order = get_or_create_ai_law(
            db=db,
            law_name="US Executive Order on Safe AI",
            jurisdiction_id=usa.id,
            category="AI Governance",
            current_status="Active",
            official_url="https://www.whitehouse.gov/",
            summary="Executive order establishing standards for AI safety, security, and responsible development.",
        )

        uk_framework = get_or_create_ai_law(
            db=db,
            law_name="UK AI Regulation Framework",
            jurisdiction_id=uk.id,
            category="AI Regulation",
            current_status="Active",
            official_url="https://www.gov.uk/",
            summary="Principles-based AI governance framework adopted by the United Kingdom.",
        )

        china_gen_ai = get_or_create_ai_law(
            db=db,
            law_name="China Generative AI Measures",
            jurisdiction_id=china.id,
            category="Generative AI",
            current_status="Implemented",
            official_url="https://www.cac.gov.cn/",
            summary="Chinese regulatory measures governing generative artificial intelligence services.",
        )

        china_deepfake = get_or_create_ai_law(
            db=db,
            law_name="China Deep Synthesis Regulation",
            jurisdiction_id=china.id,
            category="Deepfake Regulation",
            current_status="Implemented",
            official_url="https://www.cac.gov.cn/",
            summary="Regulation addressing deep synthesis technologies and synthetic media.",
        )

        canada_aida = get_or_create_ai_law(
            db=db,
            law_name="Artificial Intelligence and Data Act",
            jurisdiction_id=canada.id,
            category="AI Governance",
            current_status="Proposed",
            official_url="https://ised-isde.canada.ca/",
            summary="Canadian framework for regulating high-impact AI systems.",
        )

        india_framework = get_or_create_ai_law(
            db=db,
            law_name="India AI Governance Framework",
            jurisdiction_id=india.id,
            category="AI Governance",
            current_status="Draft",
            official_url="https://www.meity.gov.in/",
            summary="Emerging Indian framework for responsible and ethical AI deployment.",
        )

        singapore_framework = get_or_create_ai_law(
            db=db,
            law_name="Singapore Model AI Governance Framework",
            jurisdiction_id=singapore.id,
            category="AI Governance",
            current_status="Active",
            official_url="https://www.imda.gov.sg/",
            summary="Singapore guidance for responsible AI governance and implementation.",
        )

        oecd_principles = get_or_create_ai_law(
            db=db,
            law_name="OECD AI Principles",
            jurisdiction_id=oecd.id,
            category="AI Ethics",
            current_status="Adopted",
            official_url="https://oecd.ai/en/ai-principles",
            summary="International principles promoting trustworthy and human-centric artificial intelligence.",
        )

        un_recommendations = get_or_create_ai_law(
            db=db,
            law_name="UN AI Advisory Recommendations",
            jurisdiction_id=un.id,
            category="Global AI Governance",
            current_status="Advisory",
            official_url="https://www.un.org/",
            summary="United Nations recommendations for international AI governance coordination.",
        )

        # -------------------------------------------------
        # Law Events
        # -------------------------------------------------

        create_event(
            db,
            eu_ai_act.id,
            "EU AI Act Approved",
            "European Parliament approved the AI Act framework.",
            datetime(2024, 3, 13),
        )

        create_event(
            db,
            nist_framework.id,
            "NIST Framework Published",
            "NIST officially released the AI Risk Management Framework.",
            datetime(2023, 1, 26),
        )

        create_event(
            db,
            us_ai_order.id,
            "Executive Order Signed",
            "US administration signed executive order on AI safety.",
            datetime(2023, 10, 30),
        )

        create_event(
            db,
            china_gen_ai.id,
            "Generative AI Measures Effective",
            "Chinese generative AI rules became effective nationally.",
            datetime(2023, 8, 15),
        )

        create_event(
            db,
            canada_aida.id,
            "AIDA Introduced",
            "Canadian government introduced AIDA legislation proposal.",
            datetime(2022, 6, 16),
        )

        # -------------------------------------------------
        # Snapshots
        # -------------------------------------------------

        create_snapshot(
            db=db,
            law_id=eu_ai_act.id,
            jurisdiction_id=eu.id,
            source_url="https://artificialintelligenceact.eu/",
            content_hash="eu_ai_act_v1",
            raw_content="The EU AI Act establishes obligations for providers and deployers of AI systems based on risk categories including prohibited, high-risk, limited-risk, and minimal-risk systems.",
        )

        create_snapshot(
            db=db,
            law_id=nist_framework.id,
            jurisdiction_id=usa.id,
            source_url="https://www.nist.gov/itl/ai-risk-management-framework",
            content_hash="nist_ai_rmf_v1",
            raw_content="The NIST AI Risk Management Framework provides guidance for trustworthy AI development, deployment, and governance across organizations.",
        )

        create_snapshot(
            db=db,
            law_id=china_gen_ai.id,
            jurisdiction_id=china.id,
            source_url="https://www.cac.gov.cn/",
            content_hash="china_genai_v1",
            raw_content="Chinese generative AI measures require providers to ensure lawful training data usage, transparency obligations, and content moderation compliance.",
        )

        create_snapshot(
            db=db,
            law_id=singapore_framework.id,
            jurisdiction_id=singapore.id,
            source_url="https://www.imda.gov.sg/",
            content_hash="singapore_ai_framework_v1",
            raw_content="Singapore's AI governance framework promotes transparency, explainability, fairness, and human-centric AI management practices.",
        )
    
        print("Seed data inserted successfully.")

    finally:
        db.close()


if __name__ == "__main__":
    seed_data()