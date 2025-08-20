"""
Módulo de autenticación con Azure AD para la aplicación de análisis AENC y TFROC.
"""

import streamlit as st
from streamlit_oauth import OAuth2Component
from config.azure_config import AZURE_CONFIG


class AzureAuth:
    """
    Clase para manejar la autenticación con Azure AD.
    """
    
    def __init__(self):
        """Inicializa la configuración de Azure AD."""
        self.client_id = AZURE_CONFIG['client_id']
        self.client_secret = AZURE_CONFIG['client_secret']
        self.tenant_id = AZURE_CONFIG['tenant_id']
        self.redirect_uri = AZURE_CONFIG['redirect_uri']
        self.scope = " ".join(AZURE_CONFIG['scopes'])
        
        # Configurar endpoints
        self.authorize_endpoint = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/authorize"
        self.token_endpoint = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"
        
        # Inicializar componente OAuth2
        self.oauth2 = OAuth2Component(
            self.client_id,
            self.client_secret,
            authorize_endpoint=self.authorize_endpoint,
            token_endpoint=self.token_endpoint
        )
    
    def authenticate(self):
        """
        Maneja el flujo de autenticación.
        
        Returns:
            str or None: Token de acceso si la autenticación es exitosa, None en caso contrario.
        """
        if "token" not in st.session_state:
            st.markdown("<br>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns([2, 2, 2])
            with col2:
                result = self.oauth2.authorize_button(
                    name="🔐 Inicia sesión con tus credenciales de Ruitoque",
                    redirect_uri=self.redirect_uri,
                    scope=self.scope,
                    key="azure_aenc_tfroc"
                )
            
            if not result:
                return None
            elif "access_token" in result:
                st.session_state["token"] = result["access_token"]
                st.rerun()
            elif "token" in result and "access_token" in result["token"]:
                st.session_state["token"] = result["token"]["access_token"]
                st.rerun()
            else:
                st.error(f"❌ Error en la autenticación: {result}")
                st.write("Resultado de autenticación:", result)
                return None
        
        return st.session_state.get("token")
    
    def get_token(self):
        """
        Obtiene el token de acceso de la sesión.
        
        Returns:
            str or None: Token de acceso si existe, None en caso contrario.
        """
        return st.session_state.get("token")
    
    def is_authenticated(self):
        """
        Verifica si el usuario está autenticado.
        
        Returns:
            bool: True si el usuario está autenticado, False en caso contrario.
        """
        return "token" in st.session_state and st.session_state["token"] is not None
    
    def logout(self):
        """
        Cierra la sesión del usuario.
        """
        if "token" in st.session_state:
            del st.session_state["token"]
        st.rerun()
