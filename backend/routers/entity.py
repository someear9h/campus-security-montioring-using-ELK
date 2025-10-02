from fastapi import APIRouter, HTTPException, Path
from schemas.entity_profile import EntityProfile
from services import entity_service

router = APIRouter()

# A list of valid identifier types we can search by.
VALID_IDENTIFIERS = [
    "entity_id", "card_id", "email", "student_id",
    "staff_id", "device_hash", "face_id", "name"
]

@router.get(
    "/{identifier_type}/{identifier_value}/profile",
    response_model=EntityProfile
)
def get_entity_profile(
    identifier_type: str = Path(
        ...,
        description="The type of identifier to search by (e.g., 'card_id')."
    ),
    identifier_value: str = Path(
        ...,
        description="The value of the identifier (e.g., 'C7151')."
    )
):
    """
    Resolves an entity and retrieves their full profile using any known identifier.

    This endpoint searches the master 'entities' record to find the complete
    profile associated with a given piece of information, such as an email,
    card ID, or device hash.
    """
    # 1. Validate that the user is searching for a valid type of ID.
    if identifier_type not in VALID_IDENTIFIERS:
        raise HTTPException(
            status_code=400, # Bad Request
            detail=f"Invalid identifier type. Please use one of: {', '.join(VALID_IDENTIFIERS)}"
        )

    # 2. Call the service function to perform the lookup in Elasticsearch.
    profile = entity_service.find_profile_by_identifier(
        id_column=identifier_type,
        id_value=identifier_value
    )

    # 3. If the service returns None, it means no profile was found.
    # We raise a standard 404 Not Found error.
    if not profile:
        raise HTTPException(
            status_code=404,
            detail=f"No entity found with {identifier_type}: {identifier_value}"
        )

    return profile
