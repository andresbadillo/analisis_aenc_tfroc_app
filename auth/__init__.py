"""
Módulo de autenticación para la aplicación de análisis AENC y TFROC.
"""

from .azure_auth import AzureAuth
from .sharepoint import SharePointClient

__all__ = ['AzureAuth', 'SharePointClient']
