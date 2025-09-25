"""
Proposal Generator - AI-powered tool for converting discovery call transcripts into business proposals.
"""

from .models import CustomerInfo, ImplementationPhase, ProjectRequirements, ProposalData
from .workflow import ProposalWorkflow

__version__ = "0.1.0"
__all__ = [
    "ProposalWorkflow",
    "CustomerInfo",
    "ProjectRequirements",
    "ProposalData",
    "ImplementationPhase",
]
