from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserProfileDetails
from app.models import UserDb, StudentProfileDb
from fastapi import HTTPException
from app.auth import create_access_token, hash_password, verify_password
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, outerjoin
from app.crud.faculty_subject import get_faculty_by_user_id


async def get_user_by_email(db: Session, email: str):
    return db.query(UserDb).filter(UserDb.email == email).first()


async def get_student_profile_details(db: Session, user_id: int):
    return (
        db.query(StudentProfileDb).filter(StudentProfileDb.user_id == user_id).first()
    )


async def get_student_details(db: AsyncSession, email: str):
    stmt = (
        select(
            UserDb.id,
            UserDb.name,
            UserDb.email,
            UserDb.is_registered,
            StudentProfileDb.faculty_id,
            StudentProfileDb.class_id,
        )
        .select_from(
            outerjoin(UserDb, StudentProfileDb, UserDb.id == StudentProfileDb.user_id)
        )
        .where(UserDb.email == email)
    )

    result = await db.execute(stmt)
    user_data = result.fetchone()

    if not user_data:
        return None

    return {
        "id": user_data.id,
        "name": user_data.name,
        "email": user_data.email,
        "is_registered": user_data.is_registered,
        "faculty_id": user_data.faculty_id,
        "class_id": user_data.class_id,
    }


async def create_user(db: Session, user: UserCreate, role: str):
    db_user = await get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = hash_password(user.password)
    new_user = UserDb(
        name=user.name, email=user.email, role=role, password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    token = create_access_token(data={"sub": new_user.email})
    return {
        "user": {"id": new_user.id, "email": new_user.email, "name": new_user.name},
        "access_token": token,
    }


async def login_user(db: AsyncSession, email: str, password: str):
    db_user = await get_user_by_email(db, email)
    if not db_user or not verify_password(password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(data={"sub": db_user.email})
    if db_user.role == "student":
        student_profile = await get_student_profile_details(db, db_user.id)
        return {
            "user": {
                "id": db_user.id,
                "email": db_user.email,
                "name": db_user.name,
                "faculty_id": student_profile.faculty_id if student_profile else None,
                "class_id": student_profile.class_id if student_profile else None,
                "is_registered": db_user.is_registered,
            },
            "access_token": token,
        }
    else:
        faculty_profile = await get_faculty_by_user_id(db, user_id=db_user.id)
        return {
            "user": {
                "id": db_user.id,
                "email": db_user.email,
                "name": db_user.name,
                "faculty_name": faculty_profile.name if faculty_profile else None,
                "faculty_email": faculty_profile.email if faculty_profile else None,
                "faculty_id": faculty_profile.id if faculty_profile else None,
                "is_registered": db_user.is_registered,
            },
            "access_token": token,
        }


async def update_student_profile(
    db: Session, user_profile: UserProfileDetails, user_id: int
):
    user_profile_details = await get_student_profile_details(db, user_id)
    if user_profile_details:
        raise ValueError("User profile details already updated")
    new_student_profile = StudentProfileDb(
        faculty_id=user_profile.faculty_id,
        class_id=user_profile.class_id,
        user_id=user_id,
    )
    db.add(new_student_profile)
    query = (
        update(UserDb)
        .where(UserDb.id == user_id)
        .values(is_registered=True)
        .execution_options(synchronize_session="fetch")
    )
    db.execute(query)
    db.commit()
    db.refresh(new_student_profile)
    return {
        "class_id": new_student_profile.class_id,
        "faculty_id": new_student_profile.faculty_id,
        "is_registered": True,
    }
