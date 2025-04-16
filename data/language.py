
from typing import Dict, Any

# Language configuration
SUPPORTED_LANGUAGES: Dict[str, Dict[str, str]] = {
    "English": {
        "code": "en",
        "welcome": """
        👋 Welcome to RAN Ops Assist! 
        
        I'm your AI-powered NOC (Network Operations Center) assistant, specialized in Radio Access Network (RAN) operations. 
        
        I can help you with:
        - Troubleshooting network issues
        - Providing insights on alarms and incidents
        - Guiding you through NOC best practices
        
        How can I assist you today with your telecom network operations?
        """
    },
    "Romanian": {
        "code": "ro",
        "welcome": """
        👋 Bun venit la RAN Ops Assist! 
        
        Sunt asistentul dvs. NOC (Network Operations Center) bazat pe AI, specializat în operațiuni Radio Access Network (RAN). 
        
        Vă pot ajuta cu:
        - Depanarea problemelor de rețea
        - Oferirea de informații despre alarme și incidente
        - Ghidarea prin cele mai bune practici NOC
        
        Cum vă pot ajuta astăzi cu operațiunile dvs. de rețea de telecomunicații?
        """
    },
    "German": {
        "code": "de",
        "welcome": """
        👋 Willkommen bei RAN Ops Assist! 
        
        Ich bin Ihr KI-gestützter NOC (Network Operations Center) Assistent, spezialisiert auf Radio Access Network (RAN) Betrieb. 
        
        Ich kann Ihnen helfen bei:
        - Fehlerbehebung von Netzwerkproblemen
        - Einblicke in Alarme und Vorfälle
        - Anleitung durch NOC Best Practices
        
        Wie kann ich Ihnen heute bei Ihren Telekommunikationsnetzwerk-Operationen helfen?
        """
    }
}