"""
Proposal Generator - AI-powered tool for converting discovery call transcripts into business proposals.
"""

from .workflow import ProposalWorkflow
from .models import CustomerInfo, ProjectRequirements, ProposalData, ImplementationPhase

__version__ = "0.1.0"
__all__ = ["ProposalWorkflow", "CustomerInfo", "ProjectRequirements", "ProposalData", "ImplementationPhase"]