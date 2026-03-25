# ============================================================
# Visible — Relational Database Layer
# Relational Databases with SQLAlchemy Assignment
# Coding Temple Advanced Python Module
#
# This module implements the core relational database schema
# for Visible, a career decision intelligence platform.
#
# Domain model:
#   VisibleUser        — a professional using the platform
#   ContributionEntry  — a documented work contribution
#   PromotionCase      — links a user to their contribution
#                        evidence for a specific career goal
#
# SQLAlchemy concepts demonstrated:
#   - Engine and session setup
#   - Declarative base model definition
#   - Primary keys, foreign keys, unique constraints
#   - One-to-many relationships with relationship()
#   - CRUD: Create, Read, Update, Delete
#   - Bonus: Boolean status column and aggregate queries
# ============================================================

from sqlalchemy import (
    create_engine, Column, Integer, String,
    ForeignKey, Boolean, Float, func
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


# ============================================================
# PART 1: SETUP
# ============================================================

# Create SQLite engine — stores data in visible.db file
engine = create_engine('sqlite:///visible.db', echo=False)

# Base class for all ORM models
Base = declarative_base()

# Session factory — used for all database operations
Session = sessionmaker(bind=engine)
session = Session()


# ============================================================
# PART 2: DEFINE TABLES
# ============================================================

class VisibleUser(Base):
    """
    Represents a professional using the Visible platform.
    Replaces the generic User table with career-relevant fields.

    Relationships:
        cases: One user can have many PromotionCases
    """
    __tablename__ = 'visible_users'

    # Primary key — auto-incremented unique identifier
    id         = Column(Integer, primary_key=True)

    # User identity
    name       = Column(String, nullable=False)
    email      = Column(String, unique=True, nullable=False)
    job_title  = Column(String, nullable=True)
    company    = Column(String, nullable=True)

    # Relationship: one user has many promotion cases
    cases = relationship('PromotionCase', back_populates='user')

    def __repr__(self):
        return (f"<VisibleUser id={self.id} name='{self.name}' "
                f"title='{self.job_title}' company='{self.company}'>")


class ContributionEntry(Base):
    """
    Represents a single documented work contribution.
    Replaces the generic Product table with career-relevant fields.

    Relationships:
        cases: One contribution can appear in many PromotionCases
    """
    __tablename__ = 'contribution_entries'

    # Primary key
    id           = Column(Integer, primary_key=True)

    # Contribution details
    title        = Column(String, nullable=False)
    category     = Column(String, nullable=False)   # revenue, process, etc.
    impact_score = Column(Float, nullable=False)    # 0-100

    # Relationship: one entry can appear in many promotion cases
    cases = relationship('PromotionCase', back_populates='contribution')

    def __repr__(self):
        return (f"<ContributionEntry id={self.id} "
                f"title='{self.title[:40]}' "
                f"impact={self.impact_score}>")


class PromotionCase(Base):
    """
    Links a VisibleUser to a ContributionEntry as evidence
    for a specific career goal (promotion, raise, departure).
    Replaces the generic Order table.

    Foreign keys:
        user_id:          References VisibleUser.id
        contribution_id:  References ContributionEntry.id

    Relationships:
        user:         The user this case belongs to
        contribution: The contribution entry used as evidence
    """
    __tablename__ = 'promotion_cases'

    # Primary key
    id              = Column(Integer, primary_key=True)

    # Foreign keys — link to user and contribution tables
    user_id         = Column(Integer, ForeignKey('visible_users.id'),
                             nullable=False)
    contribution_id = Column(Integer, ForeignKey('contribution_entries.id'),
                             nullable=False)

    # How strongly this contribution supports the promotion case
    # Replaces quantity — higher weight = stronger evidence
    evidence_weight = Column(Integer, nullable=False, default=1)

    # Bonus: whether this case has been presented to a manager
    # Replaces shipped boolean
    submitted       = Column(Boolean, default=False)

    # Relationships — back_populates creates bidirectional access
    user         = relationship('VisibleUser',       back_populates='cases')
    contribution = relationship('ContributionEntry', back_populates='cases')

    def __repr__(self):
        return (f"<PromotionCase id={self.id} "
                f"user_id={self.user_id} "
                f"contribution_id={self.contribution_id} "
                f"weight={self.evidence_weight} "
                f"submitted={self.submitted}>")


# ============================================================
# PART 3: CREATE TABLES
# ============================================================

# Create all tables in the SQLite database
# If tables already exist this does nothing (safe to re-run)
Base.metadata.create_all(engine)
print("=" * 55)
print("PART 3: Tables created in visible.db")
print("  - visible_users")
print("  - contribution_entries")
print("  - promotion_cases")
print("=" * 55)


# ============================================================
# PART 4: INSERT DATA
# ============================================================

print("\n" + "=" * 55)
print("PART 4: Inserting Data")
print("=" * 55)

# --- Insert 2 Users ---
user1 = VisibleUser(
    name="Kathy Matos",
    email="kmatosli@yahoo.com",
    job_title="Senior Operations Analyst",
    company="Acme Financial"
)
user2 = VisibleUser(
    name="Jordan Rivera",
    email="jrivera@gmail.com",
    job_title="Finance Associate",
    company="Meridian Capital"
)

session.add(user1)
session.add(user2)
session.commit()
print(f"\n  Added users:")
print(f"    {user1}")
print(f"    {user2}")

# --- Insert 3 Contribution Entries ---
entry1 = ContributionEntry(
    title="Automated monthly reconciliation — saved 12hrs/month",
    category="process",
    impact_score=88.5
)
entry2 = ContributionEntry(
    title="Closed Q3 enterprise deal — $2.4M ARR",
    category="revenue",
    impact_score=96.0
)
entry3 = ContributionEntry(
    title="Onboarded and mentored 3 new analysts",
    category="leadership",
    impact_score=74.0
)

session.add(entry1)
session.add(entry2)
session.add(entry3)
session.commit()
print(f"\n  Added contribution entries:")
print(f"    {entry1}")
print(f"    {entry2}")
print(f"    {entry3}")

# --- Insert 4 Promotion Cases ---
# Link users to their contribution evidence
case1 = PromotionCase(
    user_id=user1.id,
    contribution_id=entry1.id,
    evidence_weight=3,      # High weight — strong process evidence
    submitted=True          # Already presented to manager
)
case2 = PromotionCase(
    user_id=user1.id,
    contribution_id=entry3.id,
    evidence_weight=2,      # Medium weight — supporting leadership evidence
    submitted=False         # Not yet presented
)
case3 = PromotionCase(
    user_id=user2.id,
    contribution_id=entry2.id,
    evidence_weight=5,      # Very high weight — revenue evidence
    submitted=True
)
case4 = PromotionCase(
    user_id=user2.id,
    contribution_id=entry1.id,
    evidence_weight=1,      # Low weight — secondary process evidence
    submitted=False
)

session.add(case1)
session.add(case2)
session.add(case3)
session.add(case4)
session.commit()
print(f"\n  Added promotion cases:")
print(f"    {case1}")
print(f"    {case2}")
print(f"    {case3}")
print(f"    {case4}")


# ============================================================
# PART 5: QUERIES
# ============================================================

print("\n" + "=" * 55)
print("PART 5: Queries")
print("=" * 55)

# --- Query 1: Retrieve all users ---
print("\n  1. All Users:")
users = session.query(VisibleUser).all()
for user in users:
    print(f"     ID:{user.id} | {user.name} | {user.email} "
          f"| {user.job_title} @ {user.company}")

# --- Query 2: Retrieve all contribution entries ---
print("\n  2. All Contribution Entries:")
entries = session.query(ContributionEntry).all()
for entry in entries:
    print(f"     ID:{entry.id} | [{entry.category.upper()}] "
          f"{entry.title[:45]} | Impact: {entry.impact_score}")

# --- Query 3: All promotion cases with user and contribution ---
print("\n  3. All Promotion Cases (user → contribution):")
cases = session.query(PromotionCase).all()
for case in cases:
    print(f"     Case {case.id}: {case.user.name:<20} → "
          f"'{case.contribution.title[:35]}' "
          f"| weight={case.evidence_weight} "
          f"| submitted={case.submitted}")

# --- Query 4: Update a contribution's impact score ---
print("\n  4. Updating impact score for entry 3:")
entry_to_update = session.query(ContributionEntry).filter_by(id=3).first()
print(f"     Before: {entry_to_update.title[:40]} | "
      f"impact={entry_to_update.impact_score}")
entry_to_update.impact_score = 82.0   # Revised after additional evidence
session.commit()
print(f"     After:  {entry_to_update.title[:40]} | "
      f"impact={entry_to_update.impact_score}")

# --- Query 5: Delete a user by ID ---
print("\n  5. Deleting user with ID=2:")
user_to_delete = session.query(VisibleUser).filter_by(id=2).first()
if user_to_delete:
    print(f"     Deleting: {user_to_delete}")
    # Delete associated cases first to avoid foreign key constraint
    session.query(PromotionCase).filter_by(user_id=user_to_delete.id).delete()
    session.delete(user_to_delete)
    session.commit()
    print(f"     User ID=2 and their cases deleted successfully.")

# Confirm remaining users
remaining = session.query(VisibleUser).all()
print(f"     Remaining users: {[u.name for u in remaining]}")


# ============================================================
# PART 6: BONUS
# ============================================================

print("\n" + "=" * 55)
print("PART 6: Bonus — Status Queries and Aggregates")
print("=" * 55)

# --- Query all cases not yet submitted (not yet presented) ---
print("\n  Cases not yet submitted to manager:")
pending = session.query(PromotionCase).filter_by(submitted=False).all()
if pending:
    for case in pending:
        print(f"     Case {case.id}: {case.user.name} → "
              f"'{case.contribution.title[:40]}'")
else:
    print("     All cases have been submitted.")

# --- Count total number of cases per user ---
print("\n  Total promotion cases per user:")
case_counts = (
    session.query(
        VisibleUser.name,
        func.count(PromotionCase.id).label('case_count')
    )
    .join(PromotionCase, VisibleUser.id == PromotionCase.user_id)
    .group_by(VisibleUser.id)
    .all()
)
for name, count in case_counts:
    print(f"     {name}: {count} case(s) documented")

# --- Average impact score of contributions in active cases ---
print("\n  Average impact score across all documented contributions:")
avg_impact = session.query(
    func.avg(ContributionEntry.impact_score)
).scalar()
print(f"     Platform average: {avg_impact:.1f} / 100")

print("\n" + "=" * 55)
print("Visible Relational Database — all parts complete.")
print("Tables: visible_users, contribution_entries, promotion_cases")
print("=" * 55)

# Close the session cleanly
session.close()
