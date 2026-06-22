from fastapi import APIRouter

from ..schemas.analysis import AnalysisRequest, AnalysisResponse
from ..services.analysis import PasswordStrengthAnalyzer

router = APIRouter(prefix="/api/analysis", tags=["analysis"])
_analyzer = PasswordStrengthAnalyzer()


@router.post("/score", response_model=AnalysisResponse)
async def score_password(request: AnalysisRequest) -> AnalysisResponse:
    result = _analyzer.analyze_password(
        request.password,
        name=request.name,
        username=request.username,
        email=request.email,
        dob=request.dob,
    )
    return AnalysisResponse(**result)
