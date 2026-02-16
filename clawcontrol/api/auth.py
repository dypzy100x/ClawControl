"""
Authentication for Claw Control API
"""
from fastapi import Header, HTTPException, status
from clawcontrol.core.config import config


async def verify_token(x_claw_token: str = Header(...)):
    """
    Verify X-CLAW-TOKEN header matches configured token
    
    Args:
        x_claw_token: Token from request header
        
    Raises:
        HTTPException: If token is invalid
        
    Returns:
        True if valid
    """
    if x_claw_token != config.claw_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing X-CLAW-TOKEN header"
        )
    return True
